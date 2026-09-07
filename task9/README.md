# Задание 9 — развёртывание веб-сервиса

В задании реализовано FastAPI-приложение и несколько способов его запуска:
локально, как systemd-сервис, в Docker Compose и в Kubernetes.

## Эндпоинты

- `POST /` возвращает `Hello, World!`, если передан HTTP-заголовок `Test: Hello`.
- `POST /` возвращает HTTP 403, если заголовок отсутствует или имеет другое значение.
- `GET /health` выполняет ping адреса `77.88.8.8` и возвращает `200 OK` с текстом `OK` при успехе.
- Если ping не прошёл, `GET /health` возвращает HTTP 503.

## Локальный запуск в Windows PowerShell

Команды выполняются из каталога `task9`:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

После запуска интерактивная документация FastAPI доступна по адресу:

```text
http://127.0.0.1:8000/docs
```

Автоматические тесты запускаются из каталога `task9`:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## Ручная проверка

```powershell
curl.exe -i -X POST -H "Test: Hello" http://127.0.0.1:8000/
curl.exe -i -X POST -H "Test: Wrong" http://127.0.0.1:8000/
curl.exe -i http://127.0.0.1:8000/health
```

## Docker

Образ собирается из каталога `task9`:

```bash
docker build --tag task9-app:1.0 .
```

Контейнер запускает приложение от непривилегированного пользователя `app`
с UID `10001` и содержит утилиту `ping`, необходимую эндпоинту `/health`.

```bash
docker run --detach --name task9-app --publish 8000:8000 task9-app:1.0
```

## Docker Compose и мониторинг

`compose.yaml` запускает три контейнера в общей сети `task9-monitoring`:

- `app` — FastAPI-приложение и эндпоинт метрик `/metrics`;
- `prometheus` — сбор метрик приложения каждые 10 секунд;
- `alertmanager` — приём и отображение тревог от Prometheus.

Перед первым запуском Compose нужно удалить одиночный контейнер с тем же именем:

```bash
sudo docker rm --force task9-app
sudo docker compose up --detach --build
sudo docker compose ps
```

Локальные адреса внутри Ubuntu:

- приложение: `http://127.0.0.1:8000`;
- метрики приложения: `http://127.0.0.1:8000/metrics`;
- Prometheus: `http://127.0.0.1:9090`;
- Alertmanager: `http://127.0.0.1:9093`.

Настроены две тревоги:

- `Task9AppDown` — Prometheus не может опросить приложение 30 секунд;
- `Task9PingFailed` — `/health` зафиксировал неуспешный ping в течение 30 секунд.

Внешний получатель уведомлений пока не задан, поэтому Alertmanager показывает
тревоги в веб-интерфейсе, но не отправляет письма или сообщения.

## Сеть и systemd

В каталоге `network` лежат настройки Netplan и nftables для отдельного
маршрутизатора. Внешняя сеть получает доступ только к явно разрешённым
NodePort-портам. Файл `systemd/task9-app.service` используется для запуска
приложения без Docker от отдельного пользователя `task9app`.

## Kubernetes

Манифесты находятся в `kubernetes/manifests`. Deployment запускает две реплики,
задаёт requests/limits, проверки состояния и непривилегированный UID `10001`.

```bash
kubectl apply -f kubernetes/manifests/namespace.yaml
kubectl apply -f kubernetes/manifests/deployment.yaml
kubectl apply -f kubernetes/manifests/service.yaml
kubectl apply -f kubernetes/manifests/ingress.yaml
kubectl -n task9 rollout status deployment/task9-app
kubectl -n task9 get pods -o wide
```

Скрипты в `kubernetes/scripts` подготавливают Ubuntu-узлы и устанавливают
ingress-nginx. В итоговой конфигурации задания 10 внешний трафик идёт через
Istio Ingress Gateway на NodePort `30081`; соответствующие политики находятся
в каталоге `task10`.
