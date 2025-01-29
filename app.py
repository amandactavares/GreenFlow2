import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import seaborn as sns


df = pd.read_parquet("dados_sensores_5000.parquet")
print(df.head())

#Entender a Estrutura dos Dados
print(df.shape)
print(df.head())
print(df.columns)
print(df.info())

df.describe()

df.query('agua_m3 > 200')

#df.createOrReplaceTempView("sales")
#resultado = spark.sql("SELECT Region, SUM(TotalPrice) AS TotalRevenue FROM sales GROUP BY Region")
#resultado.show()