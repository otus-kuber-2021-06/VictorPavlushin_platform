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
