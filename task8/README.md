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

Перед удалением скрипт проверяет, что рабочий каталог является Git-репозиторием и что вычисленный путь находится внутри него. `keep.txt`.

`Job_3` использует точечный `git restore` только для двух демонстрационных файлов. Изменения обратно в GitHub не отправляются.