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
            description: 'Passed to Job_3 for restoring files from Git.'
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

        stage('Delete demonstration files') {
            steps {
                bat(
                    label: 'Run Job_2 PowerShell script',
                    script: 'powershell.exe -NoLogo -NoProfile -NonInteractive -ExecutionPolicy Bypass -File "task8/scripts/job2_delete.ps1" -WorkDirectory "%EFFECTIVE_PROJECT_DIR%"'
                )
            }
        }
    }

    post {
        success {
            build(
                job: 'Job_3',
                wait: false,
                parameters: [
                    string(name: 'TARGET_BRANCH', value: env.EFFECTIVE_TARGET_BRANCH),
                    string(name: 'PROJECT_DIR', value: env.EFFECTIVE_PROJECT_DIR)
                ]
            )
        }
    }
}
