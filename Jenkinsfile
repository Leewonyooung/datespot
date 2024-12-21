pipeline {
	agent any
	
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
        stage('Build') {
            steps {
                sh '/usr/local/bin/docker-compose build web'
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