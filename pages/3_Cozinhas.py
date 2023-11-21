from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
from PIL import Image
import folium
import inflection
from streamlit_folium import folium_static

st.set_page_config(page_title='Cozinhas',page_icon = '🍱', layout = 'wide')

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

st.header('Visão Cozinhas')
image_path='OIP.jpg'
image = Image.open(image_path)
st.sidebar.image(image, width = 120)
st.sidebar.markdown('# Fome Zero')

country_options = st.sidebar.multiselect('Escolha os Países que Deseja Visualizar as informações',['Brazil','England','Qatar','South Africa','Canada','Australia'],default = ['Brazil','England','Qatar','South Africa','Canada','Australia'])

linhas_selecionadas = df['country_description'].isin(country_options)
df = df.loc[linhas_selecionadas,:]

st.sidebar.markdown('##### Selecione a quantidade de Restaurantes')
data_slider = st.sidebar.slider('Até qual valor',value =20,min_value=1,max_value=20)                    
                
st.markdown('#### Melhores restaurantes dos principais tipos culinários')


culinary_options = st.sidebar.multiselect('Escolha os tipos de culinária',['Italian', 'European', 'Filipino', 'American', 'Korean', 'Pizza',
       'Taiwanese', 'Japanese', 'Coffee', 'Chinese', 'Seafood',
       'Singaporean', 'Vietnamese', 'Latin American', 'Healthy Food',
       'Cafe', 'Fast Food', 'Brazilian', 'Argentine', 'Arabian', 'Bakery',
       'Tex-Mex', 'Bar Food', 'International', 'French', 'Steak',
       'German', 'Sushi', 'Grill', 'Peruvian', 'North Eastern',
       'Ice Cream', 'Burger', 'Mexican', 'Vegetarian', 'Contemporary',
       'Desserts', 'Juices', 'Beverages', 'Spanish', 'Thai', 'Indian',
       'Mineira', 'BBQ', 'Mongolian', 'Portuguese', 'Greek', 'Asian',
       'Author', 'Gourmet Fast Food', 'Lebanese', 'Modern Australian',
       'African', 'Coffee and Tea', 'Australian', 'Middle Eastern',
       'Malaysian', 'Tapas', 'New American', 'Pub Food', 'Southern',
       'Diner', 'Donuts', 'Southwestern', 'Sandwich', 'Irish',
       'Mediterranean', 'Cafe Food', 'Korean BBQ', 'Fusion', 'Canadian',
       'Breakfast', 'Cajun', 'New Mexican', 'Belgian', 'Cuban', 'Taco',
       'Caribbean', 'Polish', 'Deli', 'British', 'California',
       'Others', 'Eastern European', 'Creole', 'Ramen', 'Ukrainian',
       'Hawaiian', 'Patisserie', 'Yum Cha', 'Pacific Northwest', 'Tea',
       'Moroccan', 'Burmese', 'Dim Sum', 'Crepes', 'Fish and Chips',
       'Russian', 'Continental', 'South Indian', 'North Indian', 'Salad',
       'Finger Food', 'Mandi', 'Turkish', 'Kerala', 'Pakistani',
       'Biryani', 'Street Food', 'Nepalese', 'Goan', 'Iranian', 'Mughlai',
       'Rajasthani', 'Mithai', 'Maharashtrian', 'Gujarati', 'Rolls',
       'Momos', 'Parsi', 'Modern Indian', 'Andhra', 'Tibetan', 'Kebab',
       'Chettinad', 'Bengali', 'Assamese', 'Naga', 'Hyderabadi', 'Awadhi',
       'Afghan', 'Lucknowi', 'Charcoal Chicken', 'Mangalorean',
       'Egyptian', 'Malwani', 'Armenian', 'Roast Chicken', 'Indonesian',
       'Western', 'Dimsum', 'Sunda', 'Kiwi', 'Asian Fusion', 'Pan Asian',
       'Balti', 'Scottish', 'Cantonese', 'Sri Lankan', 'Khaleeji',
       'South African', 'Drinks Only', 'Durban', 'World Cuisine',
       'Izgara', 'Home-made', 'Giblets', 'Fresh Fish', 'Restaurant Cafe',
       'Kumpir', 'Döner', 'Turkish Pizza', 'Ottoman', 'Old Turkish Bars',
       'Kokoreç'],default = ['Italian', 'European', 'Filipino', 'American', 'Korean', 'Pizza',
       'Taiwanese', 'Japanese', 'Coffee', 'Chinese', 'Seafood',
       'Singaporean', 'Vietnamese', 'Latin American', 'Healthy Food',
       'Cafe', 'Fast Food', 'Brazilian', 'Argentine', 'Arabian', 'Bakery',
       'Tex-Mex', 'Bar Food', 'International', 'French', 'Steak',
       'German', 'Sushi', 'Grill', 'Peruvian', 'North Eastern',
       'Ice Cream', 'Burger', 'Mexican', 'Vegetarian', 'Contemporary',
       'Desserts', 'Juices', 'Beverages', 'Spanish', 'Thai', 'Indian',
       'Mineira', 'BBQ', 'Mongolian', 'Portuguese', 'Greek', 'Asian',
       'Author', 'Gourmet Fast Food', 'Lebanese', 'Modern Australian',
       'African', 'Coffee and Tea', 'Australian', 'Middle Eastern',
       'Malaysian', 'Tapas', 'New American', 'Pub Food', 'Southern',
       'Diner', 'Donuts', 'Southwestern', 'Sandwich', 'Irish',
       'Mediterranean', 'Cafe Food', 'Korean BBQ', 'Fusion', 'Canadian',
       'Breakfast', 'Cajun', 'New Mexican', 'Belgian', 'Cuban', 'Taco',
       'Caribbean', 'Polish', 'Deli', 'British', 'California',
       'Others', 'Eastern European', 'Creole', 'Ramen', 'Ukrainian',
       'Hawaiian', 'Patisserie', 'Yum Cha', 'Pacific Northwest', 'Tea',
       'Moroccan', 'Burmese', 'Dim Sum', 'Crepes', 'Fish and Chips',
       'Russian', 'Continental', 'South Indian', 'North Indian', 'Salad',
       'Finger Food', 'Mandi', 'Turkish', 'Kerala', 'Pakistani',
       'Biryani', 'Street Food', 'Nepalese', 'Goan', 'Iranian', 'Mughlai',
       'Rajasthani', 'Mithai', 'Maharashtrian', 'Gujarati', 'Rolls',
       'Momos', 'Parsi', 'Modern Indian', 'Andhra', 'Tibetan', 'Kebab',
       'Chettinad', 'Bengali', 'Assamese', 'Naga', 'Hyderabadi', 'Awadhi',
       'Afghan', 'Lucknowi', 'Charcoal Chicken', 'Mangalorean',
       'Egyptian', 'Malwani', 'Armenian', 'Roast Chicken', 'Indonesian',
       'Western', 'Dimsum', 'Sunda', 'Kiwi', 'Asian Fusion', 'Pan Asian',
       'Balti', 'Scottish', 'Cantonese', 'Sri Lankan', 'Khaleeji',
       'South African', 'Drinks Only', 'Durban', 'World Cuisine',
       'Izgara', 'Home-made', 'Giblets', 'Fresh Fish', 'Restaurant Cafe',
       'Kumpir', 'Döner', 'Turkish Pizza', 'Ottoman', 'Old Turkish Bars',
       'Kokoreç'])

linhas_selecionadas = df['cuisines'].isin(culinary_options)
df = df.loc[linhas_selecionadas,:]

tab1,tab2,tab = st.tabs([' ',' ',' '])
with tab1:
    with st.container():
        st.markdown(f'### TOP {data_slider} RESTAURANTES')
        df1 = df.loc[:,['restaurant_name','aggregate_rating','cuisines','votes','country_description','city']].groupby(['restaurant_name','cuisines','votes','country_description','city']).mean().sort_values('aggregate_rating',ascending = False).reset_index().head(data_slider)
        df1
        
    with st.container():
        col1,col2 = st.columns(2)
        with col1:
            st.markdown(f'###### TOP {data_slider} MELHORES TIPOS DE CULINÁIRIA')
            cols = ['aggregate_rating','cuisines']
            df_aux = df.loc[:,cols].groupby('cuisines').mean().sort_values('aggregate_rating',ascending = False).reset_index().head(data_slider)
            fig = px.bar(df_aux, x='cuisines',y='aggregate_rating', labels ={'cuisines':'Tipo de culinária','aggregate_rating':'Avaliação média'})
            st.plotly_chart(fig,use_container_width = True)
        with col2:
            st.markdown(f'###### TOP {data_slider} PIORES TIPOS DE CULINÁIRIA')
            cols = ['aggregate_rating','cuisines']
            df_aux = df.loc[:,cols].groupby('cuisines').mean().sort_values('aggregate_rating',ascending = True).reset_index().head(data_slider)
            fig = px.bar(df_aux, x='cuisines',y='aggregate_rating', labels ={'cuisines':'Tipo de culinária','aggregate_rating':'Avaliação média'} )
            st.plotly_chart(fig,use_container_width = True)


