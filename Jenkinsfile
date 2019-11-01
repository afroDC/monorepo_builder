pipeline {
  agent none
    options {
        skipDefaultCheckout true
    }
    stages {
        stage('Checkout repo') {
            steps {
                checkout scm
            }
        }
        stage('Determine projects to build') {
            steps {
                script {
                    if (env.CHANGE_TARGET) {
                        // For PR's compare the working branch against the merge branch. CHANGE_TARGET is the merge branch variable.
                        // CHANGE_TARGET only exists as a variable if the job is a PR.
                        sh "python automation/monorepo_builder.py remotes/origin/${CHANGE_TARGET} && cat changes"
                    } else {
                        // For merges post PR, we just want to compare HEAD to HEAD~1 (Latest versus Latest-1)
                        sh "python automation/monorepo_builder.py HEAD~1  && cat changes"
                    }
                }
            }
        }
        // Build projects
        stage('Build example a') {
            when {
                expression {
                    // TODO: Write an external function that does this better. This doesn't work without specifics.
                    return readFile('changes').contains('a')
                }
            }
            steps {
                sh "make build-example-a"
            }
        }
        stage('Build example b') {
            when {
                expression {
                    return readFile('changes').contains('b')
                }
            }
            steps {
                sh "make build-repo"
            }
        }
        // Test projects
        stage('Test example a') {
            when {
                expression {
                    return readFile('changes').contains('a')
                }
            }
            steps {
                sh "make test-example-a"
            }
        }
        stage('Test example b') {
            when {
                expression {
                    return readFile('changes').contains('b')
                }
            }
            steps {
                sh "make test-example-b"
            }
        }
        // Upload projects
        stage('Upload example a') {
            when {
                allOf {
                    branch 'master'
                    expression {
                        return readFile('changes').contains('a')
                    }
                }
            }
            steps {
                sh "make upload-example-a"
            }
        }
        stage('Upload example b') {
            when {
                allOf {
                    branch 'master'
                    expression {
                        return readFile('changes').contains('b')
                    }
                }
            }
            steps {
                sh "make upload-example-b"
            }
        }
        // Deploy projects
        stage('Deploy example a') {
            when {
                allOf {
                    branch 'master'
                    expression {
                        return readFile('changes').contains('a')
                    }
                }
            }
            steps {
                sh "make deploy-example-a"
            }
        }
        stage('Deploy example b') {
            when {
                allOf {
                    branch 'master'
                    expression {
                        return readFile('changes').contains('b')
                    }
                }
            }
            steps {
                sh "make deploy-example-b"
            }
        }
    }
    // Post actions
    post {
        success {
            slackSend (color: 'good', message: "SUCCESS: <${env.BUILD_URL}|${env.JOB_NAME}>")
        }
        failure {
            slackSend (color: 'danger', message: "FAILURE: <${env.BUILD_URL}|${env.JOB_NAME}>")
        }
    }
}