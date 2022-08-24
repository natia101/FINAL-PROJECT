import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go 

st.set_page_config(
    page_title="Sistema de recomendación - Proyecto Final",
    page_icon="✅",
    layout="wide",
)

header = st.container()
dataset = st.container()
features = st.container()
model = st.container()
interactive = st.container()
footer = st.container()

@st.cache
def get_data() -> pd.DataFrame:
    return pd.read_csv(dataset_url)

def get_data_items() -> pd.DataFrame:
    return pd.read_csv(dataset_url_items)

with header:
    st.title("Sistema de recomendación")
    st.sidebar.header('Sistema de recomendación')
    st.markdown('El algoritmo a priori es uno de los más utilizados en este tema y permite encontrar de forma eficiente conjuntos de ítems frecuentes, los cuales sirven de base para generar reglas de asociación entre los ítems.')

with dataset:
    st.header('Reglas de Asociación')
    st.markdown('Conceptos: ')
    st.markdown('* Soporte: El soporte del ítem es el número de transacciones que contienen X dividido entre el total de transacciones.')
    st.markdown('* Confianza: La confianza de una regla “Si X entonces Y” se define acorde a la ecuación')
    st.markdown('Confianza(X=>Y)=Soporte(unión(X,Y)) /soporte(X)')

    dataset_url = "../data/raw/reglas_de_asociacion.csv"
    dataset_url_items = "../data/raw/Dataset_itemsset.csv"

    #st.subheader('')

with interactive:
    st.title('La reglas')
    df = get_data()
    #st.table(df)
    fig = go.Figure(data = [go.Table(
        header= dict(values=list(df[['antecedents','consequents','support','confidence','lift','leverage','conviction']].columns),
        align = 'center'),
        cells = dict(values=[df.antecedents,df.consequents,round(df.support,2),round(df.confidence,2),round(df.lift,2),round(df.leverage,2),round(df.conviction,2)]))
    ])
    fig.show()
    st.write(fig)

    st.title('Los items')
    df = get_data_items()
    #st.table(df)
    fig = go.Figure(data = [go.Table(
        header= dict(values=list(df[['support','itemsets']].columns),
        align = 'center'),
        cells = dict(values=[round(df.support,2),df.itemsets]))
    ])
    fig.show()
    st.write(fig)




with footer:
    st.write('Fin')