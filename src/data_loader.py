import pandas as pd
import streamlit as st
from pathlib import Path
from src import settings
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.media import File


@st.cache_data
def get_data():
    file_path = (
        Path(__file__).parent.parent / 'data' / settings.DATA_SOURCE_NAME
    )

    if not file_path.is_file():
        return None

    return pd.read_csv(file_path)


def set_data(file_content):
    agent = Agent(model=OpenAIChat(id='gpt-5-mini'), markdown=True)

    data = agent.run(
        """
            Você é um agente responsável por extrair dados de arquivos.
            No arquivo anexado eu preciso que você extraia os ativos de renda fixa somente,
            e organize eles em formado CSV.

            Gere o CSV com as seguintes colunas:

            '''
            - Emissor
            - Ativo
            - Tipo de Ativo
            - Emissão
            - Vencimento
            - Liquidez
            - Carência
            - Taxa
            - Indexador
            - Quantidade
            - Preço
            - Valor Compra
            - Saldo Bruto
            - Saldo Líquido
            - IR
            - IOF
            '''

            Algumas observações:
                - A coluna "Liquizes" deve ter os valores 'Sim' ou 'Não'.
                - A coluna "Tipo de Ativo" deve conter valores como CDB, LCI, LCA, CRI, etc... .
                - A coluna "Indexador" deve conter um dos três valores: CDI, IPCA ou PRÉ.
                - A coluna "Taxa" deve conter o valor da taxa limpo (Ex: 13, 8.4, 5)

            Me responda somente com o conteúdo do CSV, nenhuma outra mensagem deve ser retornada.
        """,
        files=[
            File(
                content=file_content,
                mime_type='application/pdf',
                filename='extrato.pdf',
            )
        ],
    )

    file_path = (
        Path(__file__).parent.parent / 'data' / settings.DATA_SOURCE_NAME
    )

    with open(file_path, 'w') as file:
        file.write(data.content)

    st.cache_data.clear()
