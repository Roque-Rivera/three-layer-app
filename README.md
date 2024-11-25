# Three-Layer App

This is a three-layer application deployed on AWS infrastructure using Terraform.

## Architecture

The application is deployed on AWS with the following components:

- Application Load Balancer (ALB) in front of web server instances
- Network Load Balancer (NLB) in front of Flask application instances
- RDS MySQL database
- VPC with public, private, and database subnets
- Auto Scaling Groups for both web and API servers
- S3 bucket for centralized logging
- AWS Secrets Manager for credential management

### Components

1. Frontend (Presentation Layer)

   - Static HTML/JavaScript served from EC2 instances
   - Hosted behind Application Load Balancer
   - Auto-scales based on demand
   - Automatically configured during instance launch

2. Backend (Application Layer)

   - Python Flask REST API
   - Runs on EC2 instances in private subnet
   - Load balanced using Network Load Balancer
   - Managed by Supervisor for reliability
   - Auto-scales based on demand

3. Database (Data Layer)
   - RDS MySQL database
   - Hosted in dedicated database subnet
   - Credentials managed through AWS Secrets Manager

## Deployment Instructions

### 1. Prerequisites

1. Install required tools:

   ```bash
   # Install AWS CLI
   curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
   unzip awscliv2.zip
   sudo ./aws/install

   # Install Terraform
   curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
   sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
   sudo apt-get update && sudo apt-get install terraform
   ```

2. Configure AWS credentials:
   ```bash
   aws configure
   ```

### 2. Repository Setup

1. Clone this repository:

   ```bash
   git clone <your-repo-url>
   cd three-layer-app
   ```

2. Update the repository URL in `terraform/terraform.tfvars`:
   ```hcl
   repo_url = "https://github.com/your-username/three-layer-app.git"
   ```

### 3. AWS Secrets Manager Setup

1. Create secrets for database credentials:

   ```bash
   # Create username secret
   aws secretsmanager create-secret \
       --name "/prod/database/username" \
       --secret-string "admin"

   # Create password secret
   aws secretsmanager create-secret \
       --name "/prod/database/password" \
       --secret-string "your-secure-password"
   ```

### 4. Terraform Deployment

1. Navigate to the Terraform directory:

   ```bash
   cd terraform
   ```

2. Initialize Terraform:

   ```bash
   terraform init
   ```

3. Review the deployment plan:

   ```bash
   terraform plan
   ```

4. Apply the configuration:

   ```bash
   terraform apply
   ```

5. Note the outputs:
   ```bash
   terraform output
   ```

### 5. Verify Deployment

1. Access the frontend:

   - Open the ALB DNS name in your browser
   - Should see the Items Manager interface

2. Test the API:

   ```bash
   # Get all items
   curl http://<nlb-dns-name>:5000/api/items

   # Create a new item
   curl -X POST \
        -H "Content-Type: application/json" \
        -d '{"name":"Test Item","description":"Test Description"}' \
        http://<nlb-dns-name>:5000/api/items
   ```

## Infrastructure Management

### Scaling

The application automatically scales based on:

- CPU utilization
- Network traffic
- Request count

Auto Scaling Groups are configured with:

- Minimum: 1 instance
- Desired: 2 instances
- Maximum: 4 instances

### Monitoring

1. CloudWatch Metrics:

   ```bash
   aws cloudwatch get-metric-statistics \
       --namespace AWS/EC2 \
       --metric-name CPUUtilization \
       --dimensions Name=AutoScalingGroupName,Value=<asg-name> \
       --start-time $(date -u +"%Y-%m-%dT%H:%M:%SZ" -d "1 hour ago") \
       --end-time $(date -u +"%Y-%m-%dT%H:%M:%SZ") \
       --period 300 \
       --statistics Average
   ```

2. Application Logs:
   ```bash
   # View logs in S3
   aws s3 ls s3://${environment}-app-logs-${suffix}/
   ```

### Maintenance

1. Update Application Code:

   - Push changes to your repository
   - The instances will pull updates on next launch

2. Database Maintenance:
   ```bash
   # Connect to RDS
   mysql -h <rds-endpoint> -u admin -p
   ```

## Troubleshooting

### Common Issues

1. Deployment Failures:

   ```bash
   # View detailed plan
   terraform plan -out=tfplan
   terraform show tfplan
   ```

2. Instance Issues:

   ```bash
   # Check instance logs
   aws ec2 get-console-output --instance-id <instance-id>
   ```

3. Database Connectivity:
   ```bash
   # Test database connection
   telnet <rds-endpoint> 3306
   ```

## Cleanup

To destroy the infrastructure:

```bash
terraform destroy
```

## Security Notes

1. Access Control

   - All instances use IAM roles
   - Secrets managed through AWS Secrets Manager
   - Network segmentation with public/private subnets

2. Network Security

   - Web servers only accept traffic from ALB
   - API servers only accept traffic from within VPC
   - Database only accessible from API servers

3. Monitoring
   - CloudWatch metrics enabled
   - VPC Flow Logs enabled
   - S3 access logging enabled
