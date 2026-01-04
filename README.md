# Flask DevOps Project – Final Course Project

This repository contains a Flask-based application developed as a **final project for a DevOps course**.

The main goal of the project is to demonstrate **end-to-end DevOps practices**, including:
- Application containerization
- Kubernetes deployment
- Transition from raw Kubernetes manifests to Helm
- CI/CD automation with Jenkins
- Git-based development workflows

The application itself is intentionally simple in order to keep the focus on DevOps concepts.

---

## Application Overview

The Flask application exposes the following endpoints:

- `/` – Basic welcome endpoint
- `/health` – Health endpoint providing runtime and environment information

Example `/health` response:

```json
{
  "status": "healthy",
  "uptime_seconds": 215,
  "timestamp_utc": "2026-01-03T18:30:11Z",
  "hostname": "flaskapp-57cf7dc49-wr4jx",
  "environment": "dev",
  "version": "0.1.0",
  "python_version": "3.11"
}
```
The /health endpoint is used for:

Kubernetes liveness/readiness probes

Smoke testing in CI/CD pipelines

Operational visibility

# Project Structure
```text

FlaskApp
├── app
│   ├── app.py                     # Flask application source code
│   ├── requirements.txt           # Python dependencies
│   └── Dockerfile                 # Docker image definition
│
├── k8s                             # Raw Kubernetes manifests (learning stage)
│   ├── deployment.yaml             # Application Deployment
│   ├── service-NodePort.yaml       # NodePort Service
│   ├── hpa.yaml                    # Horizontal Pod Autoscaler
│   ├── configmap.yaml              # Configuration via ConfigMap
│   └── cronjob-ping.yaml           # Scheduled health-check CronJob
│
├── helm
│   └── FlaskApp                   # Helm chart for production deployment
│       ├── Chart.yaml              # Chart metadata
│       ├── values.yaml             # Default configuration values
│       ├── templates               # Kubernetes templates
│       │   ├── deployment.yaml     # Templated Deployment
│       │   ├── service.yaml        # Templated Service
│       │   ├── ingress.yaml        # (Optional) Ingress
│       │   ├── serviceaccount.yaml # ServiceAccount
│       │   ├── _helpers.tpl        # Template helpers (naming/labels)
│       │   └── tests
│       │       └── test-connection.yaml
│       └── .helmignore
│
├── Jenkinsfile                    # CI/CD pipeline definition
└── README.md
```
## Kubernetes Manifests (k8s/ directory) ##

The k8s directory contains raw Kubernetes YAML manifests created during the initial stage of the project.
These files represent a manual approach to Kubernetes deployment and were used to:
Learn Kubernetes resource definitions
Understand relationships between Deployment, Service, HPA, ConfigMap and CronJob
Validate application behavior before introducing Helm

Included resources:
Deployment – Defines application pods and replicas
NodePort Service – Exposes the application externally
HPA – Demonstrates autoscaling concepts
ConfigMap – Externalized configuration
CronJob – Periodic internal health checks

⚠️ These manifests are kept for learning and documentation purposes.
The production deployment is managed using Helm.

## Helm Chart (helm/FlaskApp) ##

The Helm chart represents the production-ready packaging of the application.

Purpose of Helm:
Parameterize Kubernetes manifests
Enable repeatable deployments
Simplify configuration changes without editing YAML files
Integrate seamlessly with CI/CD pipelines
Chart Components
Chart.yaml

Contains chart metadata such as:
Chart name
Version
Application version
values.yaml

Defines configurable values, including:
Docker image repository and tag
Service type and ports
Replica count
Environment variables
These values can be overridden during deployment or by CI/CD pipelines.

templates/
Contains templated Kubernetes manifests:
deployment.yaml – Application deployment with configurable image and replicas
service.yaml – Service definition (ClusterIP / NodePort)
serviceaccount.yaml – ServiceAccount definition
_helpers.tpl – Helper templates for consistent naming and labels
tests/test-connection.yaml – Helm test pod to verify service connectivity

Local Development
Run with Python (virtual environment)

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r app/requirements.txt
python app/app.py
```
Run with Docker
```sh
docker build -t dorraviv/my-flask-app:local -f app/Dockerfile app
docker run -p 5000:5000 dorraviv/my-flask-app:local
```

Kubernetes Deployment with Helm
```sh
helm upgrade --install flaskapp helm/FlaskApp \
  -n flaskapp --create-namespace
```
Access service using Minikube:
```sh
minikube service -n flaskapp flaskapp --url
```

CI/CD Pipeline (Jenkins)

The project includes a Jenkins pipeline defined in Jenkinsfile implementing:
Build – Docker image build with versioned tags
Test – Smoke test using /health endpoint
Push – Image push to Docker Hub
Deploy – Automated deployment using Helm
Each pipeline run deploys a new version of the application to Kubernetes.

Git Workflow

Development is performed on feature branches
Changes are merged into main
Git history demonstrates branching, merging and conflict resolution

Technologies Used:

Python 3.11
Flask 3.0
Docker
Kubernetes
Helm
Jenkins
Git / GitHub
