# --- IMPORTS ---
import streamlit as st
import pandas as pd
import plotly.express as px
from ucimlrepo import fetch_ucirepo 

# --- DADOS ---
bank_marketing = fetch_ucirepo(id=222) 

X = bank_marketing.data.features 
y = bank_marketing.data.targets 

df = pd.concat([X, y], axis=1)

# --- STREAMLIT APP ---
# Título
st.title('Análise de Marketing Bancário')

# Mostrar o DataFrame
if st.checkbox('Mostrar dados brutos'):
    st.dataframe(df)

# Gráfico de distribuição do target
st.subheader('Distribuição do Target (y)')
fig1 = px.histogram(df, x='y')
st.plotly_chart(fig1)

# Filtro por profissão
st.subheader('Análise por profissão')
job_filter = st.selectbox('Selecione a profissão:', df['job'].unique())

df_filtered = df[df['job'] == job_filter]

fig2 = px.histogram(df_filtered, x='y', title=f'Resultado para profissão: {job_filter}')
st.plotly_chart(fig2)

