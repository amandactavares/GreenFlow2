from flask import Flask, jsonify, request
#import pandas as pd
import pyarrow.parquet as pq
import pyarrow.compute as pc
import matplotlib.pylab as plt
import json
from db import createTableFromParquet 
from utils.clean import cleanDataSet

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

@app.route("/parquettodb", methods=["POST"])
def loadToDb():
    #Carregar DataSet
    if 'fileName' not in request.get_json():
        file_name = 'dados_sensores_5000.parquet'
    else:
        file_name = request.args['fileName']  

    status = createTableFromParquet(file_name)    
    return status

@app.route("/cleanDataSet", methods=["POST"])
def clean():
    #Clean DataSet
    params = request.get_json(silent=True)
    if params is None or "fileName" not in params:
        file_name = 'dados_sensores_5000.parquet'
    else:
        file_name = params.get("fileName")    

    # Read the Parquet file
    table = pq.read_table(file_name)
    print(table.num_rows)

    #clean procedure/function
    df = cleanDataSet(table)
    numRows = len(df)

    # Convert DataFrame to dictionary
    df_dict = df.to_dict(orient='records')  # Each row becomes a dictionary

    data = jsonify({
        "numRows": numRows,
        "dataSet": df_dict
    })

    return data  # Ensure JSON response

    ######################## using only pyarrow complicates to much for now
    # # Create masks for null values in each column
    # null_masks = [pc.is_null(table[column]) for column in table.column_names]
    # print(null_masks)

    # # Combine the masks with 'pc.or_' (logical OR for any null in any column)
    # combined_mask = null_masks[0]
    # for mask in null_masks[1:]:
    #     combined_mask = pc.or_(combined_mask, mask)

    # # Invert the combined mask using `pc.invert()`
    # inverted_mask = pc.invert(combined_mask)

    # # Filter the table: Keep only rows without nulls (inverse of mask)
    # filtered_table = table.filter(inverted_mask)
    # print(filtered_table.num_rows)

        
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True) 