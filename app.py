import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go 
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
model = st.container()
interactive = st.container()
footer = st.container()

@st.cache
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

with model:
    data=pd.read_csv('data/raw/Assignment-1_Data.csv',sep=';')
    st.title('El modelo')
    # Limpiamos los datos

    data['Itemname'] = data['Itemname'].str.strip() # aca estamos remobiendo los espacios
    data.dropna(axis=0, subset=['BillNo'], inplace=True) # elimino los na en las boletas
    data.dropna(axis=0, subset=['CustomerID'], inplace=True) # elimino los na en los id de los clientes 
    data['BillNo'] = data['BillNo']. astype('str') # convertimos el numero de boleta en string
    data = data[~data['BillNo'].str.contains('C')] # removemos las posibles transacciones realizadas a credito
    #data.head()

    # Creamos el segundo dataset solo con los datos de Alemania
    from itertools import groupby
    dataset_germany = (data[data['Country']== "Germany"].groupby(['BillNo', 'Itemname'])['Quantity'].sum().unstack().reset_index().fillna(0).set_index('BillNo'))

    #Vamos a definir una funcion que convertira todos los cero o menores que cero a cero y si son mayores a 1 en 1, 
    # esto lo hacemos porque es lo que el algoritmo usa o espera como entrada

    dataset_germany_set = dataset_germany.applymap(my_encode_units)
    dataset_germany_set.drop('POSTAGE', inplace=True, axis=1)

    df = dataset_germany_set.copy()

    #Generamos la frecuencia de los items
    df_itemsset = apriori(df, min_support=0.07, use_colnames=True)

    # Creamos las reglas de asociacion
    my_rules = association_rules(df_itemsset, metric='lift', min_threshold=1)

    # Viasualizamos el top de las 100 reglas o normas de asociacion

    #my_rules.head(100)

    #my_rules[(my_rules['lift'] >= 3) & (my_rules['confidence'] >= 0.3)]   


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