pipeline {
  agent any

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Docker available?') {
      steps {
        sh 'docker --version'
      }
    }

    stage('Build image') {
      steps {
        sh 'docker build -t dorraviv/my-flask-app:ci -f app/Dockerfile app'
      }
    }
  }
}

