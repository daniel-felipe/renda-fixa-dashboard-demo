import locale
import streamlit as st
import plotly.express as px
from src.data_loader import get_data


st.header('Performance')

df = get_data()
if df is None:
    st.warning('Nenhum dado encontrado.')
    st.stop()


def calculate_average(df):
    sum_invested = df['Saldo Bruto'].sum()

    if sum_invested == 0:
        return 0.0

    sum_assets = (df['Saldo Bruto'] * df['Taxa']).sum()
    return sum_assets / sum_invested


col1, col2, col3 = st.columns(3)

with col1:
    df_pre = df[df['Indexador'] == 'PRÉ']
    value = calculate_average(df_pre)
    value_formatted = locale.format_string('%.2f', value)
    st.metric('Taxa Média Pré', f'{value_formatted}%', border=True)

with col2:
    df_ipca = df[df['Indexador'] == 'IPCA']
    value = calculate_average(df_ipca)
    value_formatted = locale.format_string('%.2f', value)
    st.metric('Taxa Média IPCA', f'+{value_formatted}%', border=True)

with col3:
    df_cdi = df[df['Indexador'] == 'CDI']
    value = calculate_average(df_cdi)
    value_formatted = locale.format_string('%.2f', value)
    st.metric('Taxa Média CDI', f'{value_formatted}%', border=True)

container = st.container(border=True)
container.subheader('Ganho Bruto por Indexador')
df_grouped = (
    df.groupby('Indexador')[['Saldo Bruto', 'Valor Compra']].sum().reset_index()
)
df_grouped['Ganho Bruto'] = (
    df_grouped['Saldo Bruto'] - df_grouped['Valor Compra']
)
fig = px.bar(df_grouped, x='Indexador', y='Ganho Bruto')
fig.update_traces(hovertemplate='R$ %{y:,.2f}')
fig.update_layout(separators=',.2f')
container.plotly_chart(fig)
