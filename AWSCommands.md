# Host Container on AWS

Assuming AWS CLI is installed => if not, browse https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html

## Create an ECS Cluster

Go to AWS Console → ECS → Clusters → Create Cluster 
And select Fargate, then click create.

## Store Your Docker Images in ECR

Before, check your **AWS Account ID** (In AWS Console, top and right corner) and your **region** (URL)

```bash
# Create the repository
aws ecr create-repository --repository-name bigdataqd --region us-east-1
# Keep the info retrieve here for next steps

# Log to Docker AWS services
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <Account_id>.dkr.ecr.us-east-1.amazonaws.com

# Go where your Dockerfile is located
cd BigData/NewApp

# Push the Container
docker build -t newapp .

docker tag newapp:latest <Account_id>.dkr.ecr.us-east-1.amazonaws.com/bigdataqd

docker push <Account_id>.dkr.ecr.us-east-1.amazonaws.com/bigdataqd
```

## Create a task definition

- Define a task definition in ECS
- Choose Fargate as the launch type
- Add your MongoDB & Django services (Use ECR images)
- Set the environment variables (MONGO_URL, DB credentials, etc.)

## Run Services in ECS

- Create an ECS Service linked to your task definition
- Configure a Load Balancer (optional)
- Set auto-scaling if needed

859897673753.dkr.ecr.us-east-1.amazonaws.com/mongo
docker pull mongo:latest
docker tag mongo:latest 859897673753.dkr.ecr.us-east-1.amazonaws.com/mongo
docker push 859897673753.dkr.ecr.us-east-1.amazonaws.com/mongo