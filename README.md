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
