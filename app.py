import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import seaborn as sns

def clean_data(file_name):

    #Carregar DataSet
    df = pd.read_parquet(file_name)


    #Informação Inicial do Dataset
    print("\nInformação Dataset:")
    print('\n')
    print(df.info())
    print('\n')
    print(df.head())
    print('\n')
    print(df.describe())

    #Limpar Espaços em Colunas String
    df['empresa']=df['empresa'].str.strip()
    df['setor']=df['setor'].str.strip()

    #Remover Linhas com NAs
    df = df.dropna()
    print("\nNr de Observações após Remoção de NA:", len(df))

    #Remover Duplicados
    df = df.drop_duplicates()
    print("\nNr de Observações após Remoção de Duplicados:", len(df))

    #Converter Data Types de Columnas Float para Numeric
    df['energia_kwh'] = pd.to_numeric(df['energia_kwh'], errors='coerce')
    df['agua_m3'] = pd.to_numeric(df['agua_m3'], errors='coerce')
    df['co2_emissoes'] = pd.to_numeric(df['co2_emissoes'], errors='coerce')

    #Remover observações com valores não numéricos para as 3 colunas numéricas
    df = df.dropna(subset=['energia_kwh', 'agua_m3', 'co2_emissoes'])
    print("\nNr de Observações após Verificação Colunas Numéricas:", len(df))

    #Resumo Estatístico
    print('\nResumo Estatístico de Colunas Numérias')
    print(df[['energia_kwh', 'agua_m3', 'co2_emissoes']].describe())

    #Verificar se Existe Correlação entre as 3 colunas numéricas
    print('\nMatrix de Correlação')
    print(df[['energia_kwh', 'agua_m3', 'co2_emissoes']].corr())


    #Função para Remover Outliers
    def remove_outliers(df, column_name):
        Q1 = df[column_name].quantile(0.25)
        Q3 = df[column_name].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        return df[(df[column_name] >= lower_bound) & (df[column_name] <= upper_bound)]

    df_clean = df.copy()
    df_clean = remove_outliers(df_clean, 'energia_kwh')
    df_clean = remove_outliers(df_clean, 'agua_m3')
    df_clean = remove_outliers(df_clean, 'co2_emissoes')

    #Informação Dataset Tratado
    print('\nInformações Dataset Tratado')
    print('\n')
    print(df_clean.info())
    print('\n')
    print(df_clean.head())

    return df_clean

df = clean_data('dados_sensores_5000.parquet')