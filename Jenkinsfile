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
        // stage('Build') {
        //     steps {
        //         // Docker Compose를 사용해 이미지 빌드
        //         sh '/usr/local/bin/docker-compose build web'
                
        //         // AWS ECR에 Docker 이미지 푸시
        //         script {
        //             docker.withRegistry("https://240317130487.dkr.ecr.ap-northeast-2.amazonaws.com", "ecr:ap-northeast-2:Jenkinsdatespot-pushecr") {
        //                 sh "docker tag web:latest 240317130487.dkr.ecr.ap-northeast-2.amazonaws.com/datespot:tag"
        //                 sh "docker push 240317130487.dkr.ecr.ap-northeast-2.amazonaws.com/datespot:tag"
        //             }
        //         }
        //     }
        // }
		stage('Build and Push to ECR') {
			steps {
				script {
					// Docker 이미지 빌드
					sh '''
						docker build -t datespot-pipeline-web:latest .
					'''
					
					// ECR에 Docker 이미지 푸시
					docker.withRegistry("https://240317130487.dkr.ecr.ap-northeast-2.amazonaws.com", "pushecr") {
						sh '''
							docker tag datespot-pipeline-web:latest 240317130487.dkr.ecr.ap-northeast-2.amazonaws.com/datespot:latest
							docker push 240317130487.dkr.ecr.ap-northeast-2.amazonaws.com/datespot:latest
						'''
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
