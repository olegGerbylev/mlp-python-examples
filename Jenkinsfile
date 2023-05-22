pipeline {
    options {
        gitLabConnection("gitlab just-ai")
        buildDiscarder(logRotator(numToKeepStr: '10', artifactNumToKeepStr: '10'))
        disableConcurrentBuilds()
        timeout(time: 180, unit: 'MINUTES')
        timestamps()
    }
    agent {
        label 'caila-build-agent'
    }

    parameters {
        extendedChoice(name: 'COMPONENTS',
                value: 'python-client,python-composite-action,python-fit-action,python-rest-client,python-simple-action',
                defaultValue: 'python-client,python-composite-action,python-fit-action,python-rest-client,python-simple-action',
                description: '', descriptionPropertyValue: '', multiSelectDelimiter: ',', quoteValue: false, saveJSONParameterToFile: false, type: 'PT_MULTI_SELECT', visibleItemCount: 5)
    }
    stages {
        stage('notify gitlab') {
            steps {
                updateGitlabCommitStatus name: "build", state: "running"
            }
        }
        stage('Build') {
            steps {
                script {
                    echo "========================================================="
                    echo params.COMPONENTS

                    for (cmp in params.COMPONENTS.split(",")) {
                        stage("Build ${cmp}") {
                            script {
                                echo "========================================================="
                                echo cmp
                                try {
                                    sh """cd ${WORKSPACE}/${cmp} && sh ./build.sh"""
                                } catch(Exception e) {
                                    catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                                        error("build ${cmp} failed.")
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    post {
//        always {
//            cleanWs()
//        }
        failure {
            updateGitlabCommitStatus name: "build", state: "failed"
        }
        success {
            updateGitlabCommitStatus name: "build", state: "success"
        }
        unstable {
            updateGitlabCommitStatus name: "build", state: "failed"
        }
    }
}
