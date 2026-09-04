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
                    script: 'powershell.exe -NoLogo -NoProfile -NonInteractive -ExecutionPolicy Bypass -File "task8/scripts/job3_restore.ps1" -Branch "%TARGET_BRANCH%" -WorkDirectory "%PROJECT_DIR%"'
                )
            }
        }
    }
}
