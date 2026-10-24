# MiniPay DevOps Capstone

A tiny, runnable demonstration project for the Enterprise Payment & Notification Engine DevOps lab. It simulates payments; it does not connect to a bank or process real money.

## Components
- Flask backend: health, payment simulation, and notification-log endpoints.
- NGINX frontend: small web form; proxies `/api/` requests to the backend.
- Unit tests for API health, payment/notification creation, and invalid amounts.
- Dockerfiles and Docker Compose for local testing.
- Jenkins Declarative Pipeline.
- Kubernetes backend Deployment + ClusterIP Service, frontend Deployment + NodePort Service (`30099`).
- Terraform local-file resource and Ansible local validation playbook.

## Fast local run with Docker Compose
From this directory:
```bash
docker compose up --build -d
docker compose ps
```
Open `http://localhost:8080`, submit a demo payment, and check the health button.
Try API directly:
```bash
curl http://localhost:5000/api/health
curl -X POST http://localhost:5000/api/payments -H "Content-Type: application/json" -d "{\"customer\":\"Exam User\",\"amount\":125.50}"
curl http://localhost:5000/api/notifications
```
Stop:
```bash
docker compose down
```

## Tests without Docker
```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```

## Git task
Initialize only if the exam repo is not already initialized:
```bash
git init
git add .
git commit -m "feat: add MiniPay payment and notification demo"
git branch -M main
git checkout -b release-v1.0
echo v1.0-prod-bundle > version.txt
git add version.txt
git commit -m "chore: finalize release v1.0"
git checkout main
git merge release-v1.0
git tag -a v1.0.0-final -m "Final Capstone Release"
```
Set a remote URL supplied by your instructor before pushing:
```bash
git remote add origin <YOUR_REPOSITORY_URL>
git push -u origin main
git push origin release-v1.0
git push origin v1.0.0-final
```
If a repository/remote is already supplied, do not reinitialize it or replace its remote.

## Docker images
```bash
docker build -t minipay-backend:v1.0 .
docker build -t minipay-frontend:v1.0 ./frontend
docker run --rm -p 5000:5000 minipay-backend:v1.0
```
The backend container above stays running while the Flask server runs. Use Ctrl+C to stop it.

## Kubernetes
The manifests use local images and `imagePullPolicy: IfNotPresent`, suitable for a single-node cluster if those images are visible to the Kubernetes node. Build the images first:
```bash
docker build -t minipay-backend:v1.0 .
docker build -t minipay-frontend:v1.0 ./frontend
kubectl apply -f capstone-stack.yaml
kubectl get deployments,pods,services
kubectl rollout status deployment/payment-backend
kubectl rollout status deployment/payment-frontend
```
Open `http://localhost:30099` if the cluster exposes NodePort on localhost. If using a remote or multi-node cluster, push images to a registry your cluster can access, update image names in the YAML, and configure credentials if needed.

Clean up:
```bash
kubectl delete -f capstone-stack.yaml
```

## Terraform + Ansible
Run from this project directory (requires Terraform and Ansible):
```bash
terraform init
terraform validate
terraform plan
terraform apply -auto-approve
ansible-playbook -i localhost, -c local ansible-check.yml
```
Or use the professor's exact local command:
```bash
ansible localhost -m command -a "cat capstone.env" -c local
```

## Jenkins
The included `Jenkinsfile` assumes a Linux Jenkins agent with Python 3, pip, Docker CLI, and permission to access the Docker daemon. Configure the job to use this repository, then Build Now. Kubernetes is intentionally not applied from Jenkins by default: that requires configured cluster credentials/context. The pipeline checks that the manifest exists and prints a message rather than pretending to deploy.

## Exam caveats
- Jira must be completed in the instructor's Jira project/board; it cannot be performed from this repository.
- Never commit real secrets, API keys, payment details, or credentials.
- A `capstone.env` file created by Terraform only records configuration; it does not itself deploy or verify the Kubernetes service.
