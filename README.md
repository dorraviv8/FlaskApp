# Flask Hello World App

This is a simple Python Flask application that returns a "Hello, World!" message when accessed.

# Project Structure
```text

FlaskApp
├── app
│   ├── app.py                        # Main Flask application
│   ├── requirements.txt              # Python dependencies
│   ├── Dockerfile                    # Docker image build instructions
│   ├── docker-compose.yml            # Docker Compose configuration
│   └── README.md                     # Project documentation
│
└── k8s
    ├── deployment.yaml               # Deployment for the Flask app
    ├── service-NodePort.yaml         # Service exposing the app
    ├── hpa.yaml                      # Horizontal Pod Autoscaler config
    ├── configmap.yaml                # ConfigMap for configs/env
    └── cronjob-ping.yaml             # CronJob for scheduled tasks

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

2. Run the app:
   python app.py

3. Access the application:
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

