# Задание 8: CI/CD и Jenkins

Репозиторий демонстрирует автоматическую цепочку из трёх Jenkins Pipeline jobs:

```text
GitHub master --Poll SCM--> Job_1 --> Job_2 --> Job_3
```

1. `Job_1` получает ветку `master` из GitHub в локальный каталог Jenkins.
2. `Job_2` удаляет два демонстрационных файла.
3. `Job_3` восстанавливает эти файлы из `origin/master`.

## Файлы задания

```text
task8/
├── README.md
├── demo/
│   ├── keep.txt
│   ├── delete_me_1.txt
│   └── delete_me_2.txt
├── jenkins/
│   ├── Job_1.Jenkinsfile
│   ├── Job_2.Jenkinsfile
│   └── Job_3.Jenkinsfile
└── scripts/
    ├── job1_checkout.ps1
    ├── job2_delete.ps1
    └── job3_restore.ps1
```

## Безопасность

`Job_2` содержит фиксированный список разрешённых целей и удаляет только:

- `task8/demo/delete_me_1.txt`;
- `task8/demo/delete_me_2.txt`.

Перед удалением скрипт проверяет, что рабочий каталог является Git-репозиторием и что вычисленный путь находится внутри него. `keep.txt` и файлы `task1.py`–`task7.py` не удаляются.

`Job_3` использует точечный `git restore` только для двух демонстрационных файлов. Изменения обратно в GitHub не отправляются.

## Параметры по умолчанию

- Репозиторий: `https://github.com/DmitryBat9/test_for_devops.git`.
- Ветка: `master`.
- Общий рабочий каталог: `C:/Users/Dmitry/JenkinsWork/task8-project`.
- Проверка GitHub: один раз примерно в две минуты (`H/2 * * * *`).

Все три jobs должны использовать одинаковый `PROJECT_DIR`. `Job_1` передаёт его следующим jobs автоматически.

## Требуемые Jenkins plugins

- Git;
- Pipeline;
- Pipeline: Build Step.

Они входят в обычный набор `Install suggested plugins`. В разделе **Manage Jenkins → Tools → Git installations** Jenkins должен видеть `git.exe`. На используемом компьютере он расположен по адресу `E:\Git\cmd\git.exe`.

## Создание jobs

Jobs следует создать в порядке `Job_3`, `Job_2`, `Job_1`.

Для каждой job:

1. Выбрать **New Item**.
2. Ввести точное имя job и выбрать **Pipeline**.
3. В разделе **Pipeline** выбрать **Pipeline script from SCM**.
4. Выбрать SCM **Git**.
5. Указать Repository URL: `https://github.com/DmitryBat9/test_for_devops.git`.
6. Для публичного репозитория оставить Credentials как `- none -`.
7. Указать Branch Specifier: `*/master`.
8. Указать соответствующий Script Path.

| Job | Script Path |
| --- | --- |
| `Job_1` | `task8/jenkins/Job_1.Jenkinsfile` |
| `Job_2` | `task8/jenkins/Job_2.Jenkinsfile` |
| `Job_3` | `task8/jenkins/Job_3.Jenkinsfile` |

## Автоматический запуск

В `Job_1.Jenkinsfile` настроен `pollSCM`. Jenkins периодически проверяет ветку `master` и запускает `Job_1` только при появлении нового коммита.

После успешного выполнения:

- `Job_1` вызывает `Job_2`;
- `Job_2` вызывает `Job_3`;
- при ошибке следующая job не запускается.

После создания jobs необходимо один раз запустить `Job_1` через **Build with Parameters**, чтобы Jenkins загрузил Jenkinsfile и зарегистрировал триггер. Это первоначальная инициализация. Последующие запуски выполняются автоматически после изменений в `master`.

## Ожидаемый результат

В журналах должны появиться сообщения:

```text
[Job_1] Branch 'master' is ready at commit ...
[Job_2] Removed task8/demo/delete_me_1.txt
[Job_2] Removed task8/demo/delete_me_2.txt
[Job_3] Restored task8/demo/delete_me_1.txt
[Job_3] Restored task8/demo/delete_me_2.txt
[Job_3] Verified: the demonstration files match origin/master.
```

После завершения цепочки оба удалённых файла снова существуют, а их содержимое совпадает с версией в `origin/master`.
