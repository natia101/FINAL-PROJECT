from fcntl import F_SEAL_SEAL
from pickle import FALSE
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go 
import re

from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

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
    st.sidebar.header('Sistema de recomendación')
    #st.markdown('El algoritmo a priori es uno de los más utilizados en este tema y permite encontrar de forma eficiente conjuntos de ítems frecuentes, los cuales sirven de base para generar reglas de asociación entre los ítems.')

with features:
    st.header('Reglas de Asociación')
    st.markdown('Conceptos: ')
    st.markdown('* Soporte: El soporte del ítem es el número de transacciones que contienen X dividido entre el total de transacciones.')
    st.markdown('* Confianza: La confianza de una regla “Si X entonces Y” se define acorde a la ecuación')
    st.markdown('Confianza(X=>Y)=Soporte(unión(X,Y)) /soporte(X)')

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
    #st.table(df)
    
    df.sort_values(['support'],ascending=False,inplace=True)

    fig = go.Figure(data = [go.Table(
        header= dict(values= ['itemsets'],
        align = 'center'),
        cells = dict(values=[df.itemsets]))
    ])
    fig.show()
    st.write(fig)
    

with footer:
    st.write('Fin')