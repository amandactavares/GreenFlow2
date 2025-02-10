import sys
import os

from flask import jsonify, request

from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import Optional
import uvicorn

#import pandas as pd
import pyarrow.parquet as pq
import pyarrow.compute as pc
import matplotlib.pylab as plt
import json
from db import createTableFromParquet 
from utils.clean import cleanDataSet

# Add the parent directory to Python's module search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

app = FastAPI()

# Pydantic model for request body
class ParquetFile(BaseModel):
    file_name: Optional[str] = 'dados_sensores_5000.parquet'# This field is optional, default is 'dados_sensores_5000.parquet'

@app.get("/Summary")
def readFileSummary(parquetfile: ParquetFile = Depends()):
    #Carregar DataSet
    file_name = parquetfile.file_name    

    # Read the Parquet file
    table = pq.read_table(file_name)
    # Get column names
    parquet_columns = table.schema.names

    # Read the first row (index 0)
    row = table.slice(0, 1)# df.iloc[0]  # Returns a Series

    types = {}
    staticalData = {}
    for column in parquet_columns:
        types[column]= str(row.column(column).type)
        if row.column(column).type == 'double': 
            rowList = table.column(column).to_pylist() 
            staticalData[column] = {
                "max": max(rowList),
                "min": min(rowList),
                "avarage": round(sum(rowList)/len(rowList),3)
            }

    data = {
        "columns": parquet_columns,
        "types": types,
        "staticalData": staticalData
    }
    return data

@app.post("/parquettodb")
def loadToDb(parquetfile: ParquetFile):
    #Carregar DataSet
    file_name = parquetfile.file_name  

    status = createTableFromParquet(file_name)    
    return status

@app.post("/cleanDataSet")
def clean(parquetfile: ParquetFile):
    #Clean DataSet

    file_name = parquetfile.file_name    

    # Read the Parquet file
    table = pq.read_table(file_name)

    #clean procedure/function
    df = cleanDataSet(table)
    numRows = len(df)

    # Convert DataFrame to dictionary
    df_dict = df.to_dict(orient='records')  # Each row becomes a dictionary
    
    return {
        "numRows": numRows,
        "dataSet": df_dict
    }
        
if __name__ == "__main__":
    print("Python Path:", sys.path)  # Debugging line
    uvicorn.run("src.api:app", host="0.0.0.0", port=8080, reload=True) 