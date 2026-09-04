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
                    script: 'powershell.exe -NoLogo -NoProfile -NonInteractive -ExecutionPolicy Bypass -File "task8/scripts/job2_delete.ps1" -WorkDirectory "%PROJECT_DIR%"'
                )
            }
        }
    }

    post {
        success {
            build(
                job: 'Job_3',
                wait: true,
                propagate: true,
                parameters: [
                    string(name: 'TARGET_BRANCH', value: params.TARGET_BRANCH),
                    string(name: 'PROJECT_DIR', value: params.PROJECT_DIR)
                ]
            )
        }
    }
}
