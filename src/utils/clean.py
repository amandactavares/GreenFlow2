import pyarrow as pa

def cleanDataSet(table,dataSetFormat="pandas"):
    parquet_columns = table.schema.names #df.columns.tolist()
    # Read the first row (index 0)
    row = table.slice(0, 1) # get first row to see the data type of each column

    stringColumns = []
    for column in parquet_columns:
        print(str(row.column(column).type))
        if str(row.column(column).type) == 'string':
            stringColumns.append(column)

    print(stringColumns)

    # Convert the PyArrow Table to a Pandas DataFrame
    df = table.to_pandas()
    #Remover Linhas com NAs
    df = df.dropna()

    #Remover Duplicados
    df = df.drop_duplicates()

    #Clean Spaces in string Columns dynamicaly
    for columnString in stringColumns:
        df[columnString]=df[columnString].str.strip()

    if dataSetFormat == "pandas":
        return df
    else :
        return pa.Table.from_pandas(df)
