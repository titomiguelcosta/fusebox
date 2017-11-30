pipeline {
    agent any
    
    environment {
        dockerImage = "titomiguelcosta/fusebox"
        dockerImageTest = "${dockerImage}:build-${env.BUILD_NUMBER}"
        dockerHubAccountNameOnJenkins = "dockerhub-titomiguelcosta"
        envVariablesOnJenkins = "fusebox-env-variables-prod"
    }

    stages {
        stage("Validate") {
            steps {
                sh 'docker build -t ${dockerImageTest} -f Dockerfile.ci .'
                sh 'docker run ${dockerImageTest} make lint'
                sh 'docker run ${dockerImageTest} make tests'
                sh 'docker rmi -f ${dockerImageTest}'
            }
        }
        stage("Build") {
            steps {
                sh 'docker build -t ${dockerImage} .'
                withCredentials([[$class: "UsernamePasswordMultiBinding", credentialsId: "${dockerHubAccountNameOnJenkins}", usernameVariable: "USERNAME", passwordVariable: "PASSWORD"]]) {
                    sh 'docker login --username=$USERNAME --password=$PASSWORD'
                    sh 'docker push ${dockerImage}:latest'
                    sh 'docker rmi -f ${dockerImage}'
                }
            }
        }
        stage("Deploy") {
            parallel {
                stage('Main Application') {
                    steps {
                        script {
                            withCredentials([[$class: "FileBinding", credentialsId: "${envVariablesOnJenkins}", variable: "ENV_FILE"]]) {
                                if (env.BRANCH_NAME == "master") {
                                    env_values = readFile "$ENV_FILE"
                                    sh 'ecs deploy --timeout 6000 --ignore-warnings --profile pixelfusion pixelfusion-dev fusebox2 $env_values'
                                }
                            }
                        }
                    }
                }
                stage('Prediction Worker') {
                    steps {
                        script {
                            withCredentials([[$class: "FileBinding", credentialsId: "${envVariablesOnJenkins}", variable: "ENV_FILE"]]) {
                                if (env.BRANCH_NAME == "master") {
                                    env_values = readFile "$ENV_FILE"
                                    sh 'ecs deploy --timeout 6000 --ignore-warnings --profile pixelfusion pixelfusion-dev fusebox-predictions-service $env_values'
                                }
                            }
                        }
                    }
                }
                stage('Playlist Worker') {
                    steps {
                        script {
                            withCredentials([[$class: "FileBinding", credentialsId: "${envVariablesOnJenkins}", variable: "ENV_FILE"]]) {
                                if (env.BRANCH_NAME == "master") {
                                    env_values = readFile "$ENV_FILE"
                                    sh 'ecs deploy --timeout 6000 --ignore-warnings --profile pixelfusion pixelfusion-dev fusebox-playlist-service $env_values'
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
