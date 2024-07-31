# Imports
import bdd
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout


# Dataset
dataset_meteo = list(bdd.coleccion_meteo.find())
# DF
df_meteo = pd.DataFrame(dataset_meteo)
# Division de DFs
df_humedad = df_meteo[df_meteo['medida'] == 'humidity']
df_temperatura = df_meteo[df_meteo['medida'] == 'temperature']
df_superficial_wetting = df_meteo[df_meteo['medida'] == 'superficial_wetting']
df_visibilidad = df_meteo[df_meteo['medida'] == 'visibility']
df_precipitaciones = df_meteo[df_meteo['medida'] == 'precipitation']
df_velocidad_media_viento = df_meteo[df_meteo['medida'] == 'mean_speed']
df_direccion_viento = df_meteo[df_meteo['medida'] == 'direction_sigma']

# Metodo llamado desde analisis
def analisis_meteo():
    # Regresion lineal
    modelo_RL = LinearRegression()

    # Red neuronal
    modelo_RN = Sequential()
    modelo_RN.add(Dense(512, activation='relu', input_dim=5))
    modelo_RN.add(Dropout(0.1))
    modelo_RN.add(Dense(512, activation='relu'))
    modelo_RN.add(Dropout(0.1))
    modelo_RN.add(Dense(1, activation='linear'))
    # Compilar modelo
    modelo_RN.compile(optimizer='adam', loss='mse', metrics=['mae'])
    # Resumen del modelo
    modelo_RN.summary()

    # Random Forest
    modelo_RF = RandomForestRegressor(n_estimators=128)


    # DIAGRAMA DE CORRELACION
    # --------------------- #
    # Listado de los nombres de los DFs divididos
    df_divididos = [df_humedad, df_temperatura, df_superficial_wetting, df_visibilidad, df_precipitaciones, df_velocidad_media_viento, df_direccion_viento]
    # Bucle para recorrer todos los DFs
    for df in df_divididos:
        # Obtener unicamente los campos numericos
        df_sin_textos = df.select_dtypes(include=['number'])
        # Dimensiones
        plt.figure(figsize=(10, 8)) 
        # Graficar matriz de correlacion
        correlation_matrix = df_sin_textos.corr()
        # Estetica
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
        plt.title(f'Matriz de Correlacion {df}')
        plt.show()


    # PREDICCION HUMEDAD #
    # ------------------ #
    # Division de columnas del DF
    X_humedad = df_meteo[['año', 'dia', 'max', 'max_acumulado', 'mes', 'min', 'total']]
    Y_humedad = df_meteo['media']

    # Division de datos
    X_humedad_train, X_humedad_test, Y_humedad_train, Y_humedad_test = train_test_split(X_humedad, Y_humedad, test_size=0.2)

    # Entrenamiento RL
    modelo_RL.fit(X_humedad_train, Y_humedad_train)
    # Entrenamiento RN
    modelo_RN.fit(X_humedad_train, Y_humedad_train, epochs=400, batch_size=64, verbose=0)
    # Entrenamiento RF
    modelo_RF.fit(X_humedad_train, Y_humedad_train)

    # Prediccion RL
    prediccion_RL_humedad = modelo_RL.predict(X_humedad_test)
    # Prediccion RN
    prediccion_RN_humedad = modelo_RN.predict(X_humedad_test)
    # Prediccion RF
    prediccion_RF_humedad = modelo_RF.predict(X_humedad_test)

    # Evaluacion RN
    mse_RN_humedad, mae_RN_humedad = modelo_RN.evaluate(X_humedad_test, Y_humedad_test)

    # Metricas
    mae_RL_humedad = mean_absolute_error(Y_humedad_test, prediccion_RL_humedad)
    mse_RL_humedad = mean_squared_error(Y_humedad_test, prediccion_RL_humedad)
    r2_RN_humedad = r2_score(Y_humedad_test, prediccion_RN_humedad)
    r2_RL_humedad = r2_score(Y_humedad_test, prediccion_RL_humedad)
    mae_RF_humedad = mean_absolute_error(Y_humedad_test, prediccion_RF_humedad)
    mse_RF_humedad = mean_squared_error(Y_humedad_test, prediccion_RF_humedad)
    r2_RF_humedad = r2_score(Y_humedad_test, prediccion_RF_humedad)

    # Impresion
    print(f'Humedad')
    print(f'RL: {mse_RL_humedad} | {mae_RL_humedad} | {r2_RL_humedad}')
    print(f'RN: {mse_RN_humedad} | {mae_RN_humedad} | {r2_RN_humedad}')
    print(f'RF: {mse_RF_humedad} | {mae_RF_humedad} | {r2_RF_humedad}')


    # PREDICCION TEMPERATURA #
    # ---------------------- #
    # Division de columnas del DF
    X_temperatura = df_meteo[['año', 'dia', 'max', 'max_acumulado', 'mes', 'min', 'total']]
    Y_temperatura = df_meteo['media']

    # Division de datos
    X_temperatura_train, X_temperatura_test, Y_temperatura_train, Y_temperatura_test = train_test_split(X_temperatura, Y_temperatura, test_size=0.2)

    # Entrenamiento RL
    modelo_RL.fit(X_temperatura_train, Y_temperatura_train)
    # Entrenamiento RN
    modelo_RN.fit(X_temperatura_train, Y_temperatura_train, epochs=400, batch_size=64, verbose=0)
    # Entrenamiento RF
    modelo_RF.fit(X_temperatura_train, Y_temperatura_train)

    # Prediccion RL
    prediccion_RL_temperatura = modelo_RL.predict(X_temperatura_test)
    # Prediccion RN
    prediccion_RN_temperatura = modelo_RN.predict(X_temperatura_test)
    # Prediccion RF
    prediccion_RF_temperatura = modelo_RF.predict(X_temperatura_test)

    # Evaluacion RN
    mse_RN_temperatura, mae_RN_temperatura = modelo_RN.evaluate(X_temperatura_test, Y_temperatura_test)

    # Metricas
    mae_RL_temperatura = mean_absolute_error(Y_temperatura_test, prediccion_RL_temperatura)
    mse_RL_temperatura = mean_squared_error(Y_temperatura_test, prediccion_RL_temperatura)
    r2_RN_temperatura = r2_score(Y_temperatura_test, prediccion_RN_temperatura)
    r2_RL_temperatura = r2_score(Y_temperatura_test, prediccion_RL_temperatura)
    mae_RF_temperatura = mean_absolute_error(Y_temperatura_test, prediccion_RF_temperatura)
    mse_RF_temperatura = mean_squared_error(Y_temperatura_test, prediccion_RF_temperatura)
    r2_RF_temperatura = r2_score(Y_temperatura_test, prediccion_RF_temperatura)

    # Impresion
    print(f'Temperatura')
    print(f'RL: {mse_RL_temperatura} | {mae_RL_temperatura} | {r2_RL_temperatura}')
    print(f'RN: {mse_RN_temperatura} | {mae_RN_temperatura} | {r2_RN_temperatura}')
    print(f'RF: {mse_RF_temperatura} | {mae_RF_temperatura} | {r2_RF_temperatura}')


    # PREDICCION SW #
    # ---------------------- #
    # Division de columnas del DF
    X_SW = df_meteo[['año', 'dia', 'max', 'max_acumulado', 'mes', 'min', 'total']]
    Y_SW = df_meteo['media']

    # Division de datos
    X_SW_train, X_SW_test, Y_SW_train, Y_SW_test = train_test_split(X_SW, Y_SW, test_size=0.2)

    # Entrenamiento RL
    modelo_RL.fit(X_SW_train, Y_SW_train)
    # Entrenamiento RN
    modelo_RN.fit(X_SW_train, Y_SW_train, epochs=400, batch_size=64, verbose=0)
    # Entrenamiento RF
    modelo_RF.fit(X_SW_train, Y_SW_train)

    # Prediccion RL
    prediccion_RL_SW = modelo_RL.predict(X_SW_test)
    # Prediccion RN
    prediccion_RN_SW = modelo_RN.predict(X_SW_test)
    # Prediccion RF
    prediccion_RF_SW = modelo_RF.predict(X_SW_test)

    # Evaluacion RN
    mse_RN_SW, mae_RN_SW = modelo_RN.evaluate(X_SW_test, Y_SW_test)

    # Metricas
    mae_RL_SW = mean_absolute_error(Y_SW_test, prediccion_RL_SW)
    mse_RL_SW = mean_squared_error(Y_SW_test, prediccion_RL_SW)
    r2_RN_SW = r2_score(Y_SW_test, prediccion_RN_SW)
    r2_RL_SW = r2_score(Y_SW_test, prediccion_RL_SW)
    mae_RF_SW = mean_absolute_error(Y_SW_test, prediccion_RF_SW)
    mse_RF_SW = mean_squared_error(Y_SW_test, prediccion_RF_SW)
    r2_RF_SW = r2_score(Y_SW_test, prediccion_RF_SW)

    # Impresion
    print(f'Supperficial wetting')
    print(f'RL: {mse_RL_SW} | {mae_RL_SW} | {r2_RL_SW}')
    print(f'RN: {mse_RN_SW} | {mae_RN_SW} | {r2_RN_SW}')
    print(f'RF: {mse_RF_SW} | {mae_RF_SW} | {r2_RF_SW}')


    # PREDICCION VISIBILIDAD #
    # ---------------------- #
    # Division de columnas del DF
    X_visibilidad = df_meteo[['año', 'dia', 'max', 'max_acumulado', 'mes', 'min', 'total']]
    Y_visibilidad = df_meteo['media']

    # Division de datos
    X_visibilidad_train, X_visibilidad_test, Y_visibilidad_train, Y_visibilidad_test = train_test_split(X_visibilidad, Y_visibilidad, test_size=0.2)

    # Entrenamiento RL
    modelo_RL.fit(X_visibilidad_train, Y_visibilidad_train)
    # Entrenamiento RN
    modelo_RN.fit(X_visibilidad_train, Y_visibilidad_train, epochs=400, batch_size=64, verbose=0)
    # Entrenamiento RF
    modelo_RF.fit(X_visibilidad_train, Y_visibilidad_train)

    # Prediccion RL
    prediccion_RL_visibilidad = modelo_RL.predict(X_visibilidad_test)
    # Prediccion RN
    prediccion_RN_visibilidad = modelo_RN.predict(X_visibilidad_test)
    # Prediccion RF
    prediccion_RF_visibilidad = modelo_RF.predict(X_visibilidad_test)

    # Evaluacion RN
    mse_RN_visibilidad, mae_RN_visibilidad = modelo_RN.evaluate(X_visibilidad_test, Y_visibilidad_test)

    # Metricas
    mae_RL_visibilidad = mean_absolute_error(Y_visibilidad_test, prediccion_RL_visibilidad)
    mse_RL_visibilidad = mean_squared_error(Y_visibilidad_test, prediccion_RL_visibilidad)
    r2_RN_visibilidad = r2_score(Y_visibilidad_test, prediccion_RN_visibilidad)
    r2_RL_visibilidad = r2_score(Y_visibilidad_test, prediccion_RL_visibilidad)
    mae_RF_visibilidad = mean_absolute_error(Y_visibilidad_test, prediccion_RF_visibilidad)
    mse_RF_visibilidad = mean_squared_error(Y_visibilidad_test, prediccion_RF_visibilidad)
    r2_RF_visibilidad = r2_score(Y_visibilidad_test, prediccion_RF_visibilidad)

    # Impresion
    print(f'Visibilidad')
    print(f'RL: {mse_RL_visibilidad} | {mae_RL_visibilidad} | {r2_RL_visibilidad}')
    print(f'RN: {mse_RN_visibilidad} | {mae_RN_visibilidad} | {r2_RN_visibilidad}')
    print(f'RF: {mse_RF_visibilidad} | {mae_RF_visibilidad} | {r2_RF_visibilidad}')


    # PREDICCION PRECIPITACIONES #
    # -------------------------- #
    # Division de columnas del DF
    X_precipitaciones = df_meteo[['año', 'dia', 'max', 'max_acumulado', 'mes', 'min', 'total']]
    Y_precipitaciones = df_meteo['media']

    # Division de datos
    X_precipitaciones_train, X_precipitaciones_test, Y_precipitaciones_train, Y_precipitaciones_test = train_test_split(X_precipitaciones, Y_precipitaciones, test_size=0.2)

    # Entrenamiento RL
    modelo_RL.fit(X_precipitaciones_train, Y_precipitaciones_train)
    # Entrenamiento RN
    modelo_RN.fit(X_precipitaciones_train, Y_precipitaciones_train, epochs=400, batch_size=64, verbose=0)
    # Entrenamiento RF
    modelo_RF.fit(X_precipitaciones_train, Y_precipitaciones_train)

    # Prediccion RL
    prediccion_RL_precipitaciones = modelo_RL.predict(X_precipitaciones_test)
    # Prediccion RN
    prediccion_RN_precipitaciones = modelo_RN.predict(X_precipitaciones_test)
    # Prediccion RF
    prediccion_RF_precipitaciones = modelo_RF.predict(X_precipitaciones_test)

    # Evaluacion RN
    mse_RN_precipitaciones, mae_RN_precipitaciones = modelo_RN.evaluate(X_precipitaciones_test, Y_precipitaciones_test)

    # Metricas
    mae_RL_precipitaciones = mean_absolute_error(Y_precipitaciones_test, prediccion_RL_precipitaciones)
    mse_RL_precipitaciones = mean_squared_error(Y_precipitaciones_test, prediccion_RL_precipitaciones)
    r2_RN_precipitaciones = r2_score(Y_precipitaciones_test, prediccion_RN_precipitaciones)
    r2_RL_precipitaciones = r2_score(Y_precipitaciones_test, prediccion_RL_precipitaciones)
    mae_RF_precipitaciones = mean_absolute_error(Y_precipitaciones_test, prediccion_RF_precipitaciones)
    mse_RF_precipitaciones = mean_squared_error(Y_precipitaciones_test, prediccion_RF_precipitaciones)
    r2_RF_precipitaciones = r2_score(Y_precipitaciones_test, prediccion_RF_precipitaciones)

    # Impresion
    print(f'Precipitaciones')
    print(f'RL: {mse_RL_precipitaciones} | {mae_RL_precipitaciones} | {r2_RL_precipitaciones}')
    print(f'RN: {mse_RN_precipitaciones} | {mae_RN_precipitaciones} | {r2_RN_precipitaciones}')
    print(f'RF: {mse_RF_precipitaciones} | {mae_RF_precipitaciones} | {r2_RF_precipitaciones}')


    # PREDICCION VELOCIDAD MEDIA VIENTO #
    # --------------------------------- #
    # Division de columnas del DF
    X_vel_media_viento = df_meteo[['año', 'dia', 'max', 'max_acumulado', 'mes', 'min', 'total']]
    Y_vel_media_viento = df_meteo['media']

    # Division de datos
    X_vel_media_viento_train, X_vel_media_viento_test, Y_vel_media_viento_train, Y_vel_media_viento_test = train_test_split(X_vel_media_viento, Y_vel_media_viento, test_size=0.2)

    # Entrenamiento RL
    modelo_RL.fit(X_vel_media_viento_train, Y_vel_media_viento_train)
    # Entrenamiento RN
    modelo_RN.fit(X_vel_media_viento_train, Y_vel_media_viento_train, epochs=400, batch_size=64, verbose=0)
    # Entrenamiento RF
    modelo_RF.fit(X_vel_media_viento_train, Y_vel_media_viento_train)

    # Prediccion RL
    prediccion_RL_vel_media_viento = modelo_RL.predict(X_vel_media_viento_test)
    # Prediccion RN
    prediccion_RN_vel_media_viento = modelo_RN.predict(X_vel_media_viento_test)
    # Prediccion RF
    prediccion_RF_vel_media_viento = modelo_RF.predict(X_vel_media_viento_test)

    # Evaluacion RN
    mse_RN_vel_media_viento, mae_RN_vel_media_viento = modelo_RN.evaluate(X_vel_media_viento_test, Y_vel_media_viento_test)

    # Metricas
    mae_RL_vel_media_viento = mean_absolute_error(Y_vel_media_viento_test, prediccion_RL_vel_media_viento)
    mse_RL_vel_media_viento = mean_squared_error(Y_vel_media_viento_test, prediccion_RL_vel_media_viento)
    r2_RN_vel_media_viento = r2_score(Y_vel_media_viento_test, prediccion_RN_vel_media_viento)
    r2_RL_vel_media_viento = r2_score(Y_vel_media_viento_test, prediccion_RL_vel_media_viento)
    mae_RF_vel_media_viento = mean_absolute_error(Y_vel_media_viento_test, prediccion_RF_vel_media_viento)
    mse_RF_vel_media_viento = mean_squared_error(Y_vel_media_viento_test, prediccion_RF_vel_media_viento)
    r2_RF_vel_media_viento = r2_score(Y_vel_media_viento_test, prediccion_RF_vel_media_viento)

    # Impresion
    print(f'Velocidad media del viento')
    print(f'RL: {mse_RL_vel_media_viento} | {mae_RL_vel_media_viento} | {r2_RL_vel_media_viento}')
    print(f'RN: {mse_RN_vel_media_viento} | {mae_RN_vel_media_viento} | {r2_RN_vel_media_viento}')
    print(f'RF: {mse_RF_vel_media_viento} | {mae_RF_vel_media_viento} | {r2_RF_vel_media_viento}')


    # PREDICCION DIRECCION VIENTO #
    # --------------------------------- #
    # Division de columnas del DF
    X_direccion_viento = df_meteo[['año', 'dia', 'max', 'max_acumulado', 'mes', 'min', 'total']]
    Y_direccion_viento = df_meteo['media']

    # Division de datos
    X_direccion_viento_train, X_direccion_viento_test, Y_direccion_viento_train, Y_direccion_viento_test = train_test_split(X_direccion_viento, Y_direccion_viento, test_size=0.2)

    # Entrenamiento RL
    modelo_RL.fit(X_direccion_viento_train, Y_direccion_viento_train)
    # Entrenamiento RN
    modelo_RN.fit(X_direccion_viento_train, Y_direccion_viento_train, epochs=400, batch_size=64, verbose=0)
    # Entrenamiento RF
    modelo_RF.fit(X_direccion_viento_train, Y_direccion_viento_train)

    # Prediccion RL
    prediccion_RL_direccion_viento = modelo_RL.predict(X_direccion_viento_test)
    # Prediccion RN
    prediccion_RN_direccion_viento = modelo_RN.predict(X_direccion_viento_test)
    # Prediccion RF
    prediccion_RF_direccion_viento = modelo_RF.predict(X_direccion_viento_test)

    # Evaluacion RN
    mse_RN_direccion_viento, mae_RN_direccion_viento = modelo_RN.evaluate(X_direccion_viento_test, Y_direccion_viento_test)

    # Metricas
    mae_RL_direccion_viento = mean_absolute_error(Y_direccion_viento_test, prediccion_RL_direccion_viento)
    mse_RL_direccion_viento = mean_squared_error(Y_direccion_viento_test, prediccion_RL_direccion_viento)
    r2_RN_direccion_viento = r2_score(Y_direccion_viento_test, prediccion_RN_direccion_viento)
    r2_RL_direccion_viento = r2_score(Y_direccion_viento_test, prediccion_RL_direccion_viento)
    mae_RF_direccion_viento = mean_absolute_error(Y_direccion_viento_test, prediccion_RF_direccion_viento)
    mse_RF_direccion_viento = mean_squared_error(Y_direccion_viento_test, prediccion_RF_direccion_viento)
    r2_RF_direccion_viento = r2_score(Y_direccion_viento_test, prediccion_RF_direccion_viento)

    # Impresion
    print(f'Direccion del viento')
    print(f'RL: {mse_RL_direccion_viento} | {mae_RL_direccion_viento} | {r2_RL_direccion_viento}')
    print(f'RN: {mse_RN_direccion_viento} | {mae_RN_direccion_viento} | {r2_RN_direccion_viento}')
    print(f'RF: {mse_RF_direccion_viento} | {mae_RF_direccion_viento} | {r2_RF_direccion_viento}')