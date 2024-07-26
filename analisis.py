# Imports
import bdd
import pandas as pd

import analisis_10_flows
import analisis_20_calidad_aire
import analisis_30_meteo

# Obtener todos los datos de las colecciones de MongoDB
dataset_estaciones = list(bdd.coleccion_estaciones.find())
dataset_incidencias = list(bdd.coleccion_incidencias.find())

'''dataset_meteo_humedad = list(bdd.coleccion_meteo_aire_humedad.find())
dataset_meteo_temperatura = list(bdd.coleccion_meteo_aire_temperatura.find())
dataset_meteo_humedad_superficie = list(bdd.coleccion_meteo_atm_humedad_superficie.find())
dataset_meteo_visibilidad = list(bdd.coleccion_meteo_atm_visibilidad.find())
dataset_meteo_precipitaciones = list(bdd.coleccion_meteo_precipitaciones.find())
dataset_meteo_viento_vel_media = list(bdd.coleccion_meteo_viento_vel_media.find())
dataset_meteo_viento_direccion = list(bdd.coleccion_meteo_viento_direccion_sigma.find())'''

# Crear los df
df_estaciones = pd.DataFrame(dataset_estaciones)
df_incidencias = pd.DataFrame(dataset_incidencias)

'''df_meteo_humedad = pd.DataFrame(dataset_meteo_humedad)
df_meteo_temperatura = pd.DataFrame(dataset_meteo_temperatura)
df_meteo_humedad_superficie = pd.DataFrame(dataset_meteo_humedad_superficie)
df_meteo_visibilidad= pd.DataFrame(dataset_meteo_visibilidad)
df_meteo_precipitaciones = pd.DataFrame(dataset_meteo_precipitaciones)
df_meteo_viento_vel_media = pd.DataFrame(dataset_meteo_viento_vel_media)
df_meteo_viento_direccion = pd.DataFrame(dataset_meteo_viento_direccion)'''

#array_df = [df_estaciones, analisis_20_calidad_aire.df_calidad_aire, analisis_10_flows.df_flows, df_incidencias, df_meteo] # df_meteo_humedad, df_meteo_temperatura, df_meteo_humedad_superficie, df_meteo_visibilidad, df_meteo_precipitaciones, df_meteo_viento_vel_media, df_meteo_viento_direccion
array_df = [analisis_30_meteo.df_meteo]

# ------------------------------- ANALISIS EXPLORATORIO COMUN ------------------------------------------ #

# Obtención de información general de cada colección
for array in array_df:
    # Visualizar las primeras lineas del df
    print(array.head())
    print("------------------------------------------------------------------------")

    # Estrcutura del conjunto de datos
    print(array.shape)
    print("------------------------------------------------------------------------")

    # Información detallada del conjunto de datos
    print(array.info())
    print("------------------------------------------------------------------------")

    # Descripción del conjunto de datos
    print(array.describe())
    print("------------------------------------------------------------------------")

    # Se obtienen las columnas del conjunto de datos
    columnas = list(array.columns)
    # Bucle para cada columna
    for columna in columnas:
        print(array[columna].value_counts())

# ------------------------------- CALIDAD AIRE ------------------------------------------ #
#analisis_20_calidad_aire.analisis_calidad_aire()

# ------------------------------- FLOWS ------------------------------------------ #
#analisis_10_flows.analisis_flows()

# ------------------------------- METEO ------------------------------------------ #
analisis_30_meteo.analisis_meteo()