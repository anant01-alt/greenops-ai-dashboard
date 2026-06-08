from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import pandas as pd
import os

load_dotenv()

connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
container_name = os.getenv("CONTAINER_NAME")
blob_name = os.getenv("BLOB_NAME")

blob_service_client = BlobServiceClient.from_connection_string(
    connection_string
)

blob_client = blob_service_client.get_blob_client(
    container=container_name,
    blob=blob_name
)

download_path = "data/downloaded_cloud_usage.csv"

with open(download_path, "wb") as file:
    file.write(blob_client.download_blob().readall())

df = pd.read_csv(download_path)

print("Dataset loaded from Azure!")
print(df.head())
print("\nRows:", len(df))