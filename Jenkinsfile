pipeline {
  agent any

  options {
    timestamps()
    disableConcurrentBuilds()
  }

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

    stage('Pre-checks (Python + Helm)') {
      steps {
        sh '''
          set -euo pipefail

          echo "== Python syntax check =="
          python3 -m py_compile app/app.py

          echo "== Helm lint =="
          helm lint ${CHART_DIR}

          echo "== Helm render (template) =="
          helm template ${RELEASE} ${CHART_DIR} -n ${NAMESPACE} > /tmp/rendered.yaml
          test -s /tmp/rendered.yaml
        '''
      }
    }

    stage('Build image') {
      steps {
        sh '''
          set -euo pipefail
          docker build -t ${IMAGE_REPO}:${BUILD_NUMBER} -f app/Dockerfile app
          docker tag ${IMAGE_REPO}:${BUILD_NUMBER} ${IMAGE_REPO}:latest
        '''
      }
    }

    stage('Test (container endpoints)') {
      steps {
        sh '''
          set -euo pipefail

          # Run container
          CID=$(docker run -d -p 5005:5000 ${IMAGE_REPO}:${BUILD_NUMBER})

          # Always cleanup
          cleanup() { docker rm -f "$CID" >/dev/null 2>&1 || true; }
          trap cleanup EXIT

          # Wait a moment for app to start
          for i in $(seq 1 15); do
            if curl -fsS http://127.0.0.1:5005/health >/dev/null 2>&1; then
              break
            fi
            sleep 1
          done

          echo "== Check / =="
          curl -fsS http://127.0.0.1:5005/ | grep -q "Hello, World!"

          echo "== Check /health returns required fields =="
          python3 - <<'PY'
import json, urllib.request
data = urllib.request.urlopen("http://127.0.0.1:5005/health").read().decode("utf-8")
j = json.loads(data)
required = ["status","uptime_seconds","timestamp_utc","hostname","environment","version","python_version"]
missing = [k for k in required if k not in j]
assert not missing, f"Missing keys: {missing}"
assert j["status"] == "healthy"
assert isinstance(j["uptime_seconds"], int)
print("Health JSON OK:", j)
PY
        '''
      }
    }

    stage('Push image') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
          sh '''
            set -euo pipefail
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
          set -euo pipefail

          helm upgrade --install ${RELEASE} ${CHART_DIR} \
            -n ${NAMESPACE} --create-namespace \
            --set image.repository=${IMAGE_REPO} \
            --set image.tag=${BUILD_NUMBER} \
            --set image.pullPolicy=Always

          kubectl -n ${NAMESPACE} rollout status deployment/${RELEASE} --timeout=180s
        '''
      }
    }

    stage('Post-deploy check (port-forward)') {
      steps {
        sh '''
          set -euo pipefail

          # Port-forward service locally and hit /health
          kubectl -n ${NAMESPACE} port-forward svc/${RELEASE} 5099:5000 >/tmp/pf.log 2>&1 &
          PF_PID=$!

          cleanup() { kill $PF_PID >/dev/null 2>&1 || true; }
          trap cleanup EXIT

          # Wait for port-forward
          for i in $(seq 1 10); do
            if curl -fsS http://127.0.0.1:5099/health >/dev/null 2>&1; then
              break
            fi
            sleep 1
          done

          curl -fsS http://127.0.0.1:5099/health > /dev/null
          echo "Post-deploy /health OK"
        '''
      }
    }
  }

  post {
    always {
      sh '''
        docker logout >/dev/null 2>&1 || true
      '''
    }
  }
}

