import streamlit as st
from src import settings
from src.data_loader import get_data
from src.services import get_selic_rate, get_ipca_rate
from src.utils import format_float_number


def main():
    st.set_page_config(
        layout='wide', page_title=settings.APP_NAME, page_icon='📊'
    )

    with st.sidebar.container(border=True):
        with st.spinner('Carregando...'):
            selic, max = get_selic_rate()
        st.markdown(f'**🏛️ Selic:** `{format_float_number(selic)}%`')
        st.progress(
            selic / max,
            text=f'Nível da Taxa (Máx: {format_float_number(max)}%)',
        )

    with st.sidebar.container(border=True):
        with st.spinner('Carregando...'):
            ipca, max = get_ipca_rate()
        st.markdown(f'**🛒 IPCA:** `{format_float_number(ipca)}%`')
        st.progress(
            ipca / max,
            text=f'Nível da Inflação (Máx: {format_float_number(max)}%)',
        )

    st.sidebar.markdown(
        '#### Desenvolvidor por [Daniel Fagundes](https://danielfagundes.me)'
    )

    df = get_data()
    if df is None:
        st.write('Oops! Nenhum dado encontrao.')
        return

    dashboard_page = st.Page(
        'pages/dashboard.py', title='Dashboard', icon='🏠', default=True
    )
    flow_page = st.Page('pages/flow.py', title='Prazos', icon='📅')
    income_page = st.Page('pages/income.py', title='Performance', icon='📈')
    ensurance_page = st.Page('pages/ensurance.py', title='Proteção', icon='🛡')

    page = st.navigation(
        [dashboard_page, flow_page, income_page, ensurance_page]
    )

    page.run()


if __name__ == '__main__':
    main()
