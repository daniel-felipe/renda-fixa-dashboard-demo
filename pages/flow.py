import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from src.data_loader import get_data


st.header('Prazos')

df = get_data()

if df is None:
    st.warning('Nenhum dado encontrado.')
    st.stop()

col1, col2 = st.columns(2)

with col1:
    container = st.container(border=True)
    container.subheader('Ditribuição por prazo')
    df_copy = df
    df_copy['Vencimento'] = pd.to_datetime(df_copy['Vencimento'])
    df_copy['Emissão'] = pd.to_datetime(df_copy['Emissão'])
    df_copy['Prazo Dias'] = (df_copy['Vencimento'] - df_copy['Emissão']).dt.days
    df_copy['Faixa Prazo'] = pd.cut(
        df['Prazo Dias'],
        bins=[0, 365, 1095, np.inf],
        labels=[
            'Curto Prazo',
            'Médio Prazo',
            'Longo Prazo',
        ],
    )
    df_grouped = df.groupby('Faixa Prazo')['Saldo Bruto'].sum().reset_index()
    fig = px.bar(
        df_grouped,
        x='Saldo Bruto',
        y='Faixa Prazo',
        orientation='h',
    )
    fig.update_traces(hovertemplate='R$ %{x:,.2f}')
    container.plotly_chart(fig, height=400)

with col2:
    container = st.container(border=True)
    container.subheader('Ditribuição da Carteira por Liquidez')
    df_grouped = df.groupby('Liquidez')['Saldo Bruto'].sum().reset_index()
    fig = px.pie(
        df_grouped,
        names='Liquidez',
        values='Saldo Bruto',
    )
    fig.update_layout(separators=',.2f')
    fig.update_traces(
        hovertemplate='%{label}<br>R$ %{value:,.2f}<extra></extra>'
    )
    container.plotly_chart(fig, height=400)


with st.container(border=True):
    st.subheader('Vencimento de Ativos por Ano')
    df['Vencimento'] = pd.to_datetime(df['Vencimento'])
    df_grouped = (
        df.groupby(df['Vencimento'].dt.year)['Saldo Bruto'].sum().reset_index()
    )
    fig = px.bar(df_grouped, x='Vencimento', y='Saldo Bruto')
    fig.update_traces(hovertemplate='R$ %{y:,.2f}')
    fig.update_layout(separators=',.2f')
    st.plotly_chart(fig)
