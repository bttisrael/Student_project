import streamlit as st
from PIL import Image
import os
from folium.plugins import MarkerCluster
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
import folium
import inflection
from streamlit_folium import folium_static

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


st.set_page_config(
    page_title="Home",page_icon = "📊", layout='wide'
)

image_path = ('OIP.jpg')
image = Image.open(image_path)
st.sidebar.image(image, width=120)

st.sidebar.markdown('# Fome Zero')
st.sidebar.markdown('## Conheça os melhores restaurantes do mundo')
st.sidebar.markdown("""---""")
st.write("# Fome Zero Company Dashboard ")
st.write("Esse Dashboard foi construído para acompanhar os principais indicadores da Fome Zero")

st.write("""#### Como utilizo o Dashboard?
            - Países: Insights sobre cidades, restaurantes e avaliações de cada país da base de dados
    - Cidades: Médias de avaliação e tipos de culinária agrupados pelas principais cidades
    - Cozinhas: Aqui é possível selecionar os tipos de culinária e também a quantidade de restaurantes para avaliar o desempenho dos mesmos
    ### Ask for help
    - israelburatto@gmail.com
    ### Powered by Israel Buratto""")
country_options = st.sidebar.multiselect('Escolha os Países que Deseja Visualizar as informações',['Brazil','England','Qatar','South Africa','Canada','Australia'],default = ['Brazil','England','Qatar','South Africa','Canada','Australia'])

linhas_selecionadas = df['country_description'].isin(country_options)
df = df.loc[linhas_selecionadas,:]

data = df.loc[:,['latitude','longitude','restaurant_id','city','country_description']]
df = pd.DataFrame(data)

# Crie um mapa centrado na primeira localização do DataFrame
m = folium.Map(location=[df['latitude'].iloc[0], df['longitude'].iloc[0]], zoom_start=1)

# Crie clusters para agrupar os marcadores
marker_cluster = MarkerCluster().add_to(m)

# Adicione marcadores para cada restaurante no DataFrame
for i, row in df.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Restaurante {row['restaurant_id']}",
        tooltip=f"{row['restaurant_id']} - {row['city']}, {row['country_description']}"
    ).add_to(marker_cluster)
st.markdown('<h1>Mapa de Restaurantes</h1>', unsafe_allow_html=True)
folium_static(m)
