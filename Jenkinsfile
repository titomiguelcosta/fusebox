pipeline {
    agent any
    
    environment {
        dockerImage = "titomiguelcosta/fusebox"
        dockerImageTest = "${dockerImage}:build-${env.BUILD_NUMBER}"
        dockerHubAccountNameOnJenkins = "dockerhub-titomiguelcosta"
        envVariablesOnJenkins = "fusebox-env-variables-prod"
        withCredentials([[$class: "FileBinding", credentialsId: "${envVariablesOnJenkins}", variable: "ENV_FILE"]]) {
            envValues = readFile "$ENV_FILE"
        }
    }

    stages {
        stage("Deploy") {
            parallel {
                stage('Main Application') {
                    steps {
                        script {
                            if (env.BRANCH_NAME == "master") {
                                sh "ecs deploy --timeout 6000 --ignore-warnings --profile pixelfusion pixelfusion-dev fusebox2 ${envValues}"
                            }
                        }
                    }
                }
                stage('Prediction Worker') {
                    steps {
                        script {
                            if (env.BRANCH_NAME == "master") {
                                sh 'ecs deploy --timeout 6000 --ignore-warnings --profile pixelfusion pixelfusion-dev fusebox-predictions-service ${envValues}'
                            }
                        }
                    }
                }
                stage('Playlist Worker') {
                    steps {
                        script {
                            if (env.BRANCH_NAME == "master") {
                                sh 'ecs deploy --timeout 6000 --ignore-warnings --profile pixelfusion pixelfusion-dev fusebox-playlist-service ${envValues}'
                            }
                        }
                    }
                }
            }
        }
    }
}
