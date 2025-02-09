fig = px.bar(df, x="setor", y=["energia_kwh", "agua_m3", "co2_emissoes"],
             title="Consumo de Energia, Água e Emissões de CO2 por Setor", 
             labels={"setor": "Setor", "value": "Valor", "variable": "Categoria"})
st.plotly_chart(fig)

fig = px.scatter(df, x="energia_kwh", y="co2_emissoes", color="setor",
                 title="Relação entre Consumo de Energia e Emissões de CO2",
                 labels={"energia_kwh": "Consumo de Energia (kWh)", "co2_emissoes": "Emissões de CO2 (kg)"})
st.plotly_chart(fig)