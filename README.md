# Тестовое задание DevOps

## Состав репозитория

| Задание | Что сделано |
| --- | --- |
| 1 | Перенос текста по словам с ограничением длины строки |
| 2 | Проверка возможности составить счастливый билет |
| 3 | Получение значения из вложенного словаря |
| 4 | Преобразование JSON-строки в Python-объект |
| 5 | Заполнение пропусков одного DataFrame значениями другого |
| 6 | CRUD API на FastAPI |
| 7 | Авторизация по JWT и хеширование паролей |
| 8 | Цепочка из трёх Jenkins Pipeline jobs |
| 9 | FastAPI-приложение, Docker, мониторинг, сеть и Kubernetes |
| 10 | Cilium, Istio и OPA Gatekeeper для защиты приложения |

Файлы заданий 1–7 находятся в корне. Для заданий 8–10 предусмотрены отдельные
каталоги с README и конфигурацией.

Зависимости для Python-заданий устанавливаются одной командой:

```bash
python -m pip install -r requirements-python.txt
```

Для запуска задания 7 нужно передать ключ подписи JWT через окружение. Пример
для PowerShell:

```powershell
$env:JWT_SECRET_KEY = "local-only-change-this-secret-12345"
python task7.py
```

## Быстрая проверка задания 9

```powershell
cd task9
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Инфраструктурные настройки описаны в [task9/README.md](task9/README.md), а
политики безопасности — в [task10/README.md](task10/README.md).
