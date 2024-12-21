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
				script {
				     docker.withRegistry("https://240317130487.dkr.ecr.ap-northeast-2.amazonaws.com/datespot", "ecr:ap-northeast-2:Jenkinsdatespot-pushecr") {
					     sh "docker push https://240317130487.dkr.ecr.ap-northeast-2.amazonaws.com/datespot/image:tag"
					}
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