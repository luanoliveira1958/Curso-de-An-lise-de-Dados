import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Home",
    page_icon=","
    
)

st.header('Marketplace - visão entregador')
#image_path = r'C:\Users\Luan\repos\ds_programaçao_python\dataset\dados.jpg'
image = Image.open('dados.jpg')
st.sidebar.image(image, width=220)
st.sidebar.markdown('# Cury Company' )
st.sidebar.markdown('## Fastest Delivery in town' )
st.sidebar.markdown("""___""")

st.write("# Curry Company Growth Dashboard" )
st.markdown(
    """
    Growth Dashboard foi construído para acompanhar as métricas de crescimento dos entregadores e empresas.
    ### Como utilizar esse Growth Dashboar?
        - Visão Empresa:
            -Visão Gerencial: Métricas gerais de comportamento.
            -Visão Tática: Indicadores semanais de crescimento.
            -Visão Geográfico: Insights de geolocalização.
        - Visão entregador:
            -Acompanhamento dos indicadores semanais de crescimento.
    ### Ask for Help
    - Time de Data Science no Discord
""")

