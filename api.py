from flask import Flask, jsonify, request
#import pandas as pd
import pyarrow.parquet as pq
import matplotlib.pylab as plt
from db import create_table_from_excel

app = Flask(__name__)

@app.route("/Summary", methods=["GET"])
def readFileSummary():
    #Carregar DataSet
    if 'fileName' not in request.args:
        file_name = 'dados_sensores_5000.parquet'
    else:
        file_name = request.args['fileName']   
    #df = pd.read_parquet(file_name)
    # Read the Parquet file
    table = pq.read_table(file_name)
    # Get column names
    parquet_columns = table.schema.names #df.columns.tolist()
    #print(parquet_columns)
    # Read the first row (index 0)
    row = table.slice(0, 1)# df.iloc[0]  # Returns a Series
    print('\n\nrow:')
    #print(row)
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

    print(parquet_columns)
    print(types)
    print(staticalData)

    data = {
        "columns": parquet_columns,
        "types": types,
        "staticalData": staticalData
    }
    return data

@app.route("/parquettodb", methods=["POST"])
def loadToDb():
    #Carregar DataSet
    if 'fileName' not in request.get_json():
        file_name = 'dados_sensores_5000.parquet'
    else:
        file_name = request.args['fileName']  

    status = create_table_from_excel(file_name)    
    return status

        
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True) 