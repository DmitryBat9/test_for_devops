pipeline {
    agent any

    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        disableConcurrentBuilds()
        skipDefaultCheckout(true)
        timeout(time: 5, unit: 'MINUTES')
        timestamps()
    }

    parameters {
        string(
            name: 'TARGET_BRANCH',
            defaultValue: 'master',
            description: 'Branch used as the source for restoring files.'
        )
        string(
            name: 'PROJECT_DIR',
            defaultValue: 'C:/Users/Dmitry/JenkinsWork/task8-project',
            description: 'Shared local project directory prepared by Job_1.'
        )
    }

    environment {
        EFFECTIVE_TARGET_BRANCH = "${params.TARGET_BRANCH ?: 'master'}"
        EFFECTIVE_PROJECT_DIR = "${params.PROJECT_DIR ?: 'C:/Users/Dmitry/JenkinsWork/task8-project'}"
    }

    stages {
        stage('Checkout pipeline sources') {
            steps {
                checkout scm
            }
        }

        stage('Restore project from Git') {
            steps {
                bat(
                    label: 'Run Job_3 PowerShell script',
                    script: 'powershell.exe -NoLogo -NoProfile -NonInteractive -ExecutionPolicy Bypass -File "task8/scripts/job3_restore.ps1" -Branch "%EFFECTIVE_TARGET_BRANCH%" -WorkDirectory "%EFFECTIVE_PROJECT_DIR%"'
                )
            }
        }
    }
}
