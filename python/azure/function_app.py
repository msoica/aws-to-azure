import azure.functions as func
import json
import logging
import os
from azure.storage.blob import BlobServiceClient
from azure.storage.queue import QueueServiceClient

app = func.FunctionApp()

@app.route(route="http_trigger", auth_level=func.AuthLevel.ANONYMOUS)
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        # Retrieve the storage connection string from environment variables
        connection_string = os.getenv("AzureWebJobsStorage")
        logging.info(f'connection_string "{connection_string}" is ready.')
        if not connection_string:
            raise ValueError("AzureWebJobsStorage environment variable is not set.")

        # 1. Create a new container in Blob Storage
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_name = "test-container-python-4"
        container_client = blob_service_client.get_container_client(container_name)
        container_client.create_container()
        logging.info(f'Container "{container_name}" is ready.')

        # 2. Upload a file to Blob Storage
        blob_name = "example.txt"
        blob_client = container_client.get_blob_client(blob_name)
        file_content = "Hello from Azure Blob Storage!"
        blob_client.upload_blob(file_content, overwrite=True)
        logging.info(f'File "{blob_name}" uploaded to container "{container_name}".')

        # 3. Create a queue in Queue Storage
        queue_service_client = QueueServiceClient.from_connection_string(connection_string)
        queue_name = "test-queue"
        queue_client = queue_service_client.get_queue_client(queue_name)
        queue_client.create_queue()
        logging.info(f'Queue "{queue_name}" is ready.')

        # 4. Send a message to the queue
        message_content = "Hello from Azure Queue Storage!"
        queue_client.send_message(message_content)
        logging.info('Message sent to queue.')

        # 5. Receive messages from the queue
        messages = queue_client.receive_messages(messages_per_page=1)
        received_message = next(messages, None)
        if received_message:
            logging.info(f'Message received: {received_message.content}')
            queue_client.delete_message(received_message)
            logging.info('Message deleted from queue.')
        else:
            logging.info('No messages in queue.')

        return func.HttpResponse(
            json.dumps({"message": "Blob and Queue operations completed successfully."}),
            status_code=200
        )
    except ValueError as ve:
        logging.error(f'Configuration Error: {ve}')
        return func.HttpResponse(
            json.dumps({"message": "Configuration error.", "error": str(ve)}),
            status_code=500
        )
    except Exception as e:
        logging.error(f'Error: {e}')
        return func.HttpResponse(
            json.dumps({"message": "An error occurred.", "error": str(e)}),
            status_code=500
        )
