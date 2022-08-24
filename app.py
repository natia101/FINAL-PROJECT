from fcntl import F_SEAL_SEAL

import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go 
import re

st.set_page_config(
    page_title="Sistema de recomendación - Proyecto Final",
    page_icon="✅",
    layout="wide",
)

header = st.container()
dataset = st.container()
features = st.container()
#model = st.container()
interactive = st.container()
footer = st.container()

#@st.cache
def get_data() -> pd.DataFrame:
    return pd.read_csv(dataset_url)

def get_data_items() -> pd.DataFrame:
    return pd.read_csv(dataset_url_items)

def my_encode_units(x):
    if x <= 0:
        return 0
    if x >= 1:
        return 1    

with header:
    st.title("Sistema de recomendación")
    st.sidebar.header('Sistema de recomendación  Analisis de la Cesta de compra para el comercio minorista  Objetivo: las tecnicas de ML implementadas buscan brindar informacion a los comerciantes en cuanto a las asociaciones observadas en las ventas de productos, asi como en las reglas que operan para la rotacion de los mismos. Alcance: El analsis parte de una limpieza y adecuacion de los datos, posteriormente se crea y entrena el modelo para finalmente deployar a traves de Flask en una web que permita interactuar desde el lado del usuario de forma mas rapida y simple con el modelo Integrantes: Natia Lombardo Andrea Juarez Maria Gomez')
    #st.markdown('El algoritmo a priori es uno de los más utilizados en este tema y permite encontrar de forma eficiente conjuntos de ítems frecuentes, los cuales sirven de base para generar reglas de asociación entre los ítems.')

with features:
    st.header('Indicadores usados en las Reglas de Asociación')
    #st.markdown('')
    st.markdown('* Soporte: Nos indica cuantos productos son comprados del producto recomendado cada 100 vendidos del primer producto')
    st.markdown('* Confianza: Nos indica con que probabilidad puede ser comprado el segundo producto una vez comprado el primero')
    #st.markdown('Confianza(X=>Y)=Soporte(unión(X,Y)) /soporte(X)')

with dataset:
    dataset_url = "data/raw/reglas_de_asociacion.csv"
    dataset_url_items = "data/raw/Dataset_itemsset.csv"

with interactive:
    st.title('Lista de productos recomendados')
    df = get_data()

    df['primer_producto']=np.nan
    df['producto_recomendado']=np.nan

    for i in range(len(df)):
        df['primer_producto'][i] = re.sub(r'\W+',' ',re.search('({(.*)})', str(df.antecedents[i]))[0]).strip()
        df['producto_recomendado'][i] = re.sub(r'\W+',' ',re.search('({(.*)})', str(df.consequents[i]))[0]).strip()

    fig = go.Figure(data = [go.Table(
        header= dict(values=['Si compra','Se recomienda','% Soporte','% Confianza'],
        align = 'center'),
        cells = dict(values=[df.primer_producto,df.producto_recomendado,round(df.support*100,2),round(df.confidence*100,2)]))
    ])
    fig.show()
    st.write(fig)

    
    st.title('Productos mas vendidos')
    df = get_data_items()
    for i in range(len(df)):
        df['itemsets'][i] = re.sub(r'\W+',' ',re.search('({(.*)})', str(df.itemsets[i]))[0]).strip()
    
    df.sort_values(['support'],ascending=False,inplace=True)

    fig = go.Figure(data = [go.Table(
        header= dict(values= ['itemsets'],
        align = 'center'),
        cells = dict(values=[df.itemsets]))
    ])
    fig.show()
    st.write(fig)
    

with footer:
    st.write('Copyright')