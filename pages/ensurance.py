import streamlit as st
import plotly.express as px
from src.data_loader import get_data
from src.utils import format_currency


ENSURED_ASSET_TYPES = ['CDB', 'LCI', 'LCA', 'RDB', 'LC', 'LH']
FGC_LIMIT = 250_000

st.header('Proteção')

df = get_data()
if df is None:
    st.warning('Nenhum dado encontrado.')
    st.stop()

col1, col2 = st.columns(2)

with col1:
    df_filtered = df[df['Tipo de Ativo'].isin(ENSURED_ASSET_TYPES)]
    df_filtered = df.groupby('Emissor')['Saldo Bruto'].sum().reset_index()
    df_filtered['Coberto FGC'] = df_filtered['Saldo Bruto'].clip(
        upper=FGC_LIMIT
    )
    df_filtered['Excedente'] = (
        df_filtered['Saldo Bruto'] - df_filtered['Coberto FGC']
    )

    total_ensured = df_filtered['Coberto FGC'].sum()
    total = df_filtered['Saldo Bruto'].sum()

    percentage = round(total_ensured / total * 100) if total != 0 else 0

    st.metric(
        'Saldo Bruto Coberto pelo FGC',
        f'{percentage}%',
        border=True,
    )

with col2:
    df_grouped = df.groupby('Emissor')['Saldo Bruto'].sum().reset_index()
    df_filtered = df_grouped[df_grouped['Saldo Bruto'] > FGC_LIMIT]
    df_filtered.loc[:, 'Saldo Bruto'] = df_filtered['Saldo Bruto'] - FGC_LIMIT

    total = df_filtered['Saldo Bruto'].sum()

    st.metric(
        'Excedente ao Limite do FGC',
        format_currency(total),
        border=True,
    )


container = st.container(border=True)

with container:
    st.subheader('Saldo Bruto Total por Emissor')

    df_grouped = df.groupby('Emissor')['Saldo Bruto'].sum().reset_index()
    df_grouped['Saldo Bruto Formatado'] = df_grouped['Saldo Bruto'].apply(
        lambda value: format_currency(value)
    )
    fig = px.bar(
        df_grouped,
        x='Emissor',
        y='Saldo Bruto',
        text='Saldo Bruto Formatado',
        color='Saldo Bruto',
    )
    fig.update_traces(hovertemplate='R$ %{y:,.2f}')
    fig.update_layout(separators=',.2f')
    st.plotly_chart(fig)
