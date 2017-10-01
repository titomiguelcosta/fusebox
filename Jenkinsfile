pipeline {
    agent any

    def dockerImage = "titomiguelcosta/fusebox"
    def dockerHubAccountNameOnJenkins = "dockerhub-titomiguelcosta"

    stages {
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
        stage("Test") {
            steps {
                echo "Testing.."
            }
        }
        stage("Deploy") {
            steps {
                echo "Deploying.."
            }
        }
    }
}
