pipeline {
    agent any
    
    environment {
        dockerImage = "titomiguelcosta/fusebox"
        dockerHubAccountNameOnJenkins = "dockerhub-titomiguelcosta"
    }

    stages {
        stage("Build") {
            steps {
                sh "docker build -t ${dockerImage} ."
                withCredentials([[$class: "UsernamePasswordMultiBinding", credentialsId: "${dockerHubAccountNameOnJenkins}", usernameVariable: "USERNAME", passwordVariable: "PASSWORD"]]) {
                    sh "docker login --username=$USERNAME --password=$PASSWORD"
                    sh "docker push ${dockerImage}:latest"
                    sh "docker rmi -f ${dockerImage}"
                }
                script {
                    if (env.BRANCH_NAME == "master") {
                        sh 'ecs deploy --timeout 6000 --ignore-warnings --profile pixelfusion fusebox-cluster fusebox-service'
                    }
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
