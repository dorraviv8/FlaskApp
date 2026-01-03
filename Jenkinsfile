pipeline {
  agent any

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Build') {
      steps {
        sh 'docker build -t dorraviv/my-flask-app:ci -f app/Dockerfile app'
      }
    }
  }
}

