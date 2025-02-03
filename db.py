from flask import Flask, jsonify
from pathlib import Path
import pandas as pd
import pyarrow.parquet as pq
from pymongo import MongoClient

# Configuração do banco de dados
# MongoDB connection details
# replace localhost by the service name when migrating to Docker Containers
MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "GreenFlow"
#COLLECTION_NAME = "your_collection"

# Memory management in batch processing
BATCH_SIZE = 1000  # Adjust based on available memory

def createTableFromParquet(file_name):
    COLLECTION_NAME = Path(file_name).stem # get the filename and ignores the extesion
    print(f"COLLECTION_NAME: {COLLECTION_NAME}")
    # Connect to MongoDB
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME] 
    collection = db[COLLECTION_NAME]


    table = pq.read_table(file_name)
    #df = pd.read_parquet(file_name)

    #Clean the DataSet



    chunks = []
    #num_rows = df.shape[0]  # Total number of rows
    # Get the number of rows
    num_rows = table.num_rows

    for start in range(0, num_rows, BATCH_SIZE):
        #end = start + BATCH_SIZE  # Define chunk range
        chunk = table.slice(start, BATCH_SIZE) #df[start:end]  # Slice DataFrame
        chunks.append(chunk)  # Store chunk

    # Now, `chunks` contains the DataFrame split into smaller parts

    total_inserted = 0
    for chunk in chunks:
        data = chunk.to_pylist()#.to_dict(orient="records")
        collection.insert_many(data)
        total_inserted += len(data)
        print(f"Inserted {len(data)} records.")

    # Read the Parquet file in chunks
    # df_iterator = pd.read_parquet(file_name, engine="pyarrow", columns=None, iterator=True)
    # total_inserted = 0
    # for chunk in df_iterator:
    #     data = chunk.to_dict(orient="records")  # Convert chunk to dict
    #     if data:
    #         collection.insert_many(data)  # Insert batch into MongoDB
    #         total_inserted += len(data)
    #         print(f"Inserted {len(data)} records, Total: {total_inserted}")

    print(f"Finished inserting {total_inserted} records into MongoDB.")

    # Close the MongoDB connection
    client.close()
    result = {
        "tableName": COLLECTION_NAME,
        "records": total_inserted
    }
    print(result)
    
    return jsonify(result)

# def createTableFromParquet(file_name):
#     COLLECTION_NAME = Path(file_name).stem
#     client = MongoClient(MONGO_URI)
#     db = client[DATABASE_NAME] 
#     collection = db[COLLECTION_NAME]