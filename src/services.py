import streamlit as st
import pandas as pd
from src import settings
from datetime import datetime


DAY_IN_SECONDS = 86400


@st.cache_data(ttl=DAY_IN_SECONDS)
def get_selic_rate():
    now = datetime.now()
    start_date = now.replace(year=now.year - 10).strftime('%d/%m/%Y')

    try:
        df = pd.read_json(f'{settings.SELIC_API_URL}?dataInicial={start_date}')
        current_value = float(df['valor'].iloc[-1])
        max_value = float(df['valor'].max())

        if max_value < 1:
            max_value = current_value

        return current_value, max_value
    except Exception:
        current_value = float(settings.DEFAULT_SELIC_RATE)
        max_value = float(settings.DEFAULT_SELIC_MAX_RATE)

        if max_value < 1:
            max_value = current_value

        return current_value, max_value


@st.cache_data(ttl=DAY_IN_SECONDS)
def get_ipca_rate():
    try:
        df = pd.read_json(settings.IPCA_API_URL)
        current_value = float(df['valor'].iloc[-1])
        max_value = float(df['valor'].max())

        if max_value < 1:
            max_value = current_value

        return current_value, max_value
    except Exception:
        current_value = float(settings.DEFAULT_IPCA_RATE)
        max_value = float(settings.DEFAULT_IPCA_MAX_RATE)

        if max_value < 1:
            max_value = current_value

        return current_value, max_value
