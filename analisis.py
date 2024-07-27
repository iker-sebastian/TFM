# Imports
import bdd
import pandas as pd

import analisis_10_flows
import analisis_20_calidad_aire
import analisis_30_estaciones
import analisis_32_incidencias
import analisis_33_meteo

array_df = [analisis_10_flows.df_flows, analisis_20_calidad_aire.df_calidad_aire, analisis_30_estaciones.df_estaciones, analisis_32_incidencias.df_incidencias, analisis_33_meteo.df_meteo] 

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

# ------------------------------------- FLOWS ------------------------------------------ #
analisis_10_flows.analisis_flows()

# ---------------------------------- CALIDAD AIRE -------------------------------------- #
analisis_20_calidad_aire.analisis_calidad_aire()

# ---------------------------------- INCIDENCIAS --------------------------------------- #
analisis_32_incidencias.analisis_incidencias()

# ------------------------------------- METEO ------------------------------------------ #
analisis_33_meteo.analisis_meteo()