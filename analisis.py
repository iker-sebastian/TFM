# Imports
import bdd
import pandas as pd

import analisis_10_flows
import analisis_20_calidad_aire
import analisis_30_meteo
import analisis_32_incidencias

# Obtener todos los datos de las colecciones de MongoDB
dataset_estaciones = list(bdd.coleccion_estaciones.find())

# Crear los df
df_estaciones = pd.DataFrame(dataset_estaciones)

#array_df = [df_estaciones, analisis_20_calidad_aire.df_calidad_aire, analisis_10_flows.df_flows, df_incidencias, analisis_30_meteo.df_meteo] 
array_df = [analisis_32_incidencias.df_incidencias]

# ------------------------------- ANALISIS EXPLORATORIO COMUN ------------------------------------------ #

# Obtención de información general de cada colección
for array in array_df:
    # Visualizar las primeras lineas del df
    print(array.head())
    print('------------------------------------------------------------------------')

    # Estrcutura del conjunto de datos
    print(array.shape)
    print('------------------------------------------------------------------------')

    # Información detallada del conjunto de datos
    print(array.info())
    print('------------------------------------------------------------------------')

    # Descripción del conjunto de datos
    print(array.describe())
    print('------------------------------------------------------------------------')

    # Se obtienen las columnas del conjunto de datos
    columnas = list(array.columns)
    # Bucle para cada columna
    for columna in columnas:
        print(array[columna].value_counts())

# ---------------------------------- CALIDAD AIRE -------------------------------------- #
#analisis_20_calidad_aire.analisis_calidad_aire()

# ------------------------------------- FLOWS ------------------------------------------ #
#analisis_10_flows.analisis_flows()

# ------------------------------------- METEO ------------------------------------------ #
#analisis_30_meteo.analisis_meteo()

# ---------------------------------- INCIDENCIAS --------------------------------------- #
analisis_32_incidencias.analisis_incidencias()