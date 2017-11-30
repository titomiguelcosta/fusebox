pipeline {
    agent any
    
    environment {
        dockerImage = "titomiguelcosta/fusebox"
        dockerImageTest = "${dockerImage}:build-${env.BUILD_NUMBER}"
        dockerHubAccountNameOnJenkins = "dockerhub-titomiguelcosta"
        envVariablesOnJenkins = "fusebox-env-variables-prod"
    }

    stages {
        stage("Deploy") {
            parallel {
                stage('Main Application') {
                    steps {
                        script {
                            withCredentials([[$class: "FileBinding", credentialsId: "${envVariablesOnJenkins}", variable: "ENV_FILE"]]) {
                                if (env.BRANCH_NAME == "master") {
                                    env_values = readFile "$ENV_FILE"
                                    echo "FILE: $ENV_FILE"
                                    echo "CONTENTS: $env_values"
                                    sh "ecs deploy --timeout 6000 --ignore-warnings --profile pixelfusion pixelfusion-dev fusebox2 $env_values"
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
