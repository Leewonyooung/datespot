pipeline {
	agent any
	environment {
        DOCKER_CLI_PATH = '/usr/local/bin/docker' // Snap이 아닌 Docker Compose 설치 경로 설정
    }
	stages {
		stage("init") {
			steps {
				script {
					gv = load "script.groovy"
				}
			}
		}
		stage("Checkout") {
			steps {
				checkout scm
			}
		}
        stage("Build") {
            steps {
                script {
                    sh "${DOCKER_CLI_PATH}-compose build web"
                }
            }
        }
		stage("test") {
			when {
				expression {
					params.executeTests
				}
			}
			steps {
				script {
					gv.testApp()
				}
			}
		}
		stage("deploy") {
			steps {
				sh "docker-compose up -d"
			}
		}
	}
}