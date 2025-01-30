# Cloud Local Development Environment - Python

This project demonstrates local cloud development using AWS (LocalStack) and Azure (Azurite) with **Python**. It includes examples for serverless functions, storage, and messaging services.

## RENAME ME local.settings.json_ to local.settings.json

## Project Structure
```
├── python/
│ ├── aws/ # AWS Lambda examples and configurations
│ └── azure/ # Azure Functions examples and configurations
```

## Prerequisites

- [Homebrew](https://brew.sh/) (for macOS/Linux)
- [Python 3.8+](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/)
- [venv](https://docs.python.org/3/library/venv.html) (for virtual environments)

## Installation

### Core Tools
```bash
# Install AWS CLI and LocalStack
brew install awscli awscli-local localstack azure-cli

# Install Azure Functions Core Tools
brew tap azure/functions
brew install azure-functions-core-tools@4

# Install Azurite (Azure storage emulator)
npm install -g azurite
```

## AWS Local Development (LocalStack)

### Start LocalStack
```bash
localstack start
```

### Create and Manage S3 Buckets
```bash
awslocal s3api create-bucket --bucket test-bucket
awslocal s3api list-buckets
awslocal s3api delete-bucket --bucket test-bucket
```

### Create and Manage SQS
```bash
awslocal sqs create-queue --queue-name test-queue
awslocal sqs list-queues
awslocal sqs delete-queue --queue-url http://localhost:4566/000000000000/test-queue
```

### Lambda Functions
```bash
zip -r function.zip index.py

awslocal lambda create-function     --function-name localstack-lambda-url-example     --runtime python3.8     --role arn:aws:iam::000000000000:role/lambda-role     --handler index.lambda_handler     --zip-file fileb://function.zip

awslocal lambda list-functions
awslocal lambda delete-function --function-name localstack-lambda-url-example

curl -X POST   http://localhost:4566/2015-03-31/functions/localstack-lambda-url-example/invocations   -d '{"body": "{"num1": "10", "num2": "10"}"}'   -H "Content-Type: application/json"
```

## Azure Local Development (Azurite)
```bash
azurite --location ./azurite-data --debug ./azurite-debug.log
cd python/azure
func new # for creating a new function
func start # for running the function
func start --port PORT_NUMBER # for running the function on specific port
```

### Install Dependencies for AWS Lambda in Python
```bash
python -m venv venv
source venv/bin/activate # macOS
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

** NOTE use python < 3.11

### Install Dependencies for Azure Functions in Python
```bash
python -m venv venv
source venv/bin/activate # macOS
venv\Scripts\activate  # Windows
pip install -r requirements.txt


# For macOS (M1/M2/M3)
pip uninstall grpcio grpcio-tools -y
arch -x86_64 /usr/bin/python3 -m pip install --no-cache-dir --force-reinstall grpcio grpcio-tools
```