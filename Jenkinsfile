pipeline {
    agent any

    environment {
        ECR_REPO = "240317130487.dkr.ecr.ap-northeast-2.amazonaws.com/datespot"
        DOCKER_IMAGE_TAG = "datespot-${BUILD_NUMBER}"
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
       stage('Build and Tag Image') {
            steps {
                sh '''
                    docker build -t ${ECR_REPO}:${DOCKER_IMAGE_TAG} .
                    docker tag ${ECR_REPO}:${DOCKER_IMAGE_TAG} ${ECR_REPO}:latest
                '''
            }
        }
         stage('Push to ECR') {
            steps {
                withAWS(credentials: 'datespotecr', region: 'ap-northeast-2') {
                    sh '''
                        aws ecr get-login-password --region ap-northeast-2 | docker login --username AWS --password-stdin ${ECR_REPO}
                        docker push ${ECR_REPO}:${DOCKER_IMAGE_TAG}
                        docker push ${ECR_REPO}:latest
                    '''
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
