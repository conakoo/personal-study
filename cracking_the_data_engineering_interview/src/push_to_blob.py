import os
from io import BytesIO

import pyarrow as pa
import pyarrow.parquet as pq
from azure.storage import blob

import scrape

functions = [
    scrape.league_table,
    scrape.top_scorers,
]

# blob storage configuration
CONNECTION_STRING = os.getenv("BLOB_CONNECTION_STRING")
CONTAINER_NAME = os.getenv("BLOB_CONTAINER_NAME")


def to_blob(func):
    """Converts the output of a given function to Parquet format and uploads it to Azure Blob Storage.

    Args:
        func (function): The function that retrieves data to be processed and uploaded.
    Returns:
        None

    This function takes a provided function, calls it to obtain data, and then converts the data into
    an Arrow Table. The Arrow Table is serialized into Parquet format and uploaded to an Azure Blob
    Storage container specified in the function. The function's name is used as the blob name.

    Example:
        Consider the function "top_scorers". Calling "to_blob(top_scorers)" will process the output
        of "top_scorers", convert it to Parquet format, and upload it to Azure Blob Storage.
    """

    file_name = func.__name__
    func = func()

    # Convert DataFrame to Arrow Table
    table = pa.Table.from_pandas(func)

    parquet_buffer = BytesIO()
    pq.write_table(table, parquet_buffer)
    client = blob.BlobServiceClient.from_connection_string(CONNECTION_STRING)
    container_client = client.get_container_client(CONTAINER_NAME)

    blob_name = f"{file_name}.parquet"
    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(parquet_buffer.getvalue(), overwrite=True)
    print(f"{blob_name} successfully updated")


for items in functions:
    to_blob(items)
