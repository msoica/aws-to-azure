const AWS = require('aws-sdk');

// Configure AWS SDK to connect to LocalStack
const localstackConfig = {
    region: 'us-east-1',
    endpoint: 'http://host.docker.internal:4566',
    s3ForcePathStyle: true
};

// Initialize S3 and SQS clients
const s3 = new AWS.S3(localstackConfig);
const sqs = new AWS.SQS(localstackConfig);

exports.handler = async (event) => {
    try {
        // Example 1: Create a new S3 bucket
        const bucketName = 'test-bucket';
        await s3.createBucket({ Bucket: bucketName }).promise();
        console.log(`Bucket "${bucketName}" created successfully.`);

        // Example 2: Upload a file to S3
        const params = {
            Bucket: bucketName,
            Key: 'example.txt',
            Body: 'Hello from LocalStack!',
        };
        await s3.putObject(params).promise();
        console.log(`File uploaded to "${bucketName}/example.txt".`);

        // Example 3: Send a message to an SQS queue
        const queueName = 'test-queue';
        const { QueueUrl } = await sqs.createQueue({ QueueName: queueName }).promise();
        console.log(`Queue created: ${QueueUrl}`);

        const messageParams = {
            QueueUrl,
            MessageBody: 'Hello from SQS!',
        };
        await sqs.sendMessage(messageParams).promise();
        console.log('Message sent to SQS.');

        // Example 4: Receive messages from the SQS queue
        const receivedMessages = await sqs.receiveMessage({ QueueUrl, MaxNumberOfMessages: 1 }).promise();
        console.log('Messages received:', receivedMessages);

        return {
            statusCode: 200,
            body: JSON.stringify({
                message: 'S3 and SQS operations completed successfully.',
            }),
        };
    } catch (error) {
        console.error('Error:', error);
        return {
            statusCode: 500,
            body: JSON.stringify({
                message: 'An error occurred.',
                error: error.message,
            }),
        };
    }
};
