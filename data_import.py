# Load packages
import pandas as pd
import os
from pathlib import Path



# Import file based on file name

# Define your file name pattern
fileName = 'file'
# define your directory
mydir = Path(os.getcwd())
data = pd.DataFrame() # create an empty data frame
# for each file in the directory, if the file name contains the file name pattern, read the file and append it to the data frame
# assuming you only have one file that matches the pattern, it will be the only file in the data frame
for file in mydir.glob(f'*{fileName}*' + '.csv'):
    newData = pd.read_csv(file)
    data = pd.concat([data, newData], ignore_index=True)

print(data)

# This example does a similar thing, but pulls in every .xlsx file in the directory. 
# This is useful if you have multiple files that you want to combine into one data frame

data = pd.DataFrame() # create an empty data frame
archive = mydir / 'archive'

for file in mydir.glob('*.xlsx'): # for each file in the directory that ends in .xlsx, read the file and append it to the data frame
    newData = pd.read_excel(file)
    data = pd.concat([data, newData], ignore_index=True)
    # Another handy piece, this moves any .xlsx file to an archive folder
    # the folder is defined above as 'archive'
    file.rename(archive / file.name)



# Access from Azure Blob Storage

import pandas as pd
import numpy as np
from pathlib import Path
from azure.storage.blob import ContainerClient
from io import StringIO
from dotenv import load_dotenv
import os

# Define the blob name you want to access
blob_name = "DashboardData.csv"

# Load the environment variables
load_dotenv()

# Get the connection string and blob container name from the environment
conn_str = os.getenv('AZURE_CONNECTION_STRING')
container_name = os.getenv('CONTAINER_NAME')

# Create a ContainerClient instance via connection string auth.
container_client = ContainerClient.from_connection_string(conn_str, container_name)
# Download blob as StorageStreamDownloader object (stored in memory)
downloaded_blob = container_client.download_blob(blob_name, encoding='ISO-8859-1')

# Get data as a pandas DataFrame. In this case, the data is read from a CSV file, so we use read_csv
# If the data is in a different format, you will need to use the appropriate function (e.g., read_excel)
df = pd.read_csv(StringIO(downloaded_blob.readall()), low_memory=False)
