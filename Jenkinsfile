pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Build & Test') {
            steps {
                sh 'python3 -m pip install -r requirements.txt'
                sh 'python3 -m unittest discover -s tests -v'
            }
        }
        stage('Docker Packaging') {
            steps {
                sh 'docker build -t minipay-backend:v1.0 .'
                sh 'docker build -t minipay-frontend:v1.0 ./frontend'
            }
        }
        stage('Kubernetes Manifest Validation') {
            steps {
                sh 'test -f capstone-stack.yaml'
                sh 'echo "Manifest file found; apply it in the configured Kubernetes environment."'
            }
        }
    }
}
