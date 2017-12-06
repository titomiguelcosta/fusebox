def getLastSuccessfulCommit() {
    def lastSuccessfulHash = null
    def lastSuccessfulBuild = currentBuild.rawBuild.getPreviousSuccessfulBuild()
    if (lastSuccessfulBuild) {
        lastSuccessfulHash = commitHashForBuild(lastSuccessfulBuild)
    }

    return lastSuccessfulHash
}

def commitHashForBuild(build) {
    def scmAction = build?.actions.find { action -> action instanceof jenkins.scm.api.SCMRevisionAction }

    return scmAction?.revision?.hash
}

pipeline {
    agent any
    
    environment {
        dockerImage = "titomiguelcosta/fusebox"
        dockerImageTest = "${dockerImage}:build-${env.BUILD_NUMBER}"
        dockerHubAccountNameOnJenkins = "dockerhub-titomiguelcosta"
        envVariablesOnJenkins = "fusebox-env-variables-prod"
    }

    stages {
        stage("Pre Build") {
            steps {
                script {
                    echo "last build"
                    lastSuccessfulCommit = getLastSuccessfulCommit()

                    echo "$lastSuccessfulCommit"


                }
            }
        }

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
                            if (env.BRANCH_NAME == "master") {
                                withCredentials([[$class: "FileBinding", credentialsId: "${envVariablesOnJenkins}", variable: "ENV_FILE"]]) {
                                    envValues = readFile "$ENV_FILE"
                                    sh "ecs deploy --timeout 6000 --ignore-warnings --profile pixelfusion pixelfusion-dev fusebox2 $envValues"
                                }
                            }
                        }
                    }
                }
                stage('Prediction Worker') {
                    steps {
                        script {
                            if (env.BRANCH_NAME == "master") {
                                withCredentials([[$class: "FileBinding", credentialsId: "${envVariablesOnJenkins}", variable: "ENV_FILE"]]) {
                                    envValues = readFile "$ENV_FILE"
                                    sh "ecs deploy --timeout 6000 --ignore-warnings --profile pixelfusion pixelfusion-dev fusebox-predictions-service $envValues"
                                }
                            }
                        }
                    }
                }
                stage('Playlist Worker') {
                    steps {
                        script {
                            if (env.BRANCH_NAME == "master") {
                                withCredentials([[$class: "FileBinding", credentialsId: "${envVariablesOnJenkins}", variable: "ENV_FILE"]]) {
                                    envValues = readFile "$ENV_FILE"
                                    sh "ecs deploy --timeout 6000 --ignore-warnings --profile pixelfusion pixelfusion-dev fusebox-playlist-service $envValues"
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
