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
