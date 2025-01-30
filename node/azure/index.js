const { app } = require('@azure/functions');
const { BlobServiceClient } = require('@azure/storage-blob');
const { QueueServiceClient } = require('@azure/storage-queue');

app.http('my-test-api', {
    methods: ['GET', 'POST'],
    authLevel: 'anonymous',
    handler: async (request, context) => {
        try {
            // Retrieve your storage connection string from an environment variable.
            // In Azure Functions, typically it's in process.env.AzureWebJobsStorage by default.
            const connectionString = process.env.AzureWebJobsStorage;

            console.log(connectionString, 'connectionString')

            // 1. Create a new container in Blob Storage (equivalent to an S3 bucket)
            const blobServiceClient = BlobServiceClient.fromConnectionString(connectionString);
            const containerName = 'test-container';
            const containerClient = blobServiceClient.getContainerClient(containerName);

            await containerClient.createIfNotExists();
            context.log(`Container "${containerName}" is ready.`);

            // 2. Upload a file to Blob Storage (like uploading an object to S3)
            const blobName = 'example.txt';
            const blockBlobClient = containerClient.getBlockBlobClient(blobName);
            const fileContent = 'Hello from Azure Blob Storage!';
            await blockBlobClient.upload(fileContent, fileContent.length);
            context.log(`File "${blobName}" uploaded to container "${containerName}".`);

            // 3. Create a queue in Queue Storage (like creating an SQS queue)
            const queueServiceClient = QueueServiceClient.fromConnectionString(connectionString);
            const queueName = 'test-queue';
            const queueClient = queueServiceClient.getQueueClient(queueName);

            await queueClient.createIfNotExists();
            context.log(`Queue "${queueName}" is ready.`);

            // 4. Send a message to the queue (like sending an SQS message)
            const messageContent = 'Hello from Azure Queue Storage!';
            await queueClient.sendMessage(messageContent);
            context.log('Message sent to queue.');

            // 5. Receive messages from the queue (like receiving messages from SQS)
            const receiveResponse = await queueClient.receiveMessages({
                numberOfMessages: 1,
                visibilityTimeout: 30
            });

            if (receiveResponse.receivedMessageItems.length > 0) {
                const receivedMessage = receiveResponse.receivedMessageItems[0];
                context.log('Message received:', receivedMessage.messageText);

                // (Optional) Delete the message after processing
                await queueClient.deleteMessage(receivedMessage.messageId, receivedMessage.popReceipt);
                context.log('Message deleted from queue.');
            } else {
                context.log('No messages in queue.');
            }

            // Return an HTTP response
            return {
                status: 200,
                body: JSON.stringify({
                    message: 'Blob and Queue operations completed successfully.'
                })
            };
        } catch (error) {
            context.log.error('Error:', error);
            return {
                status: 500,
                body: JSON.stringify({
                    message: 'An error occurred.',
                    error: error.message
                })
            };
        }
    }
});
