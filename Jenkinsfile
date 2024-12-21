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
        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t 240317130487.dkr.ecr.ap-northeast-2.amazonaws.com/datespot/datespot:latest -f Dockerfile .
                '''
            }
        }
        stage('Push Docker Image to ECR Repo') {
            steps {
                withAWS(credentials: 'datespot-pushecr', region: 'ap-northeast-2') {
                    sh 'aws ecr get-login-password --region ap-northeast-2 | docker login --username AWS --password-stdin "240317130487.dkr.ecr.ap-northeast-2.amazonaws.com"'
                    sh 'docker push "240317130487.dkr.ecr.ap-northeast-2.amazonaws.com/datespot/datespot:latest"'
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
