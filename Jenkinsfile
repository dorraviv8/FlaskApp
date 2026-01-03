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
        stage('Test (smoke)') {
      steps {
        sh '''
          CID=$(docker run -d -p 5005:5000 dorraviv/my-flask-app:ci)
          sleep 2
          curl -fsS http://127.0.0.1:5005/health > /dev/null
          docker rm -f $CID
        '''
      }
    }
  }
}

