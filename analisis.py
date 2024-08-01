# Imports
import bdd
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import analisis_10_flows
import analisis_20_calidad_aire
import analisis_30_estaciones
import analisis_32_incidencias
import analisis_33_meteo

'''array_df = [analisis_10_flows.df_flows, analisis_20_calidad_aire.df_calidad_aire, analisis_30_estaciones.df_estaciones,
analisis_32_incidencias.df_incidencias, analisis_33_meteo.df_humedad, analisis_33_meteo.df_temperatura, 
analisis_33_meteo.df_superficial_wetting, analisis_33_meteo.df_visibilidad, analisis_33_meteo.df_precipitaciones,
analisis_33_meteo.df_velocidad_media_viento, analisis_33_meteo.df_direccion_viento]'''
array_df = [analisis_33_meteo.df_humedad, analisis_33_meteo.df_temperatura, 
analisis_33_meteo.df_superficial_wetting, analisis_33_meteo.df_visibilidad, analisis_33_meteo.df_precipitaciones,
analisis_33_meteo.df_velocidad_media_viento, analisis_33_meteo.df_direccion_viento]
# ------------------------------- ANALISIS EXPLORATORIO COMUN ------------------------------------------ #

# Obtencion de informacion general de cada coleccion
for array in array_df:
    # Visualizar las primeras lineas del df
    print(array.head())
    print('------------------------------------------------------------------------')

    # Estrcutura del conjunto de datos
    print(array.shape)
    print('------------------------------------------------------------------------')
'''
    # Informacion detallada del conjunto de datos
    print(array.info())
    print('------------------------------------------------------------------------')

    # Descripcion del conjunto de datos
    print(array.describe())
    print('------------------------------------------------------------------------')

    # Se obtienen las columnas del conjunto de datos
    columnas = list(array.columns)
    # Bucle para cada columna
    for columna in columnas:
        print(array[columna].value_counts())

    # DF con unicamente variables numericas
    array_num = array.select_dtypes(include=['int', 'float'])
    # Definir matriz de correlacion
    matriz_corr = array_num.corr()
    # Definir tamaño de la figura
    plt.figure(figsize=(10, 8))
    # Estilo
    sns.heatmap(matriz_corr, annot=True, cmap='coolwarm')
    # Añadir titulo
    plt.title('Matriz de Correlacion')
    # Dibujar
    plt.show()'''

# ------------------------------------- FLOWS ------------------------------------------ #
#analisis_10_flows.analisis_flows()

# ---------------------------------- CALIDAD AIRE -------------------------------------- #
#analisis_20_calidad_aire.analisis_calidad_aire()

# ---------------------------------- INCIDENCIAS --------------------------------------- #
#analisis_32_incidencias.analisis_incidencias()

# ------------------------------------- METEO ------------------------------------------ #
analisis_33_meteo.analisis_meteo()