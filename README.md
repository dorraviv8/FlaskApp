# Flask DevOps Project – Final Course Project

This repository contains a Flask-based Application developed as a **final project for a DevOps course**.

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

Learn Kubernetes resource definitions,Understand relationships between Deployment, Service, HPA, ConfigMap and CronJob

Validate application behavior before introducing Helm

### Included resources: ###

Deployment – Defines application pods and replicas

NodePort Service – Exposes the application externally

HPA – Demonstrates autoscaling concepts

ConfigMap – Externalized configuration

CronJob – Periodic internal health checks

⚠️ These manifests are kept for learning and documentation purposes.
The production deployment is managed using Helm.

## Helm Chart (helm/FlaskApp) ##

The Helm chart represents the production-ready packaging of the application.

### Purpose of Helm: ###

Parameterize Kubernetes manifests

Enable repeatable deployments

Simplify configuration changes without editing YAML files

Integrate seamlessly with CI/CD pipelines

Chart Components

### Chart.yaml ###

Contains chart metadata such as:

Chart name

Version

Application version

### values.yaml ###

Defines configurable values, including:

Docker image repository and tag

Service type and ports

Replica count

Environment variables

These values can be overridden during deployment or by CI/CD pipelines.

### templates/ ###

Contains templated Kubernetes manifests:

deployment.yaml – Application deployment with configurable image and replicas

service.yaml – Service definition (ClusterIP / NodePort)

serviceaccount.yaml – ServiceAccount definition

_helpers.tpl – Helper templates for consistent naming and labels

tests/test-connection.yaml – Helm test pod to verify service connectivity

## Local Development ##
Run with Python (virtual environment)

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r app/requirements.txt
python app/app.py
```
## Run with Docker ##
```sh
docker build -t dorraviv/my-flask-app:local -f app/Dockerfile app
docker run -p 5000:5000 dorraviv/my-flask-app:local
```

## Kubernetes Deployment with Helm ##
```sh
helm upgrade --install flaskapp helm/FlaskApp \
  -n flaskapp --create-namespace
```
Access service using Minikube:
```sh
minikube service -n flaskapp flaskapp --url
```
## CI/CD Pipeline (Jenkins + GitHub Webhook) ##

The project includes a fully automated CI/CD pipeline implemented using Jenkins.
The pipeline is defined declaratively in the Jenkinsfile located at the root of the repository.

The pipeline covers the full lifecycle of the application:
build → test → package → deploy → verify.

### Pipeline Stages ###
### 1. Source Checkout ###

Jenkins pulls the latest code from the Git repository.

The pipeline always runs against the main branch.

### 2. Pre-checks (Validation) ###

Python syntax validation using py_compile to catch errors early.

Helm validation using:

helm lint – validates chart structure and best practices

helm template – renders Kubernetes manifests to ensure they are syntactically correct

These checks prevent invalid code or Helm charts from progressing further in the pipeline.

### 3. Build Docker Image ###

A Docker image is built using the application Dockerfile.

The image is tagged with:

The Jenkins build number (immutable version)

latest (convenience tag)

### 4. Container Tests (Smoke & Health Checks) ###

The container is started locally by Jenkins.

The pipeline validates:

/ endpoint returns the expected response

/health endpoint responds successfully

/health returns valid JSON containing required fields:

status

uptime_seconds

hostname

environment

version

python_version

This ensures the container is functional before pushing it to the registry.

### 5. Push Image to Docker Hub ###

Jenkins authenticates to Docker Hub using stored credentials.

Both the versioned image and latest tag are pushed to the registry.

### 6. Deploy to Kubernetes (Helm) ###

Jenkins deploys the application using Helm:

helm upgrade --install

The Docker image tag is injected dynamically using the Jenkins build number.

Jenkins waits for the Kubernetes rollout to complete successfully.

### 7. Post-deployment Validation ###

Jenkins performs a runtime validation after deployment.

Using port-forwarding, Jenkins verifies the /health endpoint of the running Kubernetes service.

This confirms that the application is healthy inside the cluster, not just locally.

Automatic Pipeline Trigger with GitHub Webhook

The Jenkins pipeline is triggered automatically on every git push using a GitHub Webhook.

Since Jenkins runs locally, ngrok is used to expose Jenkins to the internet.

Jenkins listens for GitHub webhook events at:
https://<ngrok-url>/github-webhook/

GitHub is configured to send push events to this endpoint.

Each push automatically triggers the Jenkins pipeline without manual intervention.

This setup ensures:

Continuous Integration on every code change

Automated deployment to Kubernetes

Immediate feedback on build, test, or deployment failures

## Git Workflow ##

Development follows a Git-based workflow:

Development is performed on feature branches

Changes are merged into the main branch

Each push to main automatically triggers the Jenkins CI/CD pipeline

Git history demonstrates:

Branching

Merging

Conflict resolution


## Technologies Used: ##

Python 3.11

Flask 3.0

Docker

Kubernetes

Helm

Jenkins

Git / GitHub

Ngrok
