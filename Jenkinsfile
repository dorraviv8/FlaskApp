pipeline {
  agent any

  environment {
    IMAGE_REPO = "dorraviv/my-flask-app"
    NAMESPACE  = "flaskapp"
    RELEASE    = "flaskapp"
    CHART_DIR  = "helm/FlaskApp"
  }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Build image') {
      steps {
        sh '''
          docker build -t ${IMAGE_REPO}:${BUILD_NUMBER} -f app/Dockerfile app
          docker tag ${IMAGE_REPO}:${BUILD_NUMBER} ${IMAGE_REPO}:latest
        '''
      }
    }

    stage('Test (smoke)') {
      steps {
        sh '''
          CID=$(docker run -d -p 5005:5000 ${IMAGE_REPO}:${BUILD_NUMBER})
          sleep 2
          curl -fsS http://127.0.0.1:5005/health > /dev/null
          docker rm -f $CID
        '''
      }
    }

    stage('Push image') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
          sh '''
            echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
            docker push ${IMAGE_REPO}:${BUILD_NUMBER}
            docker push ${IMAGE_REPO}:latest
          '''
        }
      }
    }

    stage('Deploy (Helm)') {
      steps {
        sh '''
          helm upgrade --install ${RELEASE} ${CHART_DIR} \
            -n ${NAMESPACE} --create-namespace \
            --set image.repository=${IMAGE_REPO} \
            --set image.tag=${BUILD_NUMBER} \
            --set image.pullPolicy=Always

          kubectl -n ${NAMESPACE} rollout status deployment/${RELEASE} --timeout=180s
        '''
      }
    }
  }
}

