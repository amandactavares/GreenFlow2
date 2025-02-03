from flask import Flask, jsonify, request
import pandas as pd
import matplotlib.pylab as plt
from db import create_table_from_excel

app = Flask(__name__)

@app.route("/readFields", methods=["GET"])
def readFields():
    #Carregar DataSet
    if 'fileName' not in request.args:
        file_name = 'dados_sensores_5000.parquet'
    else:
        file_name = request.args['fileName']   
    df = pd.read_parquet(file_name)
    # Get column names
    parquet_columns = df.columns
    return parquet_columns.tolist()

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