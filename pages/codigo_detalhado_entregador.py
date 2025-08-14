from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import streamlit as st
from streamlit_folium import folium_static
import folium
from PIL import Image
from streamlit_lottie import st_lottie
import requests
import datetime

st.set_page_config( page_title='Visão Empresa', page_icon='',layout='wide')

df = pd.read_csv("train.csv")
df.head()

df1 = df.copy()

#Remover o 'NaN ' das colunas
linhas_selecionadas=df1['Delivery_person_ID']!= 'NaN '
df1.loc[linhas_selecionadas,:].copy()

linhas_selecionadas=df1['Delivery_person_Age']!= 'NaN '
df1.loc[linhas_selecionadas,:].copy()

linhas_selecionadas=df1['Delivery_person_Ratings']!= 'NaN '
df1.loc[linhas_selecionadas,:].copy()

linhas_selecionadas=df1['Restaurant_latitude']!= 'NaN '
df1.loc[linhas_selecionadas,:].copy()

linhas_selecionadas=df1['Restaurant_longitude']!= 'NaN '
df1.loc[linhas_selecionadas,:].copy()

linhas_selecionadas=df1['Delivery_location_latitude']!= 'NaN '
df1.loc[linhas_selecionadas,:].copy()

linhas_selecionadas=df1['Delivery_location_longitude']!= 'NaN '
df1.loc[linhas_selecionadas,:].copy()


linhas_selecionadas = df1['Time_taken(min)'] != 'NaN '
df1 = df1.loc[linhas_selecionadas,:].copy()

linhas_selecionadas = df1['Type_of_order'] != 'NaN '
df1 = df1.loc[linhas_selecionadas,:].copy()

linhas_selecionadas = df1['Type_of_vehicle'] != 'NaN '
df1 = df1.loc[linhas_selecionadas,:].copy()

linhas_selecionadas = df1['multiple_deliveries'] != 'NaN '
df1 = df1.loc[linhas_selecionadas,:].copy()


# Mantendo tudo que é diferente de "NaN ".
linhas_selecionadas = df1['Delivery_person_Age'] != 'NaN '
df1 = df1.loc[linhas_selecionadas, :].copy()
df1['Delivery_person_Age'] = df1['Delivery_person_Age'].replace(['NaN', 'NaN '], np.nan)
df1 = df1[df1['Delivery_person_Age'].notna()].copy()

linhas_selecionadas = df1['Road_traffic_density'] != 'NaN '
df1 = df1.loc[linhas_selecionadas,:].copy()



# Converter os tipos de colunas para string/float/ object
df1['Delivery_person_ID']=df1.loc[:,'Delivery_person_ID'].astype(str)
df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)
df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(int)
df1['Restaurant_latitude'] = df1['Restaurant_latitude'].astype(float)
df1['Restaurant_longitude'] = df1['Restaurant_longitude'].astype(float)
df1['Delivery_location_latitude'] = df1['Delivery_location_latitude'].astype(float)
df1['Delivery_location_longitude'] = df1['Delivery_location_longitude'].astype(float)
df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format = '%d-%m-%Y')




def extrair_tempo(valor):
    if pd.isna(valor):
        return np.nan  # mantém nulo
    valor = str(valor)
    if '(min) ' in valor:
        return valor.split('(min) ')[1]
    return valor  # se não achar, devolve o original

df1['Time_taken(min)'] = df1['Time_taken(min)'].apply(extrair_tempo).astype(float)



# Removendo os espaços dentro de strings /textos/ object
df1.loc[:,'ID'] = df1.loc[:,'ID'].str.strip()
df1.loc[:,'Road_traffic_density'] = df1.loc[:,'Road_traffic_density'].str.strip()
df1.loc[:,'Type_of_order'] = df1.loc[:,'Type_of_order'].str.strip()
df1.loc[:,'Type_of_vehicle'] = df1.loc[:,'Type_of_vehicle'].str.strip()
df1.loc[:,'Festival'] = df1.loc[:,'Festival'].str.strip()
df1.loc[:,'City'] = df1.loc[:,'City'].str.strip()
df1.loc[:,'Weatherconditions'] = df1.loc[:,'Weatherconditions'].str.strip()



# A quantidade de entregadores únicos
delivery_unique = len(df1.Delivery_person_ID.unique())
print("o número de entregadores únicos é: {}".format(delivery_unique))


#Layout no Streamlit
st.header('Marketplace - visão entregador')
#image_path = r'C:\Users\Luan\repos\ds_programaçao_python\dataset\dados.jpg'
image = Image.open('dados.jpg')
st.sidebar.image(image, width=220)
st.sidebar.markdown('# Cury Company' )
st.sidebar.markdown('## Fastest Delivery in town' )

st.sidebar.markdown('## Selecione uma data limite')

date_slider = st.sidebar.slider(
    'Até qual valor?',
     value=datetime.datetime( 2022, 4, 13),
     min_value=datetime.datetime(2022, 2, 11),
     max_value=datetime.datetime(2022, 4, 6),
     format='DD-MM-YYYY')

st.header(date_slider)

traffic_options = st.sidebar.multiselect(
    'Quais as condições do trânsito',
    ['Low', 'Medium', 'High', 'Jam'],
    default='Low')

#filtro de trânsito
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas, :]
st.dataframe(df1)

###############################################################
#Layout no Streamlit
###############################################################

tab1, tab2, tab3 = st.tabs(['# Visão Gerencial','_','_'])
with st.container():
    st.title('Overall Metrics')
    col1, col2, col3, col4 = st.columns(4, gap='large')
    with col1:
        maior_idade = df1.loc[:, 'Delivery_person_Age'].max()
        col1.metric('Maior de idade', maior_idade)
        
    with col2:
        menor_idade = df1.loc[:, 'Delivery_person_Age'].min()
        col2.metric('Menor de idade', menor_idade)
        
    with col3:
        melhor_condição = df1.loc[:, 'Vehicle_condition'].max()
        col3.metric('Melhor Condiçao', melhor_condição)
        
    with col4:
        pior_condição = df1.loc[:, 'Vehicle_condition'].min()
        col4.metric('Pior Condiçao', pior_condição)
        
with st.container():
    st.markdown("""___""")
    st.title('Avaliações')

    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Avaliações médias por Entregadores')
    with col2:
        st.subheader('Avaliação média por trânsito')
        st.subheader('Avaliação média por clim')
        
with st.container():
    st.markdown("""___""")
    st.title('Velocidade de Entrega')
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Avaliação medias por Entregador')
        df_avg_ratings_per_deliver = (df1.loc[:,['Delivery_person_Ratings','Delivery_person_ID']]
                                      .groupby('Delivery_person_ID')
                                      .mean()
                                      .reset_index())
        st.dataframe(df_avg_ratings_per_deliver)
                                      
    with col2:
        st.subheader('Top Entregadores mais lentos')
        df_avg_std_rating_by_traffic = (df1.loc[:,['Delivery_person_Ratings','Road_traffic_density']]
                                        .groupby('Road_traffic_density')
                                        .agg({'Delivery_person_Ratings':['mean','std']}))
        
        df_avg_std_rating_by_traffic.columns = ['delivery_mean','delivery_std']
        df_avg_std_rating_by_traffic = df_avg_std_rating_by_traffic.reset_index()
        st.dataframe(df_avg_std_rating_by_traffic)

        

        

        
        
        
        



        




    
