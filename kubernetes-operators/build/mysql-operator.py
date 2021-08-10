import kopf
import yaml
import kubernetes
import time
import logging
from jinja2 import Environment, FileSystemLoader

from kubernetes.stream import stream
from kubernetes.client.api import core_v1_api

logger = logging.getLogger(__name__)

def wait_until_job_end(jobname):
    api = kubernetes.client.BatchV1Api()
    job_finished = False
    jobs = api.list_namespaced_job('default')
    while (not job_finished) and any(job.metadata.name == jobname for job in jobs.items):
        time.sleep(1)
        jobs = api.list_namespaced_job('default')
        for job in jobs.items:
            if job.metadata.name == jobname:
                logger.info(f"job with { jobname }  found,wait untill end")
                if job.status.succeeded == 1:
                    logger.info(f"job with { jobname }  success")
                    job_finished = True

def render_template(filename, vars_dict):
    env = Environment(loader=FileSystemLoader('./templates'))
    template = env.get_template(filename)
    yaml_manifest = template.render(vars_dict)
    json_manifest = yaml.load(yaml_manifest, Loader=yaml.FullLoader)
    return json_manifest

def delete_success_jobs(mysql_instance_name):
    logger.info("start deletion")
    api = kubernetes.client.BatchV1Api()
    jobs = api.list_namespaced_job('default')
    for job in jobs.items:
        jobname = job.metadata.name
        if (jobname == f"backup-{mysql_instance_name}-job") or (jobname == f"restore-{mysql_instance_name}-job"):
            if job.status.succeeded == 1:
                api.delete_namespaced_job(jobname, 'default', propagation_policy='Background')

@kopf.on.create('otus.homework', 'v1', 'mysqls')
# Функция, которая будет запускаться при создании объектов тип MySQL:
def mysql_on_create(body, spec, **kwargs):
    name = body['metadata']['name']
    image = body['spec']['image'] # cохраняем в переменные содержимое описания MySQL из CR
    password = body['spec']['password']
    database = body['spec']['database']
    storage_size = body['spec']['storage_size']
    
    # Генерируем JSON манифесты для деплоя
    persistent_volume = render_template('mysql-pv.yml.j2', {'name': name, 'storage_size': storage_size})
    persistent_volume_claim = render_template('mysql-pvc.yml.j2', {'name': name, 'storage_size': storage_size})
    logger.info(f"{ persistent_volume_claim }")
    service = render_template('mysql-service.yml.j2', {'name': name})
    deployment = render_template('mysql-deployment.yml.j2', {
        'name': name,
        'image': image,
        'password': password,
        'database': database})
    restore_job = render_template('restore-job.yml.j2', {
        'name': name,
        'image': image,
        'password': password,
        'database': database})


    # Определяем, что созданные ресурсы являются дочерними к управляемому CustomResource:
    kopf.append_owner_reference(persistent_volume, owner=body)
    kopf.append_owner_reference(persistent_volume_claim, owner=body) # addopt
    kopf.append_owner_reference(service, owner=body)
    kopf.append_owner_reference(deployment, owner=body)
    kopf.append_owner_reference(restore_job, owner=body)
    # ^ Таким образом при удалении CR удалятся все, связанные с ним pv,pvc,svc, deployments

    api = kubernetes.client.CoreV1Api()
    # Создаем mysql PV:
    api.create_persistent_volume(persistent_volume)
    # Создаем mysql PVC:
    api.create_namespaced_persistent_volume_claim('default', persistent_volume_claim)
    # Создаем mysql SVC:
    api.create_namespaced_service('default', service)
    # Создаем mysql Deployment:
    api = kubernetes.client.AppsV1Api()
    api.create_namespaced_deployment('default', deployment)
    # Пытаемся восстановиться из backup
    try:
        api = kubernetes.client.BatchV1Api()
        r_result = 'with'
        api.create_namespaced_job('default', restore_job)
    except kubernetes.client.rest.ApiException:
        r_result = 'without'
        pass

    # Cоздаем PVC  и PV для бэкапов:
    try:
        backup_pv = render_template('backup-pv.yml.j2', {'name': name, 'storage_size': storage_size})
        api = kubernetes.client.CoreV1Api()
        api.create_persistent_volume(backup_pv)
    except kubernetes.client.rest.ApiException:
        logger.info(f"error create persistent volume \"backup-{ name }-pv\"")
        pass

    try:
        backup_pvc = render_template('backup-pvc.yml.j2', {'name': name, 'storage_size': storage_size})
        api = kubernetes.client.CoreV1Api()
        api.create_namespaced_persistent_volume_claim('default', backup_pvc)
    except kubernetes.client.rest.ApiException:
        logger.info(f"error create persistent volume claim \"backup-{ name }-pvc\"")
        pass
    return {'message': f"mysql-instance created {r_result} restore-job"}


@kopf.on.delete('otus.homework', 'v1', 'mysqls')
def delete_object_make_backup(body, **kwargs):
    name = body['metadata']['name']
    image = body['spec']['image']
    password = body['spec']['password']
    database = body['spec']['database']
    delete_success_jobs(name)
    # Cоздаем backup job:
    api = kubernetes.client.BatchV1Api()
    backup_job = render_template('backup-job.yml.j2', {
        'name': name,
        'image': image,
        'password': password,
        'database': database})
    api.create_namespaced_job('default', backup_job)
    wait_until_job_end(f"backup-{name}-job")
    api.delete_namespaced_job('default', name)
    apiv1 = kubernetes.client.CoreV1Api()
    apiv1.delete_persistent_volume(f"{ name }-pv")
    return {'message': "mysql and its children resources deleted"}


@kopf.on.update('mysqls', field='spec.password')
def update_pass(spec, name, old, new, status, namespace, logger, **kwargs):
    api_instance = kubernetes.client.api.core_v1_api.CoreV1Api()
    result = api_instance.list_namespaced_pod(namespace, label_selector="app="+name, watch=False)
    exec_command = [
            '/bin/sh',
            '-c',
            f"mysql -u root -p{ old } -e \"update user set authentication_string=password(\'{new}\') where user='root';FLUSH PRIVILEGES;\" mysql"]
    if len(result.items) == 1:
        if result.items[0].status.phase == 'Running':
            resp = kubernetes.stream.stream(api_instance.connect_get_namespaced_pod_exec,  result.items[0].metadata.name,  namespace,  command=exec_command,  stderr=True, stdin=True, stdout=True, tty=False)
            print(f"{resp}")
