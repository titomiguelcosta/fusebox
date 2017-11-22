pipeline {
    agent any
    
    environment {
        dockerImage = "titomiguelcosta/fusebox"
        dockerImageTest = "${dockerImage}:build-${env.BUILD_NUMBER}"
        dockerHubAccountNameOnJenkins = "dockerhub-titomiguelcosta"
    }

    stages {
        stage("Test") {
            steps {
                sh "docker build -t ${dockerImageTest} -f Dockerfile.ci ."
                sh "docker run ${dockerImageTest} make lint"
                sh "docker run ${dockerImageTest} make tests"
                sh "docker rmi -f ${dockerImageTest}"
            }
        }
        stage("Build") {
            steps {
                sh "docker build -t ${dockerImage} ."
                withCredentials([[$class: "UsernamePasswordMultiBinding", credentialsId: "${dockerHubAccountNameOnJenkins}", usernameVariable: "USERNAME", passwordVariable: "PASSWORD"]]) {
                    sh "docker login --username=$USERNAME --password=$PASSWORD"
                    sh "docker push ${dockerImage}:latest"
                    sh "docker rmi -f ${dockerImage}"
                }
            }
        }
        stage("Deploy") {
            steps {
                script {
                    if (env.BRANCH_NAME == "master") {
                        echo "Deploying.."
                        sh 'ecs deploy --timeout 6000 --ignore-warnings --profile pixelfusion fusebox-cluster fusebox-service'
                    }
                }
            }
        }
    }
}
