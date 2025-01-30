# Cloud Local Development Environment - Node.js

This project demonstrates local cloud development using AWS (LocalStack) and Azure (Azurite) with **Node.js**. It includes examples for serverless functions, storage, and messaging services.

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

** NOTE for windows we can use choco instead of bre

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
zip -r function.zip index.js node_modules

awslocal lambda create-function     --function-name localstack-lambda-url-example     --runtime nodejs18.x     --zip-file fileb://function.zip     --handler index.handler     --role arn:aws:iam::000000000000:role/lambda-role

awslocal lambda list-functions
awslocal lambda delete-function --function-name localstack-lambda-url-example

curl -X POST   http://localhost:4566/2015-03-31/functions/localstack-lambda-url-example/invocations   -d '{"body": "{"num1": "10", "num2": "10"}"}'   -H "Content-Type: application/json"
```

## Azure Local Development (Azurite)
```bash
azurite --location ./azurite-data --debug ./azurite-debug.log
cd node/azure
func new
func start
```
