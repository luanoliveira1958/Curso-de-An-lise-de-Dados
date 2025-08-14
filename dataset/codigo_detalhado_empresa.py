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
image_path = r'C:\Users\Luan\repos\ds_programaçao_python\dataset\dados.jpg'
image = Image.open(image_path)
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

tab1, tab2, tab3 = st.tabs(['# Visão Gerencial','# Visão Tática','# Visão Geográfica'])
with tab1:
    with st.container():
        st.markdown('# Orders by Day')
        cols = ['ID','Order_Date']
        df_aux = df1.loc[:, cols].groupby('Order_Date').count().reset_index()
        fig = px.bar(df_aux, x='Order_Date', y='ID' )
        st.plotly_chart( fig, use_container_width= True  )

    with st.container():
         col1, col2 = st.columns(2)
         with col1:
             st.header("Traffic Order Share")
             df_aux = df1.loc[:,['ID','Road_traffic_density']].groupby('Road_traffic_density').count().reset_index()
             df_aux = df_aux.loc[df_aux['Road_traffic_density']!="NaN ",:]
             df_aux['entregas_perc'] = df_aux['ID'] / df_aux['ID'].sum()
             fig = px.pie(df_aux, values='entregas_perc', names='Road_traffic_density' )
             st.plotly_chart(fig, use_container_with=True)

         with col2:
             st.header("Traffic Order City")
             df_aux = df1.loc[:,['ID','City','Road_traffic_density']].groupby(['City','Road_traffic_density']).count().reset_index()
             df_aux = df_aux.loc[df_aux['City']!="NaN ",:]
             df_aux = df_aux.loc[df_aux['Road_traffic_density']!="NaN ",:]
             fig = px.scatter(df_aux, x='City', y='Road_traffic_density', size='ID', color='City' )
             st.plotly_chart(fig, use_container_with=True)

with tab2:
     with st.container():
        st.markdown("#teste02")
        df1['week_of_year'] = df1['Order_Date'].dt.strftime('%U' )
        df_aux = df1.loc[:, ['ID','week_of_year']].groupby('week_of_year').count().reset_index()
        fig = px.line(df_aux, x='week_of_year', y='ID' )  # Cria o gráfico normalmente
        st.plotly_chart(fig, use_container_width=True)  # Exibe o gráfico com ajuste ao container
         
     with st.container():
        st.markdown("#Order Share by Week")
        df_aux1 = df1.loc[:, ['ID','week_of_year']].groupby('week_of_year' ).count().reset_index()
        df_aux2 = df1.loc[:, ['Delivery_person_ID','week_of_year']].groupby('week_of_year').nunique().reset_index()
        df_aux = pd.merge(df_aux1, df_aux2, how='inner', on='week_of_year')
        df_aux['order_by_delivery'] = df_aux['ID'] / df_aux['Delivery_person_ID']
        fig = px.line(df_aux, x='week_of_year', y='order_by_delivery')
        st.plotly_chart(fig, use_container_width= True)

with tab3:
    st.markdown("# Country Maps")
    df_aux = df1.loc[:,['City','Road_traffic_density','Delivery_location_latitude','Delivery_location_longitude']].groupby(['City','Road_traffic_density']).median().reset_index()
    df_aux = df_aux.loc[df_aux['City']!='NaN', :]
    df_aux = df_aux.loc[df_aux['Road_traffic_density']!='NaN', :]
    map = folium.Map()
    for index, location_info in df_aux.iterrows():
        folium.Marker([location_info['Delivery_location_latitude'],
                       location_info['Delivery_location_longitude']],
                       popup = location_info[['City','Road_traffic_density']]).add_to(map)
    folium_static(map, width=1024, height=600)             












