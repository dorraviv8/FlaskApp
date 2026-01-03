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

_______________________________________________________________________

## Overview

This project is a simple Flask-based web application.

The repository includes:
- Kubernetes manifests for deployment, service, autoscaling (HPA),
  configuration (ConfigMap), and a periodic health-check CronJob.

## Prerequisites

- Python 3.10+
- Docker and Docker Compose installed
- A running Kubernetes cluster (local `minikube` or any other cluster)
- `kubectl` configured to talk to your cluster
- Metrics server installed in the cluster (required for HPA)

# How to Run Locally (Without Docker)
1.Navigate to the application folder:

```bash
cd FlaskApp/app

2.Install dependencies:
   pip install -r requirements.txt

3. Run the app:
   python app.py

4. Access the application:
   Open http://localhost:5000 in your browser.

# Run with Docker
1. Build and run using Docker Compose:
   docker build -t flask-app:latest .

2.Run the container
  docker run -p 5000:5000 flask-app:latest

3. Access the app:
   Visit http://localhost:5000

#Running with Docker Compose:
1. From the app directory:
   docker compose up --build

2. open http://localhost:5000


#Kubernetes
The k8s folder includes basic manifest files for practicing:

- Deployment
- NodePort Service
- Horizontal Pod Autoscaler (hpa)
- ConfigMap
- CronJob

To apply all resources:

cd FlaskApp/k8s
kubectl apply -f .

# Technologies Used
- Python 3.11
- Flask 3.0
- Docker
- Docker Compose
- Kubernetes

# Notes
- Default port: 5000
- The Flask app runs automatically on container startup.
- To stop the container:
  docker compose down

# Example Output
Hello, World!

