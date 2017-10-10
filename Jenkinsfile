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
                        withEnv(['AWS_PROFILE=pixelfusion']) {
                            sh 'python deploy.py'
                        }
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
