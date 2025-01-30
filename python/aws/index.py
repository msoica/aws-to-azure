import json
import boto3

# Configure boto3 to connect to LocalStack
localstack_config = {
    "region_name": "us-east-1",
    "endpoint_url": "http://host.docker.internal:4566"
}

# Initialize S3 and SQS clients
s3 = boto3.client("s3", **localstack_config)
sqs = boto3.client("sqs", **localstack_config)

def lambda_handler(event, context):
    try:
        # Example 1: Create a new S3 bucket
        bucket_name = "test-bucket"
        s3.create_bucket(Bucket=bucket_name)
        print(f'Bucket "{bucket_name}" created successfully.')

        # Example 2: Upload a file to S3
        s3.put_object(Bucket=bucket_name, Key="example.txt", Body="Hello from LocalStack!")
        print(f'File uploaded to "{bucket_name}/example.txt".')

        # Example 3: Send a message to an SQS queue
        queue_name = "test-queue"
        response = sqs.create_queue(QueueName=queue_name)
        queue_url = response["QueueUrl"]
        print(f'Queue created: {queue_url}')

        message_params = {
            "QueueUrl": queue_url,
            "MessageBody": "Hello from SQS!"
        }
        sqs.send_message(**message_params)
        print("Message sent to SQS.")

        # Example 4: Receive messages from the SQS queue
        received_messages = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=1)
        print("Messages received:", received_messages)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "S3 and SQS operations completed successfully."
            })
        }
    except Exception as error:
        print("Error:", error)
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "An error occurred.",
                "error": str(error)
            })
        }
