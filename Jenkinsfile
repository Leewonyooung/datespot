pipeline {
    agent any

    environment {
        DOCKER_IMAGE_TAG = "datespot-${BUILD_NUMBER}"  // Docker 이미지 태그 버전
        ECR_REPO = "240317130487.dkr.ecr.ap-northeast-2.amazonaws.com/datespot"
        AWS_REGION = "ap-northeast-2"
    }

    stages {
        stage("Init") {
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
                    echo "Building Docker Image with tag: ${DOCKER_IMAGE_TAG}"
                    docker build -t ${ECR_REPO}:${DOCKER_IMAGE_TAG} -f Dockerfile .
                '''
            }
        }
        stage('Push Docker Image to ECR Repo') {
            steps {
                withAWS(credentials: 'datespotecr', region: "${AWS_REGION}") {
                    sh '''
                        # Login to ECR
                        aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin "${ECR_REPO}"
                        
                        # Push new Docker image
                        echo "Pushing Docker Image with tag: ${DOCKER_IMAGE_TAG}"
                        docker push "${ECR_REPO}:${DOCKER_IMAGE_TAG}"
                        
                        # Update the 'latest' tag
                        echo "Tagging and pushing 'latest' tag"
                        docker tag "${ECR_REPO}:${DOCKER_IMAGE_TAG}" "${ECR_REPO}:latest"
                        docker push "${ECR_REPO}:latest"
                    '''
                }
            }
        }
        stage("Clean Old Images") {
            steps {
                withAWS(credentials: 'datespotecr', region: "${AWS_REGION}") {
                    script {
                        // Clean up old images
                        def imagesToDelete = sh(
                            script: """
                                aws ecr describe-images \\
                                    --repository-name datespot \\
                                    --query 'imageDetails[?contains(imageTags, `latest`) == `false`].imageDigest' \\
                                    --output text
                            """,
                            returnStdout: true
                        ).trim().split('\n')
                        
                        if (imagesToDelete.size() > 5) {  // Keep only the latest 5 versions
                            echo "Deleting old images: ${imagesToDelete.join(', ')}"
                            sh """
                            aws ecr batch-delete-image \\
                                --repository-name datespot \\
                                --region ${AWS_REGION} \\
                                --image-ids $(for digest in ${imagesToDelete[0..-6].join(' ')}; do echo imageDigest=$digest; done)
                            """
                            }
                    }
                }
            }
        }
        stage("Test") {
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
        stage("Deploy") {
            steps {
                sh '''
                    echo "Deploying Docker Image with tag: ${DOCKER_IMAGE_TAG}"
                    DOCKER_IMAGE_TAG=${DOCKER_IMAGE_TAG} docker-compose up -d
                '''
            }
        }
    }
}
