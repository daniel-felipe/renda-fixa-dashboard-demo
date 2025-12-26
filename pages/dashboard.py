import streamlit as st
import plotly.express as px
import pandas as pd
from src.data_loader import get_data
from src.utils import format_currency


st.title('Dashboard')

df = get_data()

if df is None:
    st.warning('Nenhum dado encontrado.')
    st.stop()

col1, col2, col3 = st.columns(3)

with col1:
    total = df['Saldo Bruto'].sum()
    st.metric(
        label='Saldo Bruto Total', value=format_currency(total), border=True
    )

with col2:
    total = df['Saldo Líquido'].sum()
    st.metric(
        label='Saldo Líquido Total',
        value=format_currency(total),
        border=True,
    )

with col3:
    total = df['Valor Compra'].sum()
    st.metric(
        label='Total Valor Investido', value=format_currency(total), border=True
    )

with st.container(border=True):
    st.subheader('Saldo Líquido por Emissor')
    df_filtered = df.groupby('Emissor')['Saldo Líquido'].sum().reset_index()
    fig = px.bar(df_filtered, x='Emissor', y='Saldo Líquido')
    fig.update_traces(hovertemplate='R$ %{y:,.2f}')
    fig.update_layout(separators=',.2f')
    st.plotly_chart(fig)

col5, col6 = st.columns(2)
col7, col8 = st.columns(2)

with col5:
    container = col5.container(border=True)
    container.subheader('Distribuição por Índices')
    df_grouped = (
        df.groupby('Indexador')['Indexador'].value_counts().reset_index()
    )
    df_grouped.rename(columns={'count': 'Total de Ativos'}, inplace=True)
    fig = px.pie(
        df_grouped,
        values='Total de Ativos',
        names='Indexador',
        width=350,
        height=350,
    )
    fig.update_traces(textinfo='percent+label')
    fig.update_layout(separators=',.')
    container.plotly_chart(fig)

with col6:
    container = col6.container(border=True)
    container.subheader('Distribuição por Emissores')
    df_count = df['Emissor'].value_counts()
    df_grouped = df.groupby('Emissor')['Emissor'].value_counts().reset_index()
    df_grouped.rename(columns={'count': 'Total de Ativos'}, inplace=True)
    fig = px.pie(
        df_grouped,
        values='Total de Ativos',
        names='Emissor',
        width=350,
        height=350,
    )
    fig.update_layout(separators=',.')
    container.plotly_chart(fig)

with col7:
    container = col7.container(border=True)
    container.subheader('Prazos')
    df_filtered = df[['Emissor', 'Emissão', 'Vencimento']].reset_index()
    df_filtered['Emissão'] = pd.to_datetime(df_filtered['Emissão'])
    df_filtered['Vencimento'] = pd.to_datetime(df_filtered['Vencimento'])
    df_filtered['Diferença'] = (
        df_filtered['Vencimento'] - df_filtered['Emissão']
    ).dt.days / 365
    df_filtered['Diferença'] = df_filtered['Diferença'].apply(
        lambda v: f'{int(v)} anos' if int(v) > 1 else f'{int(v)} ano'
    )
    df_filtered = df_filtered.groupby('Diferença').count().reset_index()

    df_final = pd.DataFrame()
    df_final['Tempo'] = df_filtered['Diferença']
    df_final['Count'] = df_filtered['Emissor']
    df_final.rename(columns={'Count': 'Total de Ativos'}, inplace=True)
    fig = px.pie(
        df_final, values='Total de Ativos', names='Tempo', width=350, height=350
    )
    fig.update_traces(textinfo='percent+label')
    fig.update_layout(separators=',.')
    container.plotly_chart(fig)

with col8:
    container = col8.container(border=True)
    container.subheader('Top 5 Posições')
    sorted_df = df.sort_values('Saldo Bruto', ascending=False)
    top5_df = sorted_df[['Emissor', 'Indexador', 'Saldo Bruto']].head(5)
    top5_df = top5_df.set_index('Emissor')
    top5_df['Saldo Bruto'] = top5_df['Saldo Bruto'].apply(format_currency)
    container.table(top5_df, border=True)

st.subheader('Ativos')
columns = [
    'Emissor',
    'Tipo de Ativo',
    'Vencimento',
    'Liquidez',
    'Taxa',
    'Valor Compra',
    'Saldo Bruto',
    'Saldo Líquido',
    'IR',
]
st.dataframe(
    df[columns],
    column_config={
        'Taxa Média Ponderada': st.column_config.TextColumn('Taxa'),
        'Valor Compra': st.column_config.NumberColumn(
            'Valor Compra (R$)', format='localized'
        ),
        'Saldo Bruto': st.column_config.NumberColumn(
            'Saldo Bruto (R$)', format='localized'
        ),
        'Saldo Líquido': st.column_config.NumberColumn(
            'Saldo Líquido (R$)', format='localized'
        ),
        'IR': st.column_config.NumberColumn('IR (R$)', format='localized'),
    },
    hide_index=True,
)
