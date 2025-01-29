import pandas as pd


df = pd.read_parquet("dados_sensores_5000.parquet")

print(df.head())