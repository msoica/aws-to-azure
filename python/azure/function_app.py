import azure.functions as func
import json
import logging
import os
from azure.storage.blob import BlobServiceClient, ContainerClient
from azure.storage.queue import QueueServiceClient, QueueClient

app = func.FunctionApp()

@app.route(route="http_trigger", auth_level=func.AuthLevel.ANONYMOUS)
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        # Retrieve the storage connection string from environment variables
        connection_string = os.getenv("AzureWebJobsStorage")
        if not connection_string:
            raise ValueError("AzureWebJobsStorage environment variable is not set.")

        # Append development storage endpoints
        blob_connection_string = connection_string + "BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
        queue_connection_string = connection_string + "QueueEndpoint=http://127.0.0.1:10001/devstoreaccount1;"

        # 1. Create a new container in Blob Storage (if it doesn't exist)
        blob_service_client = BlobServiceClient.from_connection_string(blob_connection_string)
        container_name = "test-container"
        container_client = blob_service_client.get_container_client(container_name)

        try:
            container_client.create_container()
            logging.info(f'Container "{container_name}" created.')
        except Exception as e:
            logging.info(f'Container "{container_name}" already exists. Continuing...')

        # 2. Upload a file to Blob Storage
        blob_name = "example.txt"
        blob_client = container_client.get_blob_client(blob_name)
        file_content = "Hello from Azure Blob Storage!"
        blob_client.upload_blob(file_content, overwrite=True)
        logging.info(f'File "{blob_name}" uploaded to container "{container_name}".')

        # 3. Create a queue in Queue Storage (if it doesn't exist)
        queue_service_client = QueueServiceClient.from_connection_string(queue_connection_string)
        queue_name = "test-queue"
        queue_client = queue_service_client.get_queue_client(queue_name)

        try:
            queue_client.create_queue()
            logging.info(f'Queue "{queue_name}" created.')
        except Exception as e:
            logging.info(f'Queue "{queue_name}" already exists. Continuing...')

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
