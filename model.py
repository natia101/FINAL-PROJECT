pip install pandas


# Cargamos las librerias
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

from plotly.offline import plot, iplot, init_notebook_mode
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import pairwise_distances

from funpymodeling.exploratory import freq_tbl
from plotly.offline import plot, iplot, init_notebook_mode

# Cargamos los datos

dataset=pd.read_csv('../data/raw/Assignment-1_Data.csv',sep=';')

# Limpiamos los datos

dataset['Itemname'] = dataset['Itemname'].str.strip() # aca estamos remobiendo los espacios
dataset.dropna(axis=0, subset=['BillNo'], inplace=True) # elimino los na en las boletas
dataset.dropna(axis=0, subset=['CustomerID'], inplace=True) # elimino los na en los id de los clientes 
dataset['BillNo'] = dataset['BillNo']. astype('str') # convertimos el numero de boleta en string
dataset = dataset[~dataset['BillNo'].str.contains('C')] # removemos las posibles transacciones realizadas a credito
dataset.head()

# Creamos el segundo dataset solo con los datos de Alemania
from itertools import groupby
dataset_germany = (dataset[dataset['Country']== "Germany"].groupby(['BillNo', 'Itemname'])['Quantity'].sum().unstack().reset_index().fillna(0).set_index('BillNo'))


#Vamos a definir una funcion que convertira todos los cero o menores que cero a cero y si son mayores a 1 en 1, 
# esto lo hacemos porque es lo que el algoritmo usa o espera como entrada

def my_encode_units(x):
    if x <= 0:
        return 0
    if x >= 1:
        return 1

dataset_germany_set = dataset_germany.applymap(my_encode_units)
dataset_germany_set.drop('POSTAGE', inplace=True, axis=1)

df = dataset_germany_set.copy()

#Generamos la frecuencia de los items
df_itemsset = apriori(df, min_support=0.07, use_colnames=True)

# Creamos las reglas de asociacion
my_rules = association_rules(df_itemsset, metric='lift', min_threshold=1)

# Viasualizamos el top de las 100 reglas o normas de asociacion

my_rules.head(100)

my_rules[(my_rules['lift'] >= 3) & (my_rules['confidence'] >= 0.3)]

