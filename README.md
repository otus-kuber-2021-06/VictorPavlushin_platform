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
