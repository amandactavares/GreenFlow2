import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import seaborn as sns
import plotly.express as px

#Configurações de Página
st.set_page_config(layout="wide")

#Título
st.title("Consumos de Energia, Água e Emissões CO2")

with st.expander("Upload Ficheiro de Dados"):
    #Pedir Ficheiro Streamlite
    @st.cache_data
    def load_data(file):
        data=pd.read_parquet(file)
        return data

    uploaded_file = st.file_uploader("Escolha um Ficheiro Parquet")

    if uploaded_file is None:
        st.info("Escolha um Ficheiro")
        st.stop()


#Criação dos Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Global", "Empresa", "Setor",  "Monitorização"])


#Funções

#Obter e Limpar Dados
def clean_data(file):

    #Carregar DataSet
    df = load_data(file)


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

#Gráfico Histograma
def histograma(df):
    colunas = ['energia_kwh', 'agua_m3', 'co2_emissoes' ]
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    # Gerar histogramas e a linha de ajuste para cada coluna
    for i, coluna in enumerate(colunas):
        # Plotando o histograma
        sns.histplot(df[coluna], kde=True, bins=20, color='indianred', edgecolor='black', ax=axes[i])  
        # Definindo o título e os rótulos
        axes[i].set_title(f"Histograma de {coluna}")
        axes[i].set_xlabel(coluna)
        axes[i].set_ylabel('Frequência')
    plt.tight_layout()

    st.pyplot(fig)
    return 

#Consumo Agregação Empresa
def consumo_total_empresa_max(df):
    # Agrupar por empresa
    df_agrupado_emp = df.groupby("empresa").sum(numeric_only=True)

    maior_energia_emp = df_agrupado_emp["energia_kwh"].idxmax()
    maior_energia_emp_val = max(df_agrupado_emp["energia_kwh"])
    maior_agua_emp = df_agrupado_emp["agua_m3"].idxmax()
    maior_agua_emp_val = max(df_agrupado_emp["agua_m3"])
    maior_co2_emp = df_agrupado_emp["co2_emissoes"].idxmax()
    maior_co2_emp_val = max(df_agrupado_emp["co2_emissoes"])

    st.write(f"Empresa com maior consumo de energia: {maior_energia_emp} com {maior_energia_emp_val} kwh")
    st.write(f"Empresa com maior consumo de água: {maior_agua_emp} com {maior_agua_emp_val} m3")
    st.write(f"Empresa com maior emissão de CO₂: {maior_co2_emp} com {maior_co2_emp_val} emissões")
    
    return

#Consumo Agregação Empresa
def consumo_total_empresa_min(df):
    # Agrupar por empresa
    df_agrupado_emp = df.groupby("empresa").sum(numeric_only=True)

    # Encontrar as empresas com menor consumo
    menor_energia_emp = df_agrupado_emp["energia_kwh"].idxmin()
    menor_energia_emp_val = min(df_agrupado_emp["energia_kwh"])
    menor_agua_emp = df_agrupado_emp["agua_m3"].idxmin()
    menor_agua_emp_val = min(df_agrupado_emp["agua_m3"])
    menor_co2_emp = df_agrupado_emp["co2_emissoes"].idxmin()
    menor_co2_emp_val = min(df_agrupado_emp["co2_emissoes"])

    st.write(f"Empresa com menor consumo de energia: {menor_energia_emp} com {menor_energia_emp_val} kwh")
    st.write(f"Empresa com menor consumo de água: {menor_agua_emp} com {menor_agua_emp_val} m3")
    st.write(f"Empresa com menor emissão de CO₂: {menor_co2_emp} com {menor_co2_emp_val} em emissões de CO₂")
    return

#Consumo Agregação Setor
def consumo_total_setor(df):
    #Agrupar por setor e somar os valores
    df_agrupado = df.groupby("setor").sum(numeric_only=True)

    # Criar os subplots
    fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharey=False)  # 1 linha, 3 colunas

    # Plot Energia
    axes[0].bar(df_agrupado.index, df_agrupado["energia_kwh"], color="seagreen")
    axes[0].set_title("Consumo de Energia (kWh)")
    axes[0].set_ylabel("kWh")
    axes[0].set_xticklabels(df_agrupado.index, rotation=45)

    # Plot Água
    axes[1].bar(df_agrupado.index, df_agrupado["agua_m3"], color="royalblue")
    axes[1].set_title("Consumo de Água (m³)")
    axes[1].set_ylabel("m³")
    axes[1].set_xticklabels(df_agrupado.index, rotation=45)

    # Plot CO₂
    axes[2].bar(df_agrupado.index, df_agrupado["co2_emissoes"], color="crimson")
    axes[2].set_title("Emissões de CO₂")
    axes[2].set_ylabel("Toneladas")
    axes[2].set_xticklabels(df_agrupado.index, rotation=45)

    # Ajustar layout para não sobrepor labels
    plt.tight_layout()
    st.pyplot(fig)
    return

#Consumo Total Max
def cons_tot_setor_max(df):
    #Agrupar por setor e somar os valores
    df_agrupado = df.groupby("setor").sum(numeric_only=True)

    # Encontrar os setores com maior consumo
    maior_energia = df_agrupado["energia_kwh"].idxmax()
    maior_agua = df_agrupado["agua_m3"].idxmax()
    maior_co2 = df_agrupado["co2_emissoes"].idxmax()

    st.write(f"Setor com maior consumo total de energia: {maior_energia}")
    st.write(f"Setor com maior consumo total de água: {maior_agua}")
    st.write(f"Setor com maior emissão total de CO₂: {maior_co2}")
    return

#Consumo Total Min
def cons_tot_setor_min(df):
    #Agrupar por setor e somar os valores
    df_agrupado = df.groupby("setor").sum(numeric_only=True)
    #Encontrar os setores com menor consumo
    menor_energia = df_agrupado["energia_kwh"].idxmin()
    menor_agua = df_agrupado["agua_m3"].idxmin()
    menor_co2 = df_agrupado["co2_emissoes"].idxmin()

    st.write('\n')
    st.write(f"Setor com menor consumo total de energia: {menor_energia}")
    st.write(f"Setor com menor consumo total de água: {menor_agua}")
    st.write(f"Setor com menor emissão total de CO₂: {menor_co2}")
    return

#Número de Empresas
def nr_empresas(df):
    #Agrupar po Setor e Verificar Nr de Empresas de Cada Setor

    #Verificar se algum sector têm um nr de empresas significativamente diferente
    nr_empresas = df.groupby("setor")['empresa'].count().reset_index()
    nr_empresas.columns =['setor', 'empresas']

    df_agrupado_setor = df.groupby("setor").sum(numeric_only=True)

    #Plot Chart
    fig, axes = plt.subplots(figsize=(7,4))
    axes.bar(nr_empresas['setor'], nr_empresas['empresas'], color="indianred")
    axes.set_title("Nr de Empresas por Setor")
    axes.set_xlabel("Setor")
    axes.set_ylabel("# Empresas")

    for i in range(len(nr_empresas)):
        axes.text(i, nr_empresas['empresas'][i] + 0.05, str(nr_empresas['empresas'][i]), 
                ha='center', color='black')

    st.pyplot(fig)
    return

#Consumo Setor Médio por Empresa
def consumo_setor_por_empresa(df):
    # Agrupar por setor e somar os valores
    df_setor = df.groupby('setor').sum().reset_index()
    # Obter Nr de Empresas por Setor
    df_nrempresas = df.groupby('setor')['empresa'].count().reset_index()
    # Merge para obter dataframe com consumo total e nr de empresas
    merged_df = pd.merge(df_setor, df_nrempresas, on='setor')

    #Calcular consumo por empresa
    merged_df['energia_kwh_por_empresa'] = merged_df['energia_kwh'] / merged_df['empresa_y']
    merged_df['agua_m3_por_empresa'] = merged_df['agua_m3'] / merged_df['empresa_y']
    merged_df['co2_emissoes_por_empresa'] = merged_df['co2_emissoes'] / merged_df['empresa_y']

    # Output
    #print(merged_df[['setor', 'energia_kwh_por_empresa', 'agua_m3_por_empresa', 'co2_emissoes_por_empresa']])

    #Representação Gráfica
    # Criar os subplots
    fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharey=False)  # 1 linha, 3 colunas

    # Plot Energia
    axes[0].bar(merged_df['setor'], merged_df["energia_kwh_por_empresa"], color="mediumseagreen")
    axes[0].set_title("Consumo de Energia (kWh) Médio por Empresa")
    axes[0].set_ylabel("kWh")
    axes[0].set_xticklabels(merged_df['setor'], rotation=45)

    # Plot Água
    axes[1].bar(merged_df['setor'], merged_df["agua_m3_por_empresa"], color="cornflowerblue")
    axes[1].set_title("Consumo de Água (m³) Médio por Empresa")
    axes[1].set_ylabel("m³")
    axes[1].set_xticklabels(merged_df['setor'], rotation=45)

    # Plot CO₂
    axes[2].bar(merged_df['setor'], merged_df["co2_emissoes_por_empresa"], color="palevioletred")
    axes[2].set_title("Emissões de CO₂ Médias por Empresa")
    axes[2].set_ylabel("Toneladas")
    axes[2].set_xticklabels(merged_df['setor'], rotation=45)

    # Ajustar layout para não sobrepor labels
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)

    return

#Consumo Setor Médio por Empresa Max
def cons_set_max(df):
    # Agrupar por setor e somar os valores
    df_setor = df.groupby('setor').sum().reset_index()
    # Obter Nr de Empresas por Setor
    df_nrempresas = df.groupby('setor')['empresa'].count().reset_index()
    # Merge para obter dataframe com consumo total e nr de empresas
    merged_df = pd.merge(df_setor, df_nrempresas, on='setor')

    #Calcular consumo por empresa
    merged_df['energia_kwh_por_empresa'] = merged_df['energia_kwh'] / merged_df['empresa_y']
    merged_df['agua_m3_por_empresa'] = merged_df['agua_m3'] / merged_df['empresa_y']
    merged_df['co2_emissoes_por_empresa'] = merged_df['co2_emissoes'] / merged_df['empresa_y']

    # Encontrar os setores com maior consumo por empresa
    maior_energia_pemp = merged_df['setor'][merged_df["energia_kwh_por_empresa"].idxmax()]
    maior_agua_pemp = merged_df['setor'][merged_df["agua_m3_por_empresa"].idxmax()]
    maior_co2_pemp = merged_df['setor'][merged_df["co2_emissoes_por_empresa"].idxmax()]


    st.write(f"Setor com maior consumo médio de energia por empresa: {maior_energia_pemp}")
    st.write(f"Setor com maior consumo médio de água por empresa: {maior_agua_pemp}")
    st.write(f"Setor com maior média de emissão de CO₂ por empresa: {maior_co2_pemp}")
    return

#Consumo Setor Médio por Empresa Min
def cons_set_min(df):
    # Agrupar por setor e somar os valores
    df_setor = df.groupby('setor').sum().reset_index()
    # Obter Nr de Empresas por Setor
    df_nrempresas = df.groupby('setor')['empresa'].count().reset_index()
    # Merge para obter dataframe com consumo total e nr de empresas
    merged_df = pd.merge(df_setor, df_nrempresas, on='setor')

    #Calcular consumo por empresa
    merged_df['energia_kwh_por_empresa'] = merged_df['energia_kwh'] / merged_df['empresa_y']
    merged_df['agua_m3_por_empresa'] = merged_df['agua_m3'] / merged_df['empresa_y']
    merged_df['co2_emissoes_por_empresa'] = merged_df['co2_emissoes'] / merged_df['empresa_y']

    #Encontrar os setores com menor consumo por empresa
    menor_energia_pemp = merged_df['setor'][merged_df["energia_kwh_por_empresa"].idxmin()]
    menor_agua_pemp = merged_df['setor'][merged_df["agua_m3_por_empresa"].idxmin()]
    menor_co2_pemp = merged_df['setor'][merged_df["co2_emissoes_por_empresa"].idxmin()]

    st.write('\n')
    st.write(f"Setor com menor consumo médio de energia por empresa: {menor_energia_pemp}")
    st.write(f"Setor com menor consumo médio de água por empresa: {menor_agua_pemp}")
    st.write(f"Setor com menor média de emissão de CO₂ por empresa: {menor_co2_pemp}")

    return

#Boxplot Setor
def bloxplot_setor(df):
    # Definir as colunas
    colunas = ['energia_kwh', 'agua_m3', 'co2_emissoes']

    # Criar o gráfico
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    # Gerar boxplots para cada coluna
    for i, coluna in enumerate(colunas):
        sns.boxplot(data=df, x='setor', y=coluna, hue='setor', ax=axes[i], palette="Set2")
        axes[i].set_title(f"Distribuição de {coluna} por Setor")
        axes[i].set_xlabel('Setor')
        axes[i].set_ylabel(coluna)

    # Ajustar o layout
    plt.tight_layout()
    st.pyplot(fig)
    return


#Limpar Dados Chamar Função
df = clean_data(uploaded_file)


with tab1:
    
    st.header("Análise Global dos Dados")
    st.write("Visão Geral dos Dados Submetidos")
   
    col1 = st.columns(1)
    st.subheader("Visualização dos Dados Introduzidos")
    with st.expander("Vizualizar Dados"):
        st.dataframe(df)


    col2 = st.columns(1)
    st.subheader("Histograma de Consumos")
    #Histograma
    histograma(df)


with tab2:
    
    st.header("Análise por Empresa")
    st.write("Métricas e Análise dos Dados por Empresa")
    
    col1, col2 = st.columns(2)
    #Análise Empresa
    with col1:
        st.subheader("Empresas com Maior Consumo Total")
        consumo_total_empresa_max(df)

    with col2:
        st.subheader("Empresas com Menor Consumo Total")
        consumo_total_empresa_min(df)
    

    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Número de Empresas por Setor")
        nr_empresas(df)
    

with tab3:
    st.header("Análise por Sector")
    st.write("Métricas e Análise dos Dados por Setor")

    col1 = st.columns(1)
    st.subheader("Consumo Total por Setor")
    consumo_total_setor(df)
    
    col2, col3 = st.columns(2)
    with col2:
        st.subheader("Setor com Maior Consumo Total")
        cons_tot_setor_max(df)

    with col3:
        st.subheader("Setor com Menor Consumo Total")
        cons_tot_setor_min(df)

    col4 = st.columns(1)
    st.subheader("Boxplot por Setor")
    
    # Criar os boxplots
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    colunas = ['energia_kwh', 'agua_m3', 'co2_emissoes']
    titulos = ['Energia (kWh)', 'Água (m³)', 'Emissões de CO₂']
    
    for i, coluna in enumerate(colunas):
        sns.boxplot(data=df, x='setor', y=coluna, hue='setor', ax=axes[i], palette="Set2")
        axes[i].set_title(f"Distribuição de {titulos[i]} por Setor")
        axes[i].set_xlabel('Setor')
        axes[i].set_ylabel(titulos[i])
    
    plt.tight_layout()
    st.pyplot(fig)

    # Adicionar métricas em tabelas
    st.subheader("Métricas por Setor")

    # Função para criar uma tabela formatada
    def criar_tabela_metricas(df, coluna, titulo):
        media = df.groupby('setor')[coluna].mean().apply(lambda x: f"{x:.2f}") #"{:.2f}".format(df.groupby('setor')[coluna].mean())
        Q3 = df[coluna].quantile(0.75)
        empresas_acima_Q3 = df[df[coluna] > Q3].groupby('setor')['empresa'].count()
        
        # Criar DataFrame para a tabela
        tabela = pd.DataFrame({
            'Setor': media.index,
            'Média': media.values,
            'Empresas Acima do 3º Quartil': empresas_acima_Q3.values
        })
        
        # Exibir tabela sem índices
        st.markdown(f"**{titulo}**")
        st.table(tabela.style.hide(axis="index"))  # Oculta os índices

    # Tabelas para cada métrica
    col5, col6, col7 = st.columns(3)

    with col5:
        criar_tabela_metricas(df, 'energia_kwh', 'Energia (kWh)')

    with col6:
        criar_tabela_metricas(df, 'agua_m3', 'Água (m³)')

    with col7:
        criar_tabela_metricas(df, 'co2_emissoes', 'Emissões de CO₂')

    # Dropdown para selecionar empresa
    st.subheader("Detalhes por Empresa")
    
    # Lista de empresas acima do 3º quartil em pelo menos uma métrica
    empresas_acima_Q3 = df[
        (df['energia_kwh'] > df['energia_kwh'].quantile(0.75)) |
        (df['agua_m3'] > df['agua_m3'].quantile(0.75)) |
        (df['co2_emissoes'] > df['co2_emissoes'].quantile(0.75))
    ]['empresa'].unique()

    # Dropdown para selecionar empresa
    empresa_selecionada = st.selectbox(
        "Selecione uma empresa", 
        empresas_acima_Q3,
        key="dropdown_empresas"  # Adiciona uma chave única para o dropdown
    )

    # Filtrar dados da empresa selecionada
    dados_empresa = df[df['empresa'] == empresa_selecionada]

    # Calcular o 3º quartil para cada métrica
    Q3_energia = "{:.2f}".format(df['energia_kwh'].quantile(0.75))
    Q3_agua = "{:.2f}".format(df['agua_m3'].quantile(0.75))
    Q3_co2 = "{:.2f}".format(df['co2_emissoes'].quantile(0.75))

    # Criar tabela com consumo da empresa e valor de referência (3º quartil)
    consumo_empresa = pd.DataFrame({
        'Métrica': ['Energia (kWh)', 'Água (m³)', 'Emissões de CO₂'],
        'Consumo da Empresa': [
            "{:.2f}".format(dados_empresa['energia_kwh'].values[0]),
            "{:.2f}".format(dados_empresa['agua_m3'].values[0]),
            "{:.2f}".format(dados_empresa['co2_emissoes'].values[0])
        ],
        'Valor de Referência (3º Quartil)': [Q3_energia, Q3_agua, Q3_co2]
    })

    # Exibir tabela sem índices
    st.write(f"Consumo da empresa **{empresa_selecionada}**:")
    st.table(consumo_empresa.style.hide(axis="index"))  # Oculta os índices

    col5 = st.columns(1)
    st.subheader("Consumo Médio por Empresa por Setor")
    consumo_setor_por_empresa(df)

    col6, col7 = st.columns(2)
    with col6:
        st.subheader("Setor com Maior Consumo Médio por Empresa")
        cons_set_max(df)

    with col7:
        st.subheader("Setor com Menor Consumo Médio por Empresa")
        cons_set_min(df)

with tab4:
    st.header("Monitorização de Empresas")
    st.write("Espaço para Identificar Empresas com Consumo Anormal e/ou Acima da Média")
    
    col1, col2, col3 = st.columns(3)

    with col1:
        #Dropdown Setor
        dropdown_setor = df['setor'].unique().tolist()
        dropdown_setor = ['Todos os Setores'] + dropdown_setor
        setor_sel =st.selectbox("Setor", dropdown_setor)
    
    with col2:
        #Dropdown Area
        dropdown_area = ['Energia'] + ['Água'] + ['Emissões CO2']
        area_sel =st.selectbox("Área de Consumo", dropdown_area)

    with col3:
        #Input Utilizador
        percentil = st.number_input("Introduza Percentil (0-100)")
        percentil = round(float(percentil), 2)
        if percentil <0 or percentil > 100:
            st.write("O Percentil Introduzido deve estar entre 0 e 100")


    col4 = st.columns(1)
    
    st.subheader(f"Valores Estatísticos do Consumo de {area_sel} e Setor: {setor_sel} ")

    #Filtrar Dataset mediante seleção do User
    if setor_sel == 'Todos os Setores':
        df_setor = df
    else:
        df_setor = df[df['setor'] == setor_sel]

    #Calcular Valores estatísticos
    average = df_setor[['energia_kwh', 'agua_m3', 'co2_emissoes']].mean()
    val_min = df_setor[['energia_kwh', 'agua_m3', 'co2_emissoes']].min()
    val_max = df_setor[['energia_kwh', 'agua_m3', 'co2_emissoes']].max()
    percentils = df_setor[['energia_kwh', 'agua_m3', 'co2_emissoes']].quantile([0.25, 0.50, 0.75])

    if area_sel == 'Emissões CO2':
        average = average['co2_emissoes']
        val_min = val_min['co2_emissoes']
        val_max = val_max['co2_emissoes']
        percentils = percentils['co2_emissoes']
    elif area_sel  == "Água":
        average = average['agua_m3']
        val_min = val_min['agua_m3']
        val_max = val_max['agua_m3']
        percentils = percentils['agua_m3']
    else:
        average = average['energia_kwh']
        val_min = val_min['energia_kwh']
        val_max = val_max['energia_kwh']
        percentils = percentils['energia_kwh']
        

    col5, col6 = st.columns(2)

    with col5:
        
        st.markdown(f"**Average** = {round(average, 2)}")
        st.markdown (f"**Valor Mínimo** = {round(val_min,2)}")
        st.markdown (f"**Valor Máximo** = {round(val_max,2)}")
        
    
    with col6:
        st.markdown (f"**Percentil 25%** = {round(percentils[0.25],2)}")
        st.markdown (f"**Percentil 50%** = {round(percentils[0.50],2)}")
        st.markdown (f"**Percentil 75%** = {round(percentils[0.75],2)}")


    col7 = st.columns(1)

    st.subheader(f"Empresas no Percentil {percentil} de Consumo de {area_sel} , Relativo ao Setor: {setor_sel} ")

    if area_sel == 'Emissões CO2':
        valor_percentil = np.percentile(df_setor['co2_emissoes'], percentil)
        obs_filtradas = df_setor[df_setor['co2_emissoes'] > valor_percentil]
        obs_filtradas = obs_filtradas.sort_values(by='co2_emissoes', ascending=False)
        nr_emp = len(obs_filtradas)
        st.markdown(f"**Número de Empresas** = {nr_emp}")
        st.markdown("**Lista de Empresas**")
        st.write(obs_filtradas[['empresa', 'co2_emissoes']])
        
    elif area_sel  == "Água":
        valor_percentil = np.percentile(df_setor['agua_m3'], percentil)
        obs_filtradas = df_setor[df_setor['agua_m3'] > valor_percentil]
        obs_filtradas = obs_filtradas.sort_values(by='agua_m3', ascending=False)
        nr_emp = len(obs_filtradas)
        st.markdown(f"**Número de Empresas** = {nr_emp}")
        st.markdown("**Lista de Empresas**")
        st.write(obs_filtradas[['empresa', 'agua_m3']])
    else:
        valor_percentil = np.percentile(df_setor['energia_kwh'], percentil)
        obs_filtradas = df_setor[df_setor['energia_kwh'] > valor_percentil]
        obs_filtradas = obs_filtradas.sort_values(by='energia_kwh', ascending=False)
        nr_emp = len(obs_filtradas)
        st.markdown(f"**Número de Empresas** = {nr_emp}")
        st.markdown("**Lista de Empresas**")
        st.write(obs_filtradas[['empresa', 'energia_kwh']])

        

        
    