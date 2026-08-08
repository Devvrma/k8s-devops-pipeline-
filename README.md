# K8s DevOps Pipeline

A hands-on DevOps learning project that demonstrates an end-to-end workflow: two Flask microservices (**User Service** and **Auth Service**), a LocalStack-backed S3 bucket provisioned via **Terraform**, container images built with **Docker**, deployment to **Kubernetes**, and automation glued together with a **Jenkins** pipeline.

## Architecture

```
                ┌─────────────────┐        ┌──────────────────┐
                │  Auth Service    │        │   User Service    │
                │  (Flask, :5002)  │        │  (Flask, :5002)   │
                └────────┬─────────┘        └─────────┬─────────┘
                         │                              │
                         │        Kubernetes Cluster    │
                         └──────────────┬────────────────┘
                                        │
                                ┌───────▼────────┐
                                │   LocalStack     │
                                │  (fake AWS S3)   │
                                └────────────────┘

Terraform  →  provisions the S3 bucket on LocalStack
Jenkins    →  runs terraform apply, then kubectl apply on the K8s manifests
```

## Tech Stack

| Layer | Tool |
|---|---|
| Application | Python (Flask), boto3 |
| Containerization | Docker |
| Orchestration | Kubernetes |
| Infrastructure as Code | Terraform |
| Fake AWS Cloud | LocalStack (S3) |
| CI/CD | Jenkins |

## Project Structure

```
k8s-devops-pipeline-/
├── auth-service/
│   ├── auth.py            # Auth Service - login endpoint
│   └── Dockerfile
├── user-service/
│   ├── app.py              # User Service - user info + S3 upload endpoint
│   ├── upload_test.py       # Standalone script to test S3 upload via LocalStack
│   ├── requirements.txt
│   └── Dockerfile
├── K8s/
│   ├── auth-deployment.yaml
│   ├── auth-service.yaml
│   ├── user-deployement.yaml
│   ├── user-service-k8s.yaml
│   └── localstack-endpoint.yaml
├── Terraform/
│   └── main.tf              # Provisions the S3 bucket on LocalStack
├── docker-compose.yml       # Local dev setup (both services + LocalStack)
├── jenkinsfile               # CI/CD pipeline: Terraform apply → K8s deploy → verify
└── config.xml                 # Jenkins global configuration
```

## Services

### Auth Service (`auth-service/`)
Minimal Flask app with two routes:
- `GET /` – health check message
- `GET /login` – returns a mock login success response

### User Service (`user-service/`)
Flask app that talks to a LocalStack S3 bucket via `boto3`:
- `GET /user` – returns user info
- `GET /upload` – creates the bucket `my-devops-project-bucket` if missing and uploads a test file to it

## Getting Started

### Prerequisites
- Docker & Docker Compose
- kubectl + a local Kubernetes cluster (e.g. Minikube)
- Terraform
- Jenkins (optional, for the full CI/CD pipeline)

### 1. Run locally with Docker Compose

```bash
docker-compose up --build
```

This starts:
- `user-service` on `localhost:5002`
- `auth-service` on `localhost:5002` (note: both services currently share the same host port in `docker-compose.yml` — change one of the port mappings, e.g. `5001:5002`, if you want to run them side by side)
- `localstack` on `localhost:4566` (fake S3/IAM/Lambda)

### 2. Provision the S3 bucket with Terraform

```bash
cd Terraform
terraform init
terraform apply -auto-approve
```

This creates the `my-devops-project-bucket` bucket against the LocalStack endpoint.

### 3. Build images and deploy to Kubernetes

```bash
# Build images (Minikube example — build inside the cluster's Docker daemon)
eval $(minikube docker-env)
docker build -t my-user-service:v2 ./user-service
docker build -t my-auth-service:v1 ./auth-service

# Apply manifests
kubectl apply -f K8s/

# Check status
kubectl get pods
kubectl get svc
```

- `user-service` is exposed via a `LoadBalancer` service (`user-service-lb`) on port 80.
- `auth-service` is exposed via a `NodePort` service on `nodePort: 30008`.
- `localstack-endpoint.yaml` wires an in-cluster `Service`/`Endpoints` pointing at the host machine's LocalStack instance (default Minikube gateway IP).

### 4. CI/CD with Jenkins

The included `jenkinsfile` automates steps 2 and 3:

1. **Terraform Infra** – `terraform init` + `terraform apply` in `Terraform/`
2. **K8s Deployment** – `kubectl apply -f K8s/`
3. **Verify** – `kubectl get pods`

Point a Jenkins pipeline job at this repository and it will run the stages above (written for Windows agents via `bat`; swap to `sh` if running on a Linux agent).

## Notes

- LocalStack is used to simulate AWS S3 locally — no real AWS credentials or costs are involved (`test`/`test` dummy credentials).
- `imagePullPolicy: Never` is used in the deployments, so images must be built directly into your cluster's Docker daemon (see Minikube step above) rather than pulled from a registry.

## License

No license specified yet — add one if you plan to share or open-source this project.
