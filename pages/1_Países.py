from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
from PIL import Image
import folium
import inflection
from streamlit_folium import folium_static

st.set_page_config(page_title='Países',page_icon = '🗺️', layout = 'wide')

df = pd.read_csv(r'dataset/zomato.csv')
## Limpeza e tratamento dos dados
def rename_columns(dataframe):
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    return df
df = rename_columns(df)
df.head()
# Corrigindo o problema
df["cuisines"] = df["cuisines"].apply(lambda x: str(x).split(",")[0] if pd.notna(x) else x)
df = df.drop_duplicates()
country_description = {
    1: "India",
    14: "Australia",
    30: "Brazil",
    37: "Canada",
    94: "Indonesia",
    148: "New Zealand",
    162: "Philippines",
    166: "Qatar",
    184: "Singapore",
    189: "South Africa",
    191: "Sri Lanka",
    208: "Turkey",
    214: "United Arab Emirates",
    215: "England",
    216: "United States of America",
}

# Adicionando a coluna "Country Description" usando map
df['country_description'] = df['country_code'].map(country_description)
price_type = {1:'cheap',
              2:'normal',
              3:'expensive',
              4:'gourmet',}
df['price_type'] = df['price_range'].map(price_type)

df = df.drop_duplicates()

st.header('Visão Países')
image_path='OIP.jpg'
image = Image.open(image_path)
st.sidebar.image(image, width = 120)
st.sidebar.markdown('# Fome Zero')

country_options = st.sidebar.multiselect('Escolha os Países que Deseja Visualizar as informações',['Brazil','England','Qatar','South Africa','Canada','Australia'],default = ['Brazil','England','Qatar','South Africa','Canada','Australia'])

linhas_selecionadas = df['country_description'].isin(country_options)
df = df.loc[linhas_selecionadas,:]

st.dataframe(df)

tab1,tab2,tab = st.tabs([' ',' ',' '])
with tab1:
    with st.container():
        st.markdown('### QUANTIDADE DE RESTAURANTES REGISTRADOS POR PÁIS')
        cols = ['restaurant_id','country_description']
    
    # selecão de linhas
        df_aux = df.loc[:,cols].groupby('country_description').nunique().sort_values('restaurant_id', ascending = False).reset_index()          
    
        fig = px.bar(df_aux, x='country_description', y ='restaurant_id', labels ={'country_description':'País','restaurant_id':'Quantidade de restaurantes'})
        st.plotly_chart(fig,use_container_width=True)
    with st.container():
        st.markdown('### QUANTIDADE DE CIDADES REGISTRADAS POR PÁIS')
        cols = ['city','country_description']
    
    # selecão de linhas
        df_aux = df.loc[:,cols].groupby('country_description').nunique().sort_values('city', ascending = False).reset_index()          
    
        fig = px.bar(df_aux, x='country_description', y ='city', labels={'country_description':'País','city':'Quantidade de cidades'})
        st.plotly_chart(fig,use_container_width=True)
    with st.container():
        col1,col2 = st.columns(2)
        with col1:
            st.markdown('###### MÉDIA DE AVALIAÇÕES FEITAS POR PAÍS')
            cols = ['votes','country_description']
            df_aux = df.loc[:,cols].groupby('country_description').mean().sort_values('votes', ascending = False).reset_index()
            fig = px.bar(df_aux,x='country_description',y='votes',labels={'country_description':'País','votes':'Quantidade de avaliações'})
            st.plotly_chart(fig,use_container_width = True)
        with col2:
            st.markdown('###### MÉDIA DE PREÇO DE UM PRATO PARA DUAS PESSOAS POR PAÍS')
            cols = ['average_cost_for_two','country_description']
            df_aux = df.loc[:,cols].groupby('country_description').mean().sort_values('average_cost_for_two', ascending = False).reset_index()
            fig = px.bar(df_aux,x='country_description',y='average_cost_for_two',labels={'country_description':'País','average_cost_for_two':'Preço de prato para duas pessoas'})
            st.plotly_chart(fig,use_container_width = True)

