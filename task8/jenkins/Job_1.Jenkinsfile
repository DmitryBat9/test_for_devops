pipeline {
    agent any

    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        disableConcurrentBuilds()
        skipDefaultCheckout(true)
        timeout(time: 10, unit: 'MINUTES')
        timestamps()
    }

    parameters {
        string(
            name: 'REPOSITORY_URL',
            defaultValue: 'https://github.com/DmitryBat9/test_for_devops.git',
            description: 'Git repository copied into the local Jenkins work directory.'
        )
        string(
            name: 'TARGET_BRANCH',
            defaultValue: 'master',
            description: 'Branch required by the test assignment.'
        )
        string(
            name: 'PROJECT_DIR',
            defaultValue: 'C:/Users/Dmitry/JenkinsWork/task8-project',
            description: 'Shared local project directory used by all three jobs.'
        )
    }

    triggers {
        pollSCM('H/2 * * * *')
    }

    stages {
        stage('Checkout pipeline sources') {
            steps {
                checkout scm
            }
        }

        stage('Checkout master to local storage') {
            steps {
                bat(
                    label: 'Run Job_1 PowerShell script',
                    script: 'powershell.exe -NoLogo -NoProfile -NonInteractive -ExecutionPolicy Bypass -File "task8/scripts/job1_checkout.ps1" -RepositoryUrl "%REPOSITORY_URL%" -Branch "%TARGET_BRANCH%" -WorkDirectory "%PROJECT_DIR%"'
                )
            }
        }
    }

    post {
        success {
            build(
                job: 'Job_2',
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
