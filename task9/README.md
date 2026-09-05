# Задание 9 — веб-сервис

На текущем этапе реализована локальная версия приложения на FastAPI.

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

## Ручная проверка

```powershell
curl.exe -i -X POST -H "Test: Hello" http://127.0.0.1:8000/
curl.exe -i -X POST -H "Test: Wrong" http://127.0.0.1:8000/
curl.exe -i http://127.0.0.1:8000/health
```