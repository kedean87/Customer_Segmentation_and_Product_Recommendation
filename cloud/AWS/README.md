# E-Commerce Recommendation & Segmentation - AWS Fargate Deployment

This repository contains the **AWS Fargate deployment** for the E-Commerce Customer Segmentation & Recommendation Engine. It focuses on containerizing the service, deploying to Fargate, and exposing an API for predictions.

---

## 1. Overview

The AWS deployment consists of:

- **Dockerized Flask API** for product recommendations.
- **Pre-trained models** loaded at startup (no training on Fargate to avoid memory issues).
- **ECS Fargate task** running the container with public IP access.
- **Security group and subnet configuration** to allow HTTP access for testing.

---

## 2. Deployment Steps

### **Important Note**
- you must run `cd src` and then `python main.py` in order to generate the files needed to make the prediction in the docker container environment ( cannot train models and generate data on ECS/Fargate, it must be loaded or it will exceed memory limits and fail during deployment )

### Step 1: Build and Push Docker Image to ECR
```bash
# Build Docker Image
export DOCKER_BUILDKIT=1                            
docker buildx build --provenance=false --output type=docker --platform linux/amd64 -t ecommerce-recommendation:latest .

# Create ECR repository
aws ecr create-repository --repository-name ecommerce-recommendation --region us-east-2

# Authenticate Docker to ECR
aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-2.amazonaws.com

# Tag Docker image
docker tag ecommerce-image:latest <account-id>.dkr.ecr.us-east-2.amazonaws.com/ecommerce-recommendation:latest

# Push image to ECR
docker push <account-id>.dkr.ecr.us-east-2.amazonaws.com/ecommerce-recommendation:latest
```

### Step 2: Create ECS Task Execution Role
- Required for Fargate tasks to pull images from ECR.
- Use IAM console or CLI to attach `AmazonECSTaskExecutionRolePolicy`.
- Reference the role ARN in your task definition.

### Step 3: Create ECS Task Definition
- Specify:
  - Container name & image URI
  - CPU & memory
  - Port mappings (e.g., 8080)
  - Task execution role
  - Fargate launch type

### Step 4: Run ECS Fargate Task
```bash
# Find Subnet
aws ec2 describe-subnets --query "Subnets[*].[SubnetId, AvailabilityZone, CidrBlock]" --output table

# Find Subgroup
ws ec2 describe-security-groups --query "SecurityGroups[*].[GroupName,GroupId,Description,VpcId]" --output table

aws ecs run-task \
    --cluster ecommerce-cluster \
    --task-definition ecommerce-task \
    --launch-type FARGATE \
    --enable-execute-command \
    --network-configuration "awsvpcConfiguration={subnets=[subnet-xxxxxxx],securityGroups=[sg-xxxxxxx],assignPublicIp=ENABLED}"
```
- Ensure the subnet is public and the security group allows inbound traffic on port 8080.

### Step 5: Test the API
```bash
curl -X POST http://<public-ip>:8080/predict \
-H "Content-Type: application/json" \
-d '{"query": "CANDLES"}'
```
- Returns JSON with recommended products.
- Ensure container is running and public IP is accessible.

---

## 3. Common Issues And Solutions

| Problem | Solution |
|---------|---------|
| Container exits with Exit code 137 | Pre-train model locally and load it; increase memory if needed. |
| Execute command not working | Enable `--enable-execute-command` and attach valid ECS task role. |
| Security group restrictions | Update inbound rule to allow TCP traffic from `0.0.0.0/0` for testing. |
| Cannot access API | Ensure container has public IP, subnet is public, and Fargate task is running. |

---

## $. Notes
- This deployment avoids training on Fargate, only serving predictions.
- Docker container includes all dependencies for Flask API, pre-trained models, and recommendation logic.
- CI/CD can trigger deployment via AWS CLI commands.
