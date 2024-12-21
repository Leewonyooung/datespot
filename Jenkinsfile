pipeline {
    agent any
    environment {
		AWS_ECR = '240317130487.dkr.ecr.ap-northeast-2.amazonaws.com'
		AWS_IMAGE_NAME= 'datespot'
		AWS_REGION = 'ap-northeast-2'
		AWS_CREDENTIALS_ID = 'datespotecr'
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
		stage('build_and_upload_docker') {
			steps {
				script {
					build_data = docker.build(
					"${AWS_ECR}/${AWS_IMAGE_NAME}:latest",
					". -f Dockerfile.patch +@ ETC OPTION"
					)
					docker.withRegistry("https://${AWS_ECR}", "ecr:${AWS_REGION}:${AWS_CREDENTIALS_ID}") {
					build_data.push("${env.gitlabBranch}")
					build_data.push("${env.gitlabBranch}-${env.BUILD_NUMBER}")
					build_data.push("${env.gitlabBranch}-${env.GIT_COMMIT}")
					build_data.push("${env.gitlabBranch}-latest")
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
                // 컨테이너 실행
                sh "docker-compose up -d"
            }
        }
    }
}
