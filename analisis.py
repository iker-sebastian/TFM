# Imports
import bdd
import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Obtener todos los datos de las colecciones de MongoDB
dataset_estaciones = list(bdd.coleccion_estaciones.find())
dataset_calidad_aire = list(bdd.coleccion_calidad_aire.find())
'''dataset_flows = list(bdd.coleccion_flows.find())
dataset_incidencias = list(bdd.coleccion_incidencias.find())
dataset_meteo_humedad = list(bdd.coleccion_meteo_aire_humedad.find())
dataset_meteo_temperatura = list(bdd.coleccion_meteo_aire_temperatura.find())
dataset_meteo_humedad_superficie = list(bdd.coleccion_meteo_atm_humedad_superficie.find())
dataset_meteo_visibilidad = list(bdd.coleccion_meteo_atm_visibilidad.find())
dataset_meteo_precipitaciones = list(bdd.coleccion_meteo_precipitaciones.find())
dataset_meteo_viento_vel_media = list(bdd.coleccion_meteo_viento_vel_media.find())
dataset_meteo_viento_direccion = list(bdd.coleccion_meteo_viento_direccion_sigma.find())'''

# Crear los df
df_estaciones = pd.DataFrame(dataset_estaciones)
df_calidad_aire = pd.DataFrame(dataset_calidad_aire)
'''df_flows = pd.DataFrame(dataset_flows)
df_incidencias = pd.DataFrame(dataset_incidencias)
df_meteo_humedad = pd.DataFrame(dataset_meteo_humedad)
df_meteo_temperatura = pd.DataFrame(dataset_meteo_temperatura)
df_meteo_humedad_superficie = pd.DataFrame(dataset_meteo_humedad_superficie)
df_meteo_visibilidad= pd.DataFrame(dataset_meteo_visibilidad)
df_meteo_precipitaciones = pd.DataFrame(dataset_meteo_precipitaciones)
df_meteo_viento_vel_media = pd.DataFrame(dataset_meteo_viento_vel_media)
df_meteo_viento_direccion = pd.DataFrame(dataset_meteo_viento_direccion)'''

#array_df = [df_estaciones, df_calidad_aire, bdd.df_flows, bdd.df_incidencias, bdd.df_meteo_humedad, bdd.df_meteo_temperatura, bdd.df_meteo_humedad_superficie, bdd.df_meteo_visibilidad, bdd.df_meteo_precipitaciones, bdd.df_meteo_viento_vel_media, bdd.df_meteo_viento_direccion]
array_df = [df_estaciones, df_calidad_aire]

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
'''
# Rellenar valores nulos con 0
df_calidad_aire.fillna(0, inplace=True)

# Regresion lineal
modelo_LR = LinearRegression()

# Red neuronal
modelo_RN = Sequential()
modelo_RN.add(Dense(256, activation='relu', input_dim=5))
modelo_RN.add(Dense(128, activation='relu'))
modelo_RN.add(Dense(128, activation='relu'))
modelo_RN.add(Dense(1))
# Compilar modelo
modelo_RN.compile(optimizer='adam', loss='mse', metrics=['mae'])
# Resumen del modelo
modelo_RN.summary()


# Bucle de predicción para cada estacion
for id_estacion in df_calidad_aire['id_estacion'].unique():
    filtro_estacion = df_calidad_aire[df_calidad_aire['id_estacion'] == id_estacion]

    # ---------------------------------------- Prediccion SO2 ----------------------------------------- #
    X_SO2 = filtro_estacion[['PM2,5', 'PM10', 'O3 8h', 'Tolueno', 'NOX']]
    Y_SO2 = filtro_estacion['SO2']

    # Division de datos
    X_SO2_train, X_SO2_test, Y_SO2_train, Y_SO2_test = train_test_split(X_SO2, Y_SO2, test_size=0.2)

    # Regresion lineal
    modelo_LR.fit(X_SO2_train, Y_SO2_train)
    # Red neuronal
    modelo_RN.fit(X_SO2_train, Y_SO2_train, epochs=500, batch_size=10)

    # Evaluación
    mse_RN_SO2, mae_RN_SO2 = modelo_RN.evaluate(X_SO2_test, Y_SO2_test)

    # Prediccion
    prediccion_LR_SO2 = modelo_LR.predict(X_SO2_test)
    prediccion_RN_SO2 = modelo_RN.predict(X_SO2_test)

    # Valor unico
    pred_LR_SO2 = prediccion_LR_SO2[0]
    pred_RN_SO2 = prediccion_RN_SO2[0][0]

    # Metricas
    mae_LR_SO2 = mean_absolute_error(Y_SO2_test, prediccion_LR_SO2)
    mse_LR_SO2 = mean_squared_error(Y_SO2_test, prediccion_LR_SO2)
    r2_LR_SO2 = r2_score(Y_SO2_test, prediccion_LR_SO2)
    r2_RN_SO2 = r2_score(Y_SO2_test, prediccion_RN_SO2)

    # ----------------------------------------- Prediccion PM25 ------------------------------------------ #
    X_PM25 = filtro_estacion[['SO2', 'PM10', 'O3 8h', 'Tolueno', 'NOX']]
    Y_PM25 = filtro_estacion['PM2,5']

    # Division de datos
    X_PM25_train, X_PM25_test, Y_PM25_train, Y_PM25_test = train_test_split(X_PM25, Y_PM25, test_size=0.2)

    # Regresion lineal
    modelo_LR.fit(X_PM25_train, Y_PM25_train)
    # Red neuronal
    modelo_RN.fit(X_PM25_train, Y_PM25_train, epochs=500, batch_size=10)

    # Evaluación
    mse_RN_PM25, mae_RN_PM25 = modelo_RN.evaluate(X_PM25_test, Y_PM25_test)

    # Prediccion
    prediccion_LR_PM25 = modelo_LR.predict(X_PM25_test)
    prediccion_RN_PM25 = modelo_RN.predict(X_PM25_test)

    # Valor unico
    pred_LR_PM25 = prediccion_LR_PM25[0]
    pred_RN_PM25 = prediccion_RN_PM25[0][0]

    # Metricas
    mae_LR_PM25 = mean_absolute_error(Y_PM25_test, prediccion_LR_PM25)
    mse_LR_PM25 = mean_squared_error(Y_PM25_test, prediccion_LR_PM25)
    r2_LR_PM25 = r2_score(Y_PM25_test, prediccion_LR_PM25)
    r2_RN_PM25 = r2_score(Y_PM25_test, prediccion_RN_PM25)

    # ----------------------------------------- Prediccion PM10 ------------------------------------------ #
    X_PM10 = filtro_estacion[['SO2', 'PM2,5', 'O3 8h', 'Tolueno', 'NOX']]
    Y_PM10 = filtro_estacion['PM10']

    # Division de datos
    X_PM10_train, X_PM10_test, Y_PM10_train, Y_PM10_test = train_test_split(X_PM10, Y_PM10, test_size=0.2)

    # Regresion lineal
    modelo_LR.fit(X_PM10_train, Y_PM10_train)
    # Red neuronal
    modelo_RN.fit(X_PM10_train, Y_PM10_train, epochs=500, batch_size=10)

    # Evaluación
    mse_RN_PM10, mae_RN_PM10 = modelo_RN.evaluate(X_PM10_test, Y_PM10_test)

    # Prediccion
    prediccion_LR_PM10 = modelo_LR.predict(X_PM10_train)
    prediccion_RN_PM10 = modelo_RN.predict(X_PM10_test)

    # Valor unico
    pred_LR_PM10 = prediccion_LR_PM10[0]
    pred_RN_PM10 = prediccion_RN_PM10[0][0]

    # Metricas
    mae_LR_PM10 = mean_absolute_error(Y_PM10_test, prediccion_LR_PM10)
    mse_LR_PM10 = mean_squared_error(Y_PM10_test, prediccion_LR_PM10)
    r2_LR_PM10 = r2_score(Y_PM10_test, prediccion_LR_PM10)
    r2_RN_PM10 = r2_score(Y_PM10_test, prediccion_RN_PM10)

    # ----------------------------------------- Prediccion 03_8h ------------------------------------------ #
    X_03_8h = filtro_estacion[['SO2', 'PM2,5', 'PM10', 'Tolueno', 'NOX']]
    Y_03_8h = filtro_estacion['O3 8h']

    # Division de datos
    X_03_8h_train, X_03_8h_test, Y_03_8h_train, Y_03_8h_test = train_test_split(X_03_8h, Y_03_8h, test_size=0.2)

    # Regresion lineal
    modelo_LR.fit(X_03_8h_train, Y_03_8h_train)
    # Red neuronal
    modelo_RN.fit(X_03_8h_train, Y_03_8h_train, epochs=500, batch_size=10)

    # Evaluación
    mse_RN_03_8h, mae_RN_03_8h = modelo_RN.evaluate(X_03_8h_test, Y_03_8h_test)

    # Prediccion
    prediccion_LR_03_8h = modelo_LR.predict(X_03_8h_train)
    prediccion_RN_03_8h = modelo_RN.predict(X_03_8h_test)

    # Valor unico
    pred_LR_03_8h = prediccion_LR_03_8h[0]
    pred_RN_03_8h = prediccion_RN_03_8h[0][0]

    # Metricas
    mae_03_8h = mean_absolute_error(Y_03_8h_test, prediccion_LR_03_8h)
    mse_03_8h = mean_squared_error(Y_03_8h_test, prediccion_LR_03_8h)
    r2_LR_03_8h = r2_score(Y_03_8h_test, prediccion_LR_03_8h)
    r2_RN_03_8h = r2_score(Y_03_8h_test, prediccion_RN_PM10)

# ----------------------------------------- Prediccion Tolueno ------------------------------------------ #
    X_Tolueno = filtro_estacion[['SO2', 'PM2,5', 'PM10', 'O3 8h', 'NOX']]
    Y_Tolueno = filtro_estacion['Tolueno']

    # Division de datos
    X_Tolueno_train, X_Tolueno_test, Y_Tolueno_train, Y_Tolueno_test = train_test_split(X_Tolueno, Y_Tolueno, test_size=0.2)

    # Regresion lineal
    modelo_LR.fit(X_Tolueno_train, Y_Tolueno_train)

    # Prediccion
    prediccion_Tolueno = modelo_LR.predict(X_Tolueno_train)

    # Metricas
    mae_Tolueno = mean_absolute_error(Y_Tolueno_test, prediccion_Tolueno)
    mse_Tolueno = mean_squared_error(Y_Tolueno_test, prediccion_Tolueno)
    r2_Tolueno = r2_score(Y_Tolueno_test, prediccion_Tolueno)

# ----------------------------------------- Prediccion NOX ------------------------------------------ #
    X_NOX = filtro_estacion[['SO2', 'PM2,5', 'PM10', 'O3 8h', 'Tolueno']]
    Y_NOX = filtro_estacion['NOX']

    # Division de datos
    X_NOX_train, X_NOX_test, Y_NOX_train, Y_NOX_test = train_test_split(X_NOX, Y_NOX, test_size=0.2)

    # Regresion lineal
    modelo_LR.fit(X_NOX_train, Y_NOX_train)

    # Prediccion
    prediccion_NOX = modelo_LR.predict(X_NOX_train)

    # Metricas
    mae_NOX = mean_absolute_error(Y_NOX_test, prediccion_NOX)
    mse_NOX = mean_squared_error(Y_NOX_test, prediccion_NOX)
    r2_NOX = r2_score(Y_NOX_test, prediccion_NOX)
'''
