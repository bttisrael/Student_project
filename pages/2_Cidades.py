from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
from PIL import Image
import folium
import inflection
from streamlit_folium import folium_static

st.set_page_config(page_title='Cidades',page_icon = '🏙️', layout = 'wide')

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

st.header('Visão Cidades')
image_path='OIP.jpg'
image = Image.open(image_path)
st.sidebar.image(image, width = 120)
st.sidebar.markdown('# Fome Zero')

country_options = st.sidebar.multiselect('Escolha os Países que Deseja Visualizar as informações',['Brazil','England','Qatar','South Africa','Canada','Australia'],default = ['Brazil','England','Qatar','South Africa','Canada','Australia'])

linhas_selecionadas = df['country_description'].isin(country_options)
df = df.loc[linhas_selecionadas,:]

st.sidebar.markdown('##### Selecione a quantidade de Cidades')
data_slider = st.sidebar.slider('Até qual valor',value =20,min_value=1,max_value=20)

tab1,tab2,tab = st.tabs([' ',' ',' '])
with tab1:
    with st.container():
        st.markdown(f'### TOP {data_slider} CIDADES COM MAIS RESTAURANTES NA BASE DE DADOS')
        cols = ['restaurant_id','city','country_description']
        df_aux = df.loc[:,cols].groupby(['city','country_description']).count().sort_values('restaurant_id', ascending = False).reset_index().head(10)
        fig = px.bar(df_aux,x='city',y='restaurant_id',color = 'country_description',labels={'restaurant_id':'Quantidade de Restaurantes','city':'Cidades','country_description':'País'})
        st.plotly_chart(fig,use_container_width=True)
    with st.container():
        col1,col2 = st.columns(2)
        with col1:
            st.markdown(f'###### TOP {data_slider} CIDADES COM RESTAURANTES COM MÉDIA DE AVALIAÇÃO ACIMA DE 4')
            cols = ['restaurant_id','city','country_description']
            row = (df['aggregate_rating'] > 4)
            df_aux = df.loc[row,cols].groupby(['city','country_description']).count().sort_values('restaurant_id', ascending = False).reset_index().head(7)
            fig = px.bar(df_aux,x='city',y='restaurant_id',color = 'country_description',labels={'restaurant_id':'Quantidade de Restaurantes','city':'Cidades','country_description':'País'})
            st.plotly_chart(fig,use_container_width = True)
        with col2:
            st.markdown(f'###### TOP {data_slider} CIDADES COM RESTAURANTES COM MÉDIA DE AVALIAÇÃO ABAIXO DE 2.5')
            cols = ['restaurant_id','city','country_description']
            row = (df['aggregate_rating'] < 2.5)
            df_aux = df.loc[row,cols].groupby(['city','country_description']).count().sort_values('restaurant_id', ascending = False).reset_index().head(7)
            fig = px.bar(df_aux,x='city',y='restaurant_id',color = 'country_description',labels={'restaurant_id':'Quantidade de Restaurantes','city':'Cidades','country_description':'País'})
            st.plotly_chart(fig,use_container_width = True)

    with st.container():
        st.markdown(f'### TOP {data_slider} CIDADES COM MAIS RESTAURANTES COM TIPOS CULINÁRIOS DISTINTOS')
# Selecione as colunas relevantes
        cols = ['city', 'country_description', 'cuisines','restaurant_id']

# Agregue por cidade e conte tipos culinários únicos
        df_aux = df.loc[:, cols].groupby(['city', 'country_description']).agg({'cuisines': lambda x: len(set(x)), 'restaurant_id': 'count'}).reset_index()

# Renomeie as colunas para clareza
        df_aux.columns = ['city', 'country_description', 'unique_cuisines', 'restaurant_count']

# Ordene pelo número de tipos culinários únicos em ordem decrescente
        df_aux = df_aux.sort_values(by='unique_cuisines', ascending=False)

# Pegue as top 10 cidades
        df_top10 = df_aux.head(10)

# Crie o gráfico de barras
        fig = px.bar(df_top10, x='city', y='unique_cuisines', color='country_description', labels={'unique_cuisines': 'Quantidade de Tipos Culinários Distintos', 'city': 'Cidades', 'country_description': 'País'})

        st.plotly_chart(fig,use_container_width=True)

