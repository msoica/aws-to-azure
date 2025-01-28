# Cloud Local Development Environment

This project demonstrates local cloud development with AWS (using LocalStack) and Azure (using Azurite). It includes examples for serverless functions, storage, and messaging services.

## Project Structure
```
├── node/
│ ├── aws/ # AWS Lambda examples and configurations
│ └── azure/ # Azure Functions examples and configurations
```

## Prerequisites

- [Homebrew](https://brew.sh/) (for macOS/Linux)
- [Node.js](https://nodejs.org/) (v18+ recommended)
- [npm](https://www.npmjs.com/) (comes with Node.js)

## Installation

### Core Tools
```bash
# Install AWS CLI and LocalStack
brew install awscli awscli-local localstack

# Install Azure Functions Core Tools
brew tap azure/functions
brew install azure-functions-core-tools@4

# Install Azurite (Azure storage emulator)
npm install -g azurite
```

## AWS Local Development (LocalStack)

### Start LocalStack
```
# Create bucket
awslocal s3api create-bucket --bucket test-bucket

# List buckets
awslocal s3api list-buckets

# Delete bucket
awslocal s3api delete-bucket --bucket test-bucket
```

### SQS Queue Operations
```
# Create queue
awslocal sqs create-queue --queue-name test-queue

# List queues
awslocal sqs list-queues

# Delete queue
awslocal sqs delete-queue --queue-url http://localhost:4566/000000000000/test-queue
```

### Lambda Functions
```
# Package function
cd node/aws
zip -r function.zip index.js node_modules

# Create Lambda function
awslocal lambda create-function \
    --function-name localstack-lambda-url-example \
    --runtime nodejs18.x \
    --zip-file fileb://function.zip \
    --handler index.handler \
    --role arn:aws:iam::000000000000:role/lambda-role

# List functions
awslocal lambda list-functions

# Invoke function
curl -X POST \
  http://localhost:4566/2015-03-31/functions/localstack-lambda-url-example/invocations \
  -d '{"body": "{\"num1\": \"10\", \"num2\": \"10\"}"}' \
  -H "Content-Type: application/json"

# Delete function
awslocal lambda delete-function --function-name localstack-lambda-url-example
```

### Quick Development Cycle
```
# Re-deploy function
awslocal lambda delete-function --function-name localstack-lambda-url-example
zip -r function.zip index.js node_modules
awslocal lambda create-function \
    --function-name localstack-lambda-url-example \
    --runtime nodejs18.x \
    --zip-file fileb://function.zip \
    --handler index.handler \
    --role arn:aws:iam::000000000000:role/lambda-role
```

## Quick Development Cycle

### Start Azurite
```
azurite --location ./azurite-data --debug ./azurite-debug.log
```

### Function Operations
```
# Create new function (from project root)
cd node/azure
func new

# Start functions host
func start
```
