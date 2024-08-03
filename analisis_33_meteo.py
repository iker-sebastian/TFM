# Imports
import bdd
import pandas as pd
import config
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_predict, KFold
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from scikeras.wrappers import KerasRegressor

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

# Inicializar modelo red neuronal
modelo_red_neuronal = None

# Metodo llamado para invocar red neuronal
def red_neuronal():
    # Acceder a modelo_red_neuronal
    global modelo_red_neuronal
    # Condicion para crear el modelo
    if modelo_red_neuronal is None:
        # Red neuronal
        modelo_red_neuronal = Sequential()
        modelo_red_neuronal.add(Dense(512, activation='relu', input_dim=7))
        modelo_red_neuronal.add(Dropout(0.1))
        modelo_red_neuronal.add(Dense(512, activation='relu'))
        modelo_red_neuronal.add(Dropout(0.1))
        modelo_red_neuronal.add(Dense(1, activation='linear'))
        # Compilar modelo
        modelo_red_neuronal.compile(optimizer='adam', loss='mse', metrics=['mae'])
        # Resumen del modelo
        modelo_red_neuronal.summary()
    # Devuelve modelo, creado o global
    return modelo_red_neuronal

# Metodo llamado desde analisis
def analisis_meteo():
    # Regresion lineal
    modelo_RL = LinearRegression()
    # Random Forest
    modelo_RF = RandomForestRegressor(n_estimators=128)
    # Red neuronal
    modelo_RN = KerasRegressor(model=red_neuronal, epochs=400, batch_size=64, verbose=0)

    # K-Fold (tecnica de validacion cruzada)
    kf = KFold(n_splits=5, shuffle=True)


    # PREDICCION HUMEDAD #
    # ------------------ #
    # Division de columnas del DF
    X_humedad = df_humedad[['año', 'dia', 'max', 'max_acumulado', 'mes', 'min', 'total']]
    Y_humedad = df_humedad['media']

    # Cross Validation RL
    predicciones_RL_humedad = cross_val_predict(modelo_RL, X_humedad, Y_humedad, cv=kf)
    # Cross Validation RF
    predicciones_RF_humedad = cross_val_predict(modelo_RF, X_humedad, Y_humedad, cv=kf)
    # Cross Validation RN
    predicciones_RN_humedad = cross_val_predict(modelo_RN, X_humedad, Y_humedad, cv=kf)

    # Prediccion RL
    prediccion_RL_humedad = predicciones_RL_humedad.mean()
    # Prediccion RL
    prediccion_RF_humedad = predicciones_RF_humedad.mean()
    # Prediccion RL
    prediccion_RN_humedad = predicciones_RN_humedad.mean()

    # Metricas RL
    mse_RL_humedad = mean_squared_error(Y_humedad, predicciones_RL_humedad)
    mae_RL_humedad = mean_absolute_error(Y_humedad, predicciones_RL_humedad)
    r2_RL_humedad = r2_score(Y_humedad, predicciones_RL_humedad)
    # Metricas RF
    mse_RF_humedad = mean_squared_error(Y_humedad, predicciones_RF_humedad)
    mae_RF_humedad = mean_absolute_error(Y_humedad, predicciones_RF_humedad)
    r2_RF_humedad = r2_score(Y_humedad, predicciones_RF_humedad)
    # Metricas RN
    mse_RN_humedad = mean_squared_error(Y_humedad, predicciones_RN_humedad)
    mae_RN_humedad = mean_absolute_error(Y_humedad, predicciones_RN_humedad)
    r2_RN_humedad = r2_score(Y_humedad, predicciones_RN_humedad)
    
    # Impresion
    print(f'Humedad')
    print(f'MSE: RL-> {mse_RL_humedad} | RF-> {mse_RF_humedad}  | RN-> {mse_RN_humedad}')
    print(f'MAE: RL-> {mae_RL_humedad} | RF-> {mae_RF_humedad} | RN-> {mae_RN_humedad}')
    print(f'R2: RL-> {r2_RL_humedad} | RF-> {r2_RF_humedad} | RN-> {r2_RN_humedad}')
    print(f'Predicciones: RL-> {prediccion_RL_humedad} | RF-> {prediccion_RF_humedad} | RN-> {prediccion_RN_humedad}')

    # Creacion diccionario con datos
    doc = {
            'medida': 'Humedad',
            'MSE RL': mse_RL_humedad,
            'MSE RF': mse_RF_humedad,
            'MSE RN': mse_RN_humedad,
            'MAE RL': mae_RL_humedad,
            'MAE RF': mae_RF_humedad,
            'MAE RN': mae_RN_humedad,
            'R2 RL': r2_RL_humedad,
            'R2 RL': r2_RF_humedad,
            'R2 RL': r2_RN_humedad,
            'Prediccion RL': prediccion_RL_humedad,
            'Prediccion RF': prediccion_RF_humedad,
            'Prediccion RN': prediccion_RN_humedad,
        }
    
    # Añade el diccionario a un array
    config.array_dic_analisis_datos_meteo.append(doc)


    # PREDICCION TEMPERATURA #
    # ---------------------- #
    # Division de columnas del DF
    X_temperatura = df_temperatura[['año', 'dia', 'max', 'max_acumulado', 'mes', 'min', 'total']]
    Y_temperatura = df_temperatura['media']

    # Cross Validation RL
    predicciones_RL_temperatura = cross_val_predict(modelo_RL, X_temperatura, Y_temperatura, cv=kf)
    # Cross Validation RF
    predicciones_RF_temperatura = cross_val_predict(modelo_RF, X_temperatura, Y_temperatura, cv=kf)
    # Cross Validation RN
    predicciones_RN_temperatura = cross_val_predict(modelo_RN, X_temperatura, Y_temperatura, cv=kf)

    # Prediccion RL
    prediccion_RL_temperatura = predicciones_RL_temperatura.mean()
    # Prediccion RL
    prediccion_RF_temperatura = predicciones_RF_temperatura.mean()
    # Prediccion RL
    prediccion_RN_temperatura = predicciones_RN_temperatura.mean()

    # Metricas RL
    mse_RL_temperatura = mean_squared_error(Y_temperatura, predicciones_RL_temperatura)
    mae_RL_temperatura = mean_absolute_error(Y_temperatura, predicciones_RL_temperatura)
    r2_RL_temperatura = r2_score(Y_temperatura, predicciones_RL_temperatura)
    # Metricas RF
    mse_RF_temperatura = mean_squared_error(Y_temperatura, predicciones_RF_temperatura)
    mae_RF_temperatura = mean_absolute_error(Y_temperatura, predicciones_RF_temperatura)
    r2_RF_temperatura = r2_score(Y_temperatura, predicciones_RF_temperatura)
    # Metricas RN
    mse_RN_temperatura = mean_squared_error(Y_temperatura, predicciones_RN_temperatura)
    mae_RN_temperatura = mean_absolute_error(Y_temperatura, predicciones_RN_temperatura)
    r2_RN_temperatura = r2_score(Y_temperatura, predicciones_RN_temperatura)
    
    # Impresion
    print(f'Temperatura')
    print(f'MSE: RL-> {mse_RL_temperatura} | RF-> {mse_RF_temperatura}  | RN-> {mse_RN_temperatura}')
    print(f'MAE: RL-> {mae_RL_temperatura} | RF-> {mae_RF_temperatura} | RN-> {mae_RN_temperatura}')
    print(f'R2: RL-> {r2_RL_temperatura} | RF-> {r2_RF_temperatura} | RN-> {r2_RN_temperatura}')
    print(f'Predicciones: RL-> {prediccion_RL_temperatura} | RF-> {prediccion_RF_temperatura} | RN-> {prediccion_RN_temperatura}')

     # Creacion diccionario con datos
    doc = {
            'medida': 'Temperatura',
            'MSE RL': mse_RL_temperatura,
            'MSE RF': mse_RF_temperatura,
            'MSE RN': mse_RN_temperatura,
            'MAE RL': mae_RL_temperatura,
            'MAE RF': mae_RF_temperatura,
            'MAE RN': mae_RN_temperatura,
            'R2 RL': r2_RL_temperatura,
            'R2 RL': r2_RF_temperatura,
            'R2 RL': r2_RN_temperatura,
            'Prediccion RL': prediccion_RL_temperatura,
            'Prediccion RF': prediccion_RF_temperatura,
            'Prediccion RN': prediccion_RN_temperatura,
        }
    
    # Añade el diccionario a un array
    config.array_dic_analisis_datos_meteo.append(doc)


    # PREDICCION SW #
    # ---------------------- #
    # Division de columnas del DF
    X_SW = df_meteo[['año', 'dia', 'max', 'max_acumulado', 'mes', 'min', 'total']]
    Y_SW = df_meteo['media']

    # Cross Validation RL
    predicciones_RL_SW = cross_val_predict(modelo_RL, X_SW, Y_SW, cv=kf)
    # Cross Validation RF
    predicciones_RF_SW = cross_val_predict(modelo_RF, X_SW, Y_SW, cv=kf)
    # Cross Validation RN
    predicciones_RN_SW = cross_val_predict(modelo_RN, X_SW, Y_SW, cv=kf)

    # Prediccion RL
    prediccion_RL_SW = predicciones_RL_SW.mean()
    # Prediccion RL
    prediccion_RF_SW = predicciones_RF_SW.mean()
    # Prediccion RL
    prediccion_RN_SW = predicciones_RN_SW.mean()

    # Metricas RL
    mse_RL_SW = mean_squared_error(Y_SW, predicciones_RL_SW)
    mae_RL_SW = mean_absolute_error(Y_SW, predicciones_RL_SW)
    r2_RL_SW = r2_score(Y_SW, predicciones_RL_SW)
    # Metricas RF
    mse_RF_SW = mean_squared_error(Y_SW, predicciones_RF_SW)
    mae_RF_SW = mean_absolute_error(Y_SW, predicciones_RF_SW)
    r2_RF_SW = r2_score(Y_SW, predicciones_RF_SW)
    # Metricas RN
    mse_RN_SW = mean_squared_error(Y_SW, predicciones_RN_SW)
    mae_RN_SW = mean_absolute_error(Y_SW, predicciones_RN_SW)
    r2_RN_SW = r2_score(Y_SW, predicciones_RN_SW)
    
    # Impresion
    print(f'Humectacion superficial')
    print(f'MSE: RL-> {mse_RL_SW} | RF-> {mse_RF_SW}  | RN-> {mse_RN_SW}')
    print(f'MAE: RL-> {mae_RL_SW} | RF-> {mae_RF_SW} | RN-> {mae_RN_SW}')
    print(f'R2: RL-> {r2_RL_SW} | RF-> {r2_RF_SW} | RN-> {r2_RN_SW}')
    print(f'Predicciones: RL-> {prediccion_RL_SW} | RF-> {prediccion_RF_SW} | RN-> {prediccion_RN_SW}')

    # Creacion diccionario con datos
    doc = {
            'medida': 'Humectacion superficial',
            'MSE RL': mse_RL_SW,
            'MSE RF': mse_RF_SW,
            'MSE RN': mse_RN_SW,
            'MAE RL': mae_RL_SW,
            'MAE RF': mae_RF_SW,
            'MAE RN': mae_RN_SW,
            'R2 RL': r2_RL_SW,
            'R2 RL': r2_RF_SW,
            'R2 RL': r2_RN_SW,
            'Prediccion RL': prediccion_RL_SW,
            'Prediccion RF': prediccion_RF_SW,
            'Prediccion RN': prediccion_RN_SW,
        }
    
    # Añade el diccionario a un array
    config.array_dic_analisis_datos_meteo.append(doc)


    # PREDICCION VISIBILIDAD #
    # ---------------------- #
    # Division de columnas del DF
    X_visibilidad = df_meteo[['año', 'dia', 'max', 'max_acumulado', 'mes', 'min', 'total']]
    Y_visibilidad = df_meteo['media']

    # Cross Validation RL
    predicciones_RL_visibilidad = cross_val_predict(modelo_RL, X_visibilidad, Y_visibilidad, cv=kf)
    # Cross Validation RF
    predicciones_RF_visibilidad = cross_val_predict(modelo_RF, X_visibilidad, Y_visibilidad, cv=kf)
    # Cross Validation RN
    predicciones_RN_visibilidad = cross_val_predict(modelo_RN, X_visibilidad, Y_visibilidad, cv=kf)

    # Prediccion RL
    prediccion_RL_visibilidad = predicciones_RL_visibilidad.mean()
    # Prediccion RL
    prediccion_RF_visibilidad = predicciones_RF_visibilidad.mean()
    # Prediccion RL
    prediccion_RN_visibilidad = predicciones_RN_visibilidad.mean()

    # Metricas RL
    mse_RL_visibilidad = mean_squared_error(Y_visibilidad, predicciones_RL_visibilidad)
    mae_RL_visibilidad = mean_absolute_error(Y_visibilidad, predicciones_RL_visibilidad)
    r2_RL_visibilidad = r2_score(Y_visibilidad, predicciones_RL_visibilidad)
    # Metricas RF
    mse_RF_visibilidad = mean_squared_error(Y_visibilidad, predicciones_RF_visibilidad)
    mae_RF_visibilidad = mean_absolute_error(Y_visibilidad, predicciones_RF_visibilidad)
    r2_RF_visibilidad = r2_score(Y_visibilidad, predicciones_RF_visibilidad)
    # Metricas RN
    mse_RN_visibilidad = mean_squared_error(Y_visibilidad, predicciones_RN_visibilidad)
    mae_RN_visibilidad = mean_absolute_error(Y_visibilidad, predicciones_RN_visibilidad)
    r2_RN_visibilidad = r2_score(Y_visibilidad, predicciones_RN_visibilidad)
    
    # Impresion
    print(f'Visibilidad')
    print(f'MSE: RL-> {mse_RL_visibilidad} | RF-> {mse_RF_visibilidad}  | RN-> {mse_RN_visibilidad}')
    print(f'MAE: RL-> {mae_RL_visibilidad} | RF-> {mae_RF_visibilidad} | RN-> {mae_RN_visibilidad}')
    print(f'R2: RL-> {r2_RL_visibilidad} | RF-> {r2_RF_visibilidad} | RN-> {r2_RN_visibilidad}')
    print(f'Predicciones: RL-> {prediccion_RL_visibilidad} | RF-> {prediccion_RF_visibilidad} | RN-> {prediccion_RN_visibilidad}')

    doc = {
            'medida': 'Visibilidad',
            'MSE RL': mse_RL_visibilidad,
            'MSE RF': mse_RF_visibilidad,
            'MSE RN': mse_RN_visibilidad,
            'MAE RL': mae_RL_visibilidad,
            'MAE RF': mae_RF_visibilidad,
            'MAE RN': mae_RN_visibilidad,
            'R2 RL': r2_RL_visibilidad,
            'R2 RL': r2_RF_visibilidad,
            'R2 RL': r2_RN_visibilidad,
            'Prediccion RL': prediccion_RL_visibilidad,
            'Prediccion RF': prediccion_RF_visibilidad,
            'Prediccion RN': prediccion_RN_visibilidad,
        }
    
    # Añade el diccionario a un array
    config.array_dic_analisis_datos_meteo.append(doc)


    # PREDICCION PRECIPITACIONES #
    # -------------------------- #
    # Division de columnas del DF
    X_precipitaciones = df_meteo[['año', 'dia', 'max', 'max_acumulado', 'mes', 'min', 'total']]
    Y_precipitaciones = df_meteo['media']

    # Cross Validation RL
    predicciones_RL_precipitaciones = cross_val_predict(modelo_RL, X_precipitaciones, Y_precipitaciones, cv=kf)
    # Cross Validation RF
    predicciones_RF_precipitaciones = cross_val_predict(modelo_RF, X_precipitaciones, Y_precipitaciones, cv=kf)
    # Cross Validation RN
    predicciones_RN_precipitaciones = cross_val_predict(modelo_RN, X_precipitaciones, Y_precipitaciones, cv=kf)

    # Prediccion RL
    prediccion_RL_precipitaciones = predicciones_RL_precipitaciones.mean()
    # Prediccion RL
    prediccion_RF_precipitaciones = predicciones_RF_precipitaciones.mean()
    # Prediccion RL
    prediccion_RN_precipitaciones = predicciones_RN_precipitaciones.mean()

    # Metricas RL
    mse_RL_precipitaciones = mean_squared_error(Y_precipitaciones, predicciones_RL_precipitaciones)
    mae_RL_precipitaciones = mean_absolute_error(Y_precipitaciones, predicciones_RL_precipitaciones)
    r2_RL_precipitaciones = r2_score(Y_precipitaciones, predicciones_RL_precipitaciones)
    # Metricas RF
    mse_RF_precipitaciones = mean_squared_error(Y_precipitaciones, predicciones_RF_precipitaciones)
    mae_RF_precipitaciones = mean_absolute_error(Y_precipitaciones, predicciones_RF_precipitaciones)
    r2_RF_precipitaciones = r2_score(Y_precipitaciones, predicciones_RF_precipitaciones)
    # Metricas RN
    mse_RN_precipitaciones = mean_squared_error(Y_precipitaciones, predicciones_RN_precipitaciones)
    mae_RN_precipitaciones = mean_absolute_error(Y_precipitaciones, predicciones_RN_precipitaciones)
    r2_RN_precipitaciones = r2_score(Y_precipitaciones, predicciones_RN_precipitaciones)
    
    # Impresion
    print(f'Precipitaciones')
    print(f'MSE: RL-> {mse_RL_precipitaciones} | RF-> {mse_RF_precipitaciones}  | RN-> {mse_RN_precipitaciones}')
    print(f'MAE: RL-> {mae_RL_precipitaciones} | RF-> {mae_RF_precipitaciones} | RN-> {mae_RN_precipitaciones}')
    print(f'R2: RL-> {r2_RL_precipitaciones} | RF-> {r2_RF_precipitaciones} | RN-> {r2_RN_precipitaciones}')
    print(f'Predicciones: RL-> {prediccion_RL_precipitaciones} | RF-> {prediccion_RF_precipitaciones} | RN-> {prediccion_RN_precipitaciones}')

    doc = {
            'medida': 'Precipitaciones',
            'MSE RL': mse_RL_precipitaciones,
            'MSE RF': mse_RF_precipitaciones,
            'MSE RN': mse_RN_precipitaciones,
            'MAE RL': mae_RL_precipitaciones,
            'MAE RF': mae_RF_precipitaciones,
            'MAE RN': mae_RN_precipitaciones,
            'R2 RL': r2_RL_precipitaciones,
            'R2 RL': r2_RF_precipitaciones,
            'R2 RL': r2_RN_precipitaciones,
            'Prediccion RL': prediccion_RL_precipitaciones,
            'Prediccion RF': prediccion_RF_precipitaciones,
            'Prediccion RN': prediccion_RN_precipitaciones,
        }
    
    # Añade el diccionario a un array
    config.array_dic_analisis_datos_meteo.append(doc)

    # PREDICCION VELOCIDAD MEDIA VIENTO #
    # --------------------------------- #
    # Division de columnas del DF
    X_vel_media_viento = df_meteo[['año', 'dia', 'max', 'max_acumulado', 'mes', 'min', 'total']]
    Y_vel_media_viento = df_meteo['media']

    # Cross Validation RL
    predicciones_RL_vel_media_viento = cross_val_predict(modelo_RL, X_vel_media_viento, Y_vel_media_viento, cv=kf)
    # Cross Validation RF
    predicciones_RF_vel_media_viento = cross_val_predict(modelo_RF, X_vel_media_viento, Y_vel_media_viento, cv=kf)
    # Cross Validation RN
    predicciones_RN_vel_media_viento = cross_val_predict(modelo_RN, X_vel_media_viento, Y_vel_media_viento, cv=kf)

    # Prediccion RL
    prediccion_RL_vel_media_viento = predicciones_RL_vel_media_viento.mean()
    # Prediccion RL
    prediccion_RF_vel_media_viento = predicciones_RF_vel_media_viento.mean()
    # Prediccion RL
    prediccion_RN_vel_media_viento = predicciones_RN_vel_media_viento.mean()

    # Metricas RL
    mse_RL_vel_media_viento = mean_squared_error(Y_vel_media_viento, predicciones_RL_vel_media_viento)
    mae_RL_vel_media_viento = mean_absolute_error(Y_vel_media_viento, predicciones_RL_vel_media_viento)
    r2_RL_vel_media_viento = r2_score(Y_vel_media_viento, predicciones_RL_vel_media_viento)
    # Metricas RF
    mse_RF_vel_media_viento = mean_squared_error(Y_vel_media_viento, predicciones_RF_vel_media_viento)
    mae_RF_vel_media_viento = mean_absolute_error(Y_vel_media_viento, predicciones_RF_vel_media_viento)
    r2_RF_vel_media_viento = r2_score(Y_vel_media_viento, predicciones_RF_vel_media_viento)
    # Metricas RN
    mse_RN_vel_media_viento = mean_squared_error(Y_vel_media_viento, predicciones_RN_vel_media_viento)
    mae_RN_vel_media_viento = mean_absolute_error(Y_vel_media_viento, predicciones_RN_vel_media_viento)
    r2_RN_vel_media_viento = r2_score(Y_vel_media_viento, predicciones_RN_vel_media_viento)
    
    # Impresion
    print(f'Velocidad media viento')
    print(f'MSE: RL-> {mse_RL_vel_media_viento} | RF-> {mse_RF_vel_media_viento}  | RN-> {mse_RN_vel_media_viento}')
    print(f'MAE: RL-> {mae_RL_vel_media_viento} | RF-> {mae_RF_vel_media_viento} | RN-> {mae_RN_vel_media_viento}')
    print(f'R2: RL-> {r2_RL_vel_media_viento} | RF-> {r2_RF_vel_media_viento} | RN-> {r2_RN_vel_media_viento}')
    print(f'Predicciones: RL-> {prediccion_RL_vel_media_viento} | RF-> {prediccion_RF_vel_media_viento} | RN-> {prediccion_RN_vel_media_viento}')

    doc = {
            'medida': 'Velocidad media del viento',
            'MSE RL': mse_RL_vel_media_viento,
            'MSE RF': mse_RF_vel_media_viento,
            'MSE RN': mse_RN_vel_media_viento,
            'MAE RL': mae_RL_vel_media_viento,
            'MAE RF': mae_RF_vel_media_viento,
            'MAE RN': mae_RN_vel_media_viento,
            'R2 RL': r2_RL_vel_media_viento,
            'R2 RL': r2_RF_vel_media_viento,
            'R2 RL': r2_RN_vel_media_viento,
            'Prediccion RL': prediccion_RL_vel_media_viento,
            'Prediccion RF': prediccion_RF_vel_media_viento,
            'Prediccion RN': prediccion_RN_vel_media_viento,
        }
    
    # Añade el diccionario a un array
    config.array_dic_analisis_datos_meteo.append(doc)

    # PREDICCION DIRECCION VIENTO #
    # --------------------------------- #
    # Division de columnas del DF
    X_direccion_viento = df_meteo[['año', 'dia', 'max', 'max_acumulado', 'mes', 'min', 'total']]
    Y_direccion_viento = df_meteo['media']

    # Cross Validation RL
    predicciones_RL_direccion_viento = cross_val_predict(modelo_RL, X_direccion_viento, Y_direccion_viento, cv=kf)
    # Cross Validation RF
    predicciones_RF_direccion_viento = cross_val_predict(modelo_RF, X_direccion_viento, Y_direccion_viento, cv=kf)
    # Cross Validation RN
    predicciones_RN_direccion_viento = cross_val_predict(modelo_RN, X_direccion_viento, Y_direccion_viento, cv=kf)

    # Prediccion RL
    prediccion_RL_direccion_viento = predicciones_RL_direccion_viento.mean()
    # Prediccion RL
    prediccion_RF_direccion_viento = predicciones_RF_direccion_viento.mean()
    # Prediccion RL
    prediccion_RN_direccion_viento = predicciones_RN_direccion_viento.mean()

    # Metricas RL
    mse_RL_direccion_viento = mean_squared_error(Y_direccion_viento, predicciones_RL_direccion_viento)
    mae_RL_direccion_viento = mean_absolute_error(Y_direccion_viento, predicciones_RL_direccion_viento)
    r2_RL_direccion_viento = r2_score(Y_direccion_viento, predicciones_RL_direccion_viento)
    # Metricas RF
    mse_RF_direccion_viento = mean_squared_error(Y_direccion_viento, predicciones_RF_direccion_viento)
    mae_RF_direccion_viento = mean_absolute_error(Y_direccion_viento, predicciones_RF_direccion_viento)
    r2_RF_direccion_viento = r2_score(Y_direccion_viento, predicciones_RF_direccion_viento)
    # Metricas RN
    mse_RN_direccion_viento = mean_squared_error(Y_direccion_viento, predicciones_RN_direccion_viento)
    mae_RN_direccion_viento = mean_absolute_error(Y_direccion_viento, predicciones_RN_direccion_viento)
    r2_RN_direccion_viento = r2_score(Y_direccion_viento, predicciones_RN_direccion_viento)
    
    # Impresion
    print(f'Direccion viento')
    print(f'MSE: RL-> {mse_RL_direccion_viento} | RF-> {mse_RF_direccion_viento}  | RN-> {mse_RN_direccion_viento}')
    print(f'MAE: RL-> {mae_RL_direccion_viento} | RF-> {mae_RF_direccion_viento} | RN-> {mae_RN_direccion_viento}')
    print(f'R2: RL-> {r2_RL_direccion_viento} | RF-> {r2_RF_direccion_viento} | RN-> {r2_RN_direccion_viento}')
    print(f'Predicciones: RL-> {prediccion_RL_direccion_viento} | RF-> {prediccion_RF_direccion_viento} | RN-> {prediccion_RN_direccion_viento}')

    doc = {
            'medida': 'Direccion del viento',
            'MSE RL': mse_RL_direccion_viento,
            'MSE RF': mse_RF_direccion_viento,
            'MSE RN': mse_RN_direccion_viento,
            'MAE RL': mae_RL_direccion_viento,
            'MAE RF': mae_RF_direccion_viento,
            'MAE RN': mae_RN_direccion_viento,
            'R2 RL': r2_RL_direccion_viento,
            'R2 RL': r2_RF_direccion_viento,
            'R2 RL': r2_RN_direccion_viento,
            'Prediccion RL': prediccion_RL_direccion_viento,
            'Prediccion RF': prediccion_RF_direccion_viento,
            'Prediccion RN': prediccion_RN_direccion_viento,
        }
    
    # Añade el diccionario a un array
    config.array_dic_analisis_datos_meteo.append(doc)

    # Insercion datos meteorologicos despues del analisis
    for doc in config.array_dic_analisis_datos_meteo:
        # Actualiza el documento si existe '_id', si no inserta datos
        bdd.coleccion_analisis_meteo.update_one({'_id': doc['_id']}, {'$set': doc}, upsert=True)