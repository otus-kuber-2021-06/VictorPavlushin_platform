<details>
<summary><b>Выполнено ДЗ №8</b></summary>

 - [X] Основное ДЗ
 - [X] Задания со *

## В процессе сделано:
 - Задание по CRD: выставленны все поля как обязательные
 - MySQL контроллер: Поправлены темплейты, а также добавлено удаление PV котое не удалялось хотя и есть в зависимостях. Самописный
   Вопрос: почему объект создался, хотя мы создали CR, до того, как запустили контроллер?
   Согласно документации https://kopf.readthedocs.io/en/latest/walkthrough/starting/ это нрмальное поведение, и скорее всего при запуске оператора kopf смотрит events.events.k8s.io и от туда выберает нужные события.
 - Деплой оператора: из образа docker.io/vii98/mysql-operator:latest
 - Проверки ручные прошли
 - Задание со звездой 1: В конце функции ставится:
   ```python
      return {'message': f"mysql-instance created {r_result} restore-job"}
   ```
   который и отображается в статусе
   `r_result` берется в зависимости от успешности выполнения:
   ```python
   api.create_namespaced_job('default', restore_job)
   ```
 - Задание со звездой 2: выполнено
   Работает:
   ```bash
   [vii@localhost deploy]$ export MYSQLPOD=$(kubectl get pods -l app=mysql-instance -o jsonpath="{.items[*].metadata.name}")
   [vii@localhost deploy]$ kubectl exec -it $MYSQLPOD -- mysql -potuspassword -e "select * from test;" otus-database
   mysql: [Warning] Using a password on the command line interface can be insecure.
   +----+-------------+
   | id | name        |
   +----+-------------+
   |  1 | some data   |
   |  2 | some data-2 |
   +----+-------------+
   [vii@localhost deploy]$ kubectl patch mysqls.otus.homework mysql-instance --patch "$(echo -e 'spec:\n  password: otuspassword1')" --type=merge
   mysql.otus.homework/mysql-instance patched
   [vii@localhost deploy]$ kubectl exec -it $MYSQLPOD -- mysql -potuspassword -e "select * from test;" otus-database
   mysql: [Warning] Using a password on the command line interface can be insecure.
   ERROR 1045 (28000): Access denied for user 'root'@'localhost' (using password: YES)
   command terminated with exit code 1
   [vii@localhost deploy]$ kubectl exec -it $MYSQLPOD -- mysql -potuspassword1 -e "select * from test;" otus-database
   mysql: [Warning] Using a password on the command line interface can be insecure.
   +----+-------------+
   | id | name        |
   +----+-------------+
   |  1 | some data   |
   |  2 | some data-2 |
   +----+-------------+
   ```
```python
@kopf.on.update('mysqls', field='spec.password') #Подписываемся на события из mysqls с изменением в поле spec.password
def update_pass(spec, name, old, new, status, namespace, logger, **kwargs):
    api_instance = kubernetes.client.api.core_v1_api.CoreV1Api()
    result = api_instance.list_namespaced_pod(namespace, label_selector="app="+name, watch=False) #Ищем нужный под
    exec_command = [
            '/bin/sh',
            '-c',
            f"mysql -u root -p{ old } -e \"update user set authentication_string=password(\'{new}\') where user='root';FLUSH PRIVILEGES;\" mysql"] #Формируем команду которая сменит пароль
    if len(result.items) == 1: #На всякий случай проверяем что под нашелся и он один
        if result.items[0].status.phase == 'Running': #На всякий случай проверяем что он в статусе Running
            resp = kubernetes.stream.stream(api_instance.connect_get_namespaced_pod_exec,  result.items[0].metadata.name,  namespace,  command=exec_command,  stderr=True, stdin=True, stdout=True, tty=False) #Меняем пароль
            print(f"{resp}") #Для дебага :)
```

## PR checklist:
 - [X] Выставлен label с темой домашнего задания
</details>


<details>
<summary><b>Выполнено ДЗ №7</b></summary>

 - [X] Основное ДЗ
 - [X] Задания со * но не все

## В процессе сделано:
 - Установлен nginx-ingress
 - Установлен cert-manager в лабе указан 0.16.1 но он не актуален т.к. происходит генерация сертификата подписанного устаревшим корневым сертификатом. Установлена паследняя версия
 - cert-manager Самостоятельное задание: Создан ClusterIssuer
 - chartmuseum установлен сертификат валидный
 - chartmuseum | Задание со зведой - частично выполнено в harbor
 - harbor установлена последняя версия т.к. та что в задании не запускается, скачан оригинальный values.yaml и прописынны нужные значения. Сертификат выдался валидный.
 - Используем helmfile | Задание со звездой: выполнено
 - Создаем свой helm chart: создан микросервис frontend, шаблонизирован, и добавлен в зависимость к hipster-shop.
 - Создаем свой helm chart | Задание со звездой: вынесен как микросервис Redis и зависимость реализованна через requirements.yaml, работаспособность сохранена
 - Проверка: т.к. поднят harbor у нас, туда были поменщены репы и возможность установки появилась
 - Kubecfg: вынесены сервисы paymentservice и shippingservice. При добавлении libsonnet из домашнего задания не работло т.к. у деплоймента apiVersion указывалось apps/v1beta2, а это уже не работает.
   Поледняя версия тоже не работала. Т.о. была скачана старая версия libsonnet и поправлена локально.
 - Задание со звездой по другим решение на основе jsonnet, не выполнено.
 - Kustomize выполнено

## PR checklist:
 - [X] Выставлен label с темой домашнего задания
</details>

<details>
<summary><b>Выполнено ДЗ №6</b></summary>

 - [X] Основное ДЗ
 - [X] Задания со *

## В процессе сделано:
 - Скопироаны и препенены фаилы minio-statefulset.yaml и minio-headless-service.yaml
 - Создан фаил секретов minio-secrets.yaml и переделан statefulSet на использование секретов.

## Как запустить проект:
 - Применить манифесты kubectl apply -f *.yaml

## Как проверить работоспособность:
 - mc *

## PR checklist:
 - [X] Выставлен label с темой домашнего задания
 - [X] Выставлена метка Review Required
</details>

<details>
<summary><b>Выполнено ДЗ №5</b></summary>

 - [X] Основное ДЗ
 - [X] Задания со *

## В процессе сделано:
 - Добавление проверок Pod - выполнено
   Вопрос для самопроверки: по идее мы имеем дело с микросервисами, и у нас один основной процесс если он не работает то не будет работать все, но у нас может быть бекенд (2 сервиса в одном контейнере) который работает с фронтендом например по unix.socket...
 - Создание объекта Deployment - выполено
   Сомастоятельная работа по Deployment - выполено
 - Добавление сервисов в кластер ( ClusterIP ) - выполнено
 - Включение режима балансировки IPVS - выполнено
 - Установка MetalLB в Layer2-режиме - выполнено
 - Добавление сервиса LoadBalancer - выполнено
 - Установка Ingress-контроллера и прокси ingress-nginx - выполнено
 - Создание правил Ingress - выполнено

## Как запустить проект:
 - Применить манифесты kubectl apply -f *.yaml

## Как проверить работоспособность:
 - curl
 - Веббраузер

## PR checklist:
 - [X] Выставлен label с темой домашнего задания
</details>

<details>
<summary><b>Выполнено ДЗ №4</b></summary>

 - [X] Основное ДЗ

## В процессе сделано:
 - Пункт 1: Созданы и применены манифест файлы для задачи 1;
 - Пункт 2: Созданы и применены манифест файлы для задачи 2;
 - Пункт 3: Созданы и применены манифест файлы для задачи 3;

## Как запустить проект:
 - Применить манифесты kubectl apply -f *.yaml

## Как проверить работоспособность:
 - kubectl get ns
 - kubectl get pods
 - kubectl get sa [-n NameSpace]
 - kubectl describe sa USER
 - kubectl get clusterrole [-n NameSpace]
 - kubectl get role [-n NameSpace]
 - kubectl get clusterrolebindings [-n NameSpace]
 - kubectl get rolebindings [-n NameSpace]
 - kubectl auth can-i VERB pods -A --as system:serviceaccount:default:USER

## PR checklist:
 - [X] Выставлен label с темой домашнего задания
</details>

<details>
<summary><b>Выполнено ДЗ №3</b></summary>

 - [X] Основное ДЗ
 - [X] Задания со *

## В процессе сделано:
 - Пункт 1:
    - Уcтановлен kind
    - Из манифест файла kind-config.yaml развернут кластер
    - Создан манифест файл frontend-replicaset.yaml и проведено тестирование
    - Cоздан манифест файл paymentservice-replicaset.yaml
    - Cоздан манифест файл paymentservice-deployment.yaml и развернут Deployment
    - Проведено обновление образов и пересоздание Pods
    - Проведен откат к передыдущей версии образа.
    - Создан манифес frontend-deployment.yaml и проведено тестирование readinessProde.
  Type     Reason     Age               From               Message
  ----     ------     ----              ----               -------
  Normal   Started    65s               kubelet            Started container server
  Warning  Unhealthy  7s (x5 over 47s)  kubelet            Readiness probe failed: HTTP probe failed with statuscode: 404	

    Контролер ReplicaSet отслеживает только изменеия в ключе replicas и соответсвие запущеных pods и не следит за остальными 
изменениями в манифест файле. Для отслеживания именений замены имиджа, необходимо использовать Deployment.

 - Дополнительное задание 1:
    - Созданы манифест фаqлы: paymentservice-deployment-bg.yaml и paymentservice-deployment-reverse.yaml
    - Протестированы стратегии обновления Deployment: blue-green и Reverse Rolling Update

 - Дополнительное задание 2:
    - Сгенерирован frontend-pod-healthy.yaml
    - После исправления файла frontend-pod-healthy.yaml запущенный pod в статусе Running

 - Дополнительное задание 3:
    - Для деплоя на master nodes необходимо добавить в манифест файл node-exporter-daemonset.yaml
    ключ tolerations и соответствующие параметры.
```	
    tolerations:
      - key: node-role.kubernetes.io/master
        operator: Exists
        effect: NoSchedule	
```

## Как запустить проект:
 - Создать кластер kind create cluster --config kind-config.yaml
 - Создать Pods командой kubectl apply -f *.yaml

## Как проверить работоспособность:
 - Настроить форвардинг портов для pod коммандой: kubectl port-forward --address 0.0.0.0 kubectl port-forward node-exporter-* 9100:9100
 - Выполнить запрос curl localhost:9100/metrics

## PR checklist:
 - [X] Выставлен label с темой домашнего задания
</details>

<details>
<summary><b>Выполнено ДЗ №2</b></summary>

 - [X] Основное ДЗ
 - [X] Задание со *

## В процессе сделано:

 - Пункт 1:
    - Уcтановлен kubectl
    - Установлен minikube
    - Cоздан Dockerfile, в котором описан образ web сервера на nginx
    - Cобран докер образ и размещен в Container Registry Docker Hub
    - Создан манифест файл web-pod.yaml

 - Пункт 2:
    - Собран и загружен образ Hipster Shop
    - Сгенерирован frontend-pod-healthy.yaml
    - После исправления файла frontend-pod-healthy.yaml запущенный pod в статусе Running	

## Как запустить проект:
 - Создать манифест файл web-pod.yaml
 - Создать pod командой kubectl apply -f web-pod.yaml

## Как проверить работоспособность:
 - Настроить форвардинг портов для pod коммандой: kubectl port-forward --address 0.0.0.0 pod/web 8000:8000
 - Перейти по ссылке http://localhost:8000/index.html

## PR checklist:
 - [X] Выставлен label с темой домашнего задания
</details>
