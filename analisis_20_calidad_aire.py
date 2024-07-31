# Imports
import bdd
import pandas as pd

from sklearn import datasets, metrics
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_predict, cross_val_score, KFold
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, make_scorer

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from scikeras.wrappers import KerasRegressor

# Dataset
dataset_calidad_aire = list(bdd.coleccion_calidad_aire.find())
# DF
df_calidad_aire = pd.DataFrame(dataset_calidad_aire)

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
        modelo_red_neuronal.add(Dense(512, activation='relu', input_dim=5))
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
def analisis_calidad_aire():
    # Regresion lineal
    modelo_RL = LinearRegression()
    # Random Forest
    modelo_RF = RandomForestRegressor(n_estimators=128)
    # Red neuronal
    modelo_RN = KerasRegressor(model=red_neuronal, epochs=400, batch_size=64, verbose=0)

    # K-Fold (tecnica de validacion cruzada)
    kf = KFold(n_splits=5, shuffle=True)

    # DF para eliminar los campos que no aportan informacion
    df_numerico = df_calidad_aire.drop(columns=['_id', 'id_estacion', 'nombre', 'unidad_medicion'])
    # Borrar valores atipicos o erroneos
    df_numerico_clean = df_numerico.drop(df_numerico[df_numerico['SO2'] == -1].index)
    # DF agrupado
    df_group_by_date = df_numerico_clean.groupby(['fecha', 'provincia']).mean().reset_index()
    # Rellenar valores nulos con 0 para prediccion
    df_group_by_date_clean = df_group_by_date.fillna(0)


    # PREDICCION TOLUENO #
    # ------------------ #
    # Division de columnas del DF
    X_Tolueno = df_group_by_date_clean[['SO2', 'PM10', 'PM2,5', 'O3 8h', 'NOX']]
    Y_Tolueno = df_group_by_date_clean['Tolueno']

    # Cross Validation RL
    predicciones_RL_Tolueno = cross_val_predict(modelo_RL, X_Tolueno, Y_Tolueno, cv=kf)
    # Cross Validation RF
    predicciones_RF_Tolueno = cross_val_predict(modelo_RF, X_Tolueno, Y_Tolueno, cv=kf)
    # Cross Validation RN
    predicciones_RN_Tolueno = cross_val_predict(modelo_RN, X_Tolueno, Y_Tolueno, cv=kf)

    # Prediccion RL
    prediccion_RL_Tolueno = predicciones_RL_Tolueno.mean()
    # Prediccion RL
    prediccion_RF_Tolueno = predicciones_RF_Tolueno.mean()
    # Prediccion RL
    prediccion_RN_Tolueno = predicciones_RN_Tolueno.mean()

    # Metricas RL
    mse_RL_Tolueno = mean_squared_error(Y_Tolueno, predicciones_RL_Tolueno)
    mae_RL_Tolueno = mean_absolute_error(Y_Tolueno, predicciones_RL_Tolueno)
    r2_RL_Tolueno = r2_score(Y_Tolueno, predicciones_RL_Tolueno)
    # Metricas RF
    mse_RF_Tolueno = mean_squared_error(Y_Tolueno, predicciones_RF_Tolueno)
    mae_RF_Tolueno = mean_absolute_error(Y_Tolueno, predicciones_RF_Tolueno)
    r2_RF_Tolueno = r2_score(Y_Tolueno, predicciones_RF_Tolueno)
    # Metricas RN
    mse_RN_Tolueno = mean_squared_error(Y_Tolueno, predicciones_RN_Tolueno)
    mae_RN_Tolueno = mean_absolute_error(Y_Tolueno, predicciones_RN_Tolueno)
    r2_RN_Tolueno = r2_score(Y_Tolueno, predicciones_RN_Tolueno)
    
    # Impresion
    print(f'Tolueno')
    print(f'MSE: RL-> {mse_RL_Tolueno} | RF-> {mse_RF_Tolueno}  | RN-> {mse_RN_Tolueno}')
    print(f'MAE: RL-> {mae_RL_Tolueno} | RF-> {mae_RF_Tolueno} | RN-> {mae_RN_Tolueno}')
    print(f'R2: RL-> {r2_RL_Tolueno} | RF-> {r2_RF_Tolueno} | RN-> {r2_RN_Tolueno}')
    print(f'Predicciones: RL-> {prediccion_RL_Tolueno} | RF-> {prediccion_RF_Tolueno} | RN-> {prediccion_RN_Tolueno}')


    # PREDICCION SO2 #
    # -------------- #
    # Division de columnas del DF
    X_SO2 = df_group_by_date_clean[['PM2,5', 'PM10', 'O3 8h', 'Tolueno', 'NOX']]
    Y_SO2 = df_group_by_date_clean['SO2']

    # Cross Validation RL
    predicciones_RL_SO2 = cross_val_predict(modelo_RL, X_SO2, Y_SO2, cv=kf)
    # Cross Validation RF
    predicciones_RF_SO2 = cross_val_predict(modelo_RF, X_SO2, Y_SO2, cv=kf)
    # Cross Validation RN
    predicciones_RN_SO2 = cross_val_predict(modelo_RN, X_SO2, Y_SO2, cv=kf)

    # Prediccion RL
    prediccion_RL_SO2 = predicciones_RL_SO2.mean()
    # Prediccion RL
    prediccion_RF_SO2 = predicciones_RF_SO2.mean()
    # Prediccion RL
    prediccion_RN_SO2 = predicciones_RN_SO2.mean()

    # Metricas RL
    mse_RL_SO2 = mean_squared_error(Y_SO2, predicciones_RL_SO2)
    mae_RL_SO2 = mean_absolute_error(Y_SO2, predicciones_RL_SO2)
    r2_RL_SO2 = r2_score(Y_SO2, predicciones_RL_SO2)
    # Metricas RF
    mse_RF_SO2 = mean_squared_error(Y_SO2, predicciones_RF_SO2)
    mae_RF_SO2 = mean_absolute_error(Y_SO2, predicciones_RF_SO2)
    r2_RF_SO2 = r2_score(Y_SO2, predicciones_RF_SO2)
    # Metricas RN
    mse_RN_SO2 = mean_squared_error(Y_SO2, predicciones_RN_SO2)
    mae_RN_SO2 = mean_absolute_error(Y_SO2, predicciones_RN_SO2)
    r2_RN_SO2 = r2_score(Y_SO2, predicciones_RN_SO2)
    
    # Impresion
    print(f'SO2')
    print(f'MSE: RL-> {mse_RL_SO2} | RF-> {mse_RF_SO2}  | RN-> {mse_RN_SO2}')
    print(f'MAE: RL-> {mae_RL_SO2} | RF-> {mae_RF_SO2} | RN-> {mae_RN_SO2}')
    print(f'R2: RL-> {r2_RL_SO2} | RF-> {r2_RF_SO2} | RN-> {r2_RN_SO2}')
    print(f'Predicciones: RL-> {prediccion_RL_SO2} | RF-> {prediccion_RF_SO2} | RN-> {prediccion_RN_SO2}')


    # PREDICCION PM25 #
    # --------------- #
    # Division de columnas del DF
    X_PM2_5 = df_group_by_date_clean[['SO2', 'PM10', 'O3 8h', 'Tolueno', 'NOX']]
    Y_PM2_5 = df_group_by_date_clean['PM2,5']

    # Cross Validation RL
    predicciones_RL_PM2_5 = cross_val_predict(modelo_RL, X_PM2_5, Y_PM2_5, cv=kf)
    # Cross Validation RF
    predicciones_RF_PM2_5 = cross_val_predict(modelo_RF, X_PM2_5, Y_PM2_5, cv=kf)
    # Cross Validation RN
    predicciones_RN_PM2_5 = cross_val_predict(modelo_RN, X_PM2_5, Y_PM2_5, cv=kf)

    # Prediccion RL
    prediccion_RL_PM2_5 = predicciones_RL_PM2_5.mean()
    # Prediccion RL
    prediccion_RF_PM2_5 = predicciones_RF_PM2_5.mean()
    # Prediccion RL
    prediccion_RN_PM2_5 = predicciones_RN_PM2_5.mean()

    # Metricas RL
    mse_RL_PM2_5 = mean_squared_error(Y_PM2_5, predicciones_RL_PM2_5)
    mae_RL_PM2_5 = mean_absolute_error(Y_PM2_5, predicciones_RL_PM2_5)
    r2_RL_PM2_5 = r2_score(Y_PM2_5, predicciones_RL_PM2_5)
    # Metricas RF
    mse_RF_PM2_5 = mean_squared_error(Y_PM2_5, predicciones_RF_PM2_5)
    mae_RF_PM2_5 = mean_absolute_error(Y_PM2_5, predicciones_RF_PM2_5)
    r2_RF_PM2_5 = r2_score(Y_PM2_5, predicciones_RF_PM2_5)
    # Metricas RN
    mse_RN_PM2_5 = mean_squared_error(Y_PM2_5, predicciones_RN_PM2_5)
    mae_RN_PM2_5 = mean_absolute_error(Y_PM2_5, predicciones_RN_PM2_5)
    r2_RN_PM2_5 = r2_score(Y_PM2_5, predicciones_RN_PM2_5)
    
    # Impresion
    print(f'PM2,5')
    print(f'MSE: RL-> {mse_RL_PM2_5} | RF-> {mse_RF_PM2_5}  | RN-> {mse_RN_PM2_5}')
    print(f'MAE: RL-> {mae_RL_PM2_5} | RF-> {mae_RF_PM2_5} | RN-> {mae_RN_PM2_5}')
    print(f'R2: RL-> {r2_RL_PM2_5} | RF-> {r2_RF_PM2_5} | RN-> {r2_RN_PM2_5}')
    print(f'Predicciones: RL-> {prediccion_RL_PM2_5} | RF-> {prediccion_RF_PM2_5} | RN-> {prediccion_RN_PM2_5}')


    # PREDICCION PM10 #
    # --------------- #
    # Division de columnas del DF
    X_PM10 = df_group_by_date_clean[['SO2', 'PM2,5', 'O3 8h', 'Tolueno', 'NOX']]
    Y_PM10 = df_group_by_date_clean['PM10']

    # Cross Validation RL
    predicciones_RL_PM10 = cross_val_predict(modelo_RL, X_PM10, Y_PM10, cv=kf)
    # Cross Validation RF
    predicciones_RF_PM10 = cross_val_predict(modelo_RF, X_PM10, Y_PM10, cv=kf)
    # Cross Validation RN
    predicciones_RN_PM10 = cross_val_predict(modelo_RN, X_PM10, Y_PM10, cv=kf)

    # Prediccion RL
    prediccion_RL_PM10 = predicciones_RL_PM10.mean()
    # Prediccion RL
    prediccion_RF_PM10 = predicciones_RF_PM10.mean()
    # Prediccion RL
    prediccion_RN_PM10 = predicciones_RN_PM10.mean()

    # Metricas RL
    mse_RL_PM10 = mean_squared_error(Y_PM10, predicciones_RL_PM10)
    mae_RL_PM10 = mean_absolute_error(Y_PM10, predicciones_RL_PM10)
    r2_RL_PM10 = r2_score(Y_PM10, predicciones_RL_PM10)
    # Metricas RF
    mse_RF_PM10 = mean_squared_error(Y_PM10, predicciones_RF_PM10)
    mae_RF_PM10 = mean_absolute_error(Y_PM10, predicciones_RF_PM10)
    r2_RF_PM10 = r2_score(Y_PM10, predicciones_RF_PM10)
    # Metricas RN
    mse_RN_PM10 = mean_squared_error(Y_PM10, predicciones_RN_PM10)
    mae_RN_PM10 = mean_absolute_error(Y_PM10, predicciones_RN_PM10)
    r2_RN_PM10 = r2_score(Y_PM10, predicciones_RN_PM10)
    
    # Impresion
    print(f'PM10')
    print(f'MSE: RL-> {mse_RL_PM10} | RF-> {mse_RF_PM10}  | RN-> {mse_RN_PM10}')
    print(f'MAE: RL-> {mae_RL_PM10} | RF-> {mae_RF_PM10} | RN-> {mae_RN_PM10}')
    print(f'R2: RL-> {r2_RL_PM10} | RF-> {r2_RF_PM10} | RN-> {r2_RN_PM10}')
    print(f'Predicciones: RL-> {prediccion_RL_PM10} | RF-> {prediccion_RF_PM10} | RN-> {prediccion_RN_PM10}')


    # PREDICCION 03 8h #
    # ---------------- #
    # Division de columnas del DF
    X_03_8h = df_group_by_date_clean[['SO2', 'PM2,5', 'PM10', 'Tolueno', 'NOX']]
    Y_03_8h = df_group_by_date_clean['O3 8h']

    # Cross Validation RL
    predicciones_RL_03_8h = cross_val_predict(modelo_RL, X_03_8h, Y_03_8h, cv=kf)
    # Cross Validation RF
    predicciones_RF_03_8h = cross_val_predict(modelo_RF, X_03_8h, Y_03_8h, cv=kf)
    # Cross Validation RN
    predicciones_RN_03_8h = cross_val_predict(modelo_RN, X_03_8h, Y_03_8h, cv=kf)

    # Prediccion RL
    prediccion_RL_03_8h = predicciones_RL_03_8h.mean()
    # Prediccion RL
    prediccion_RF_03_8h = predicciones_RF_03_8h.mean()
    # Prediccion RL
    prediccion_RN_03_8h = predicciones_RN_03_8h.mean()

    # Metricas RL
    mse_RL_03_8h = mean_squared_error(Y_03_8h, predicciones_RL_03_8h)
    mae_RL_03_8h = mean_absolute_error(Y_03_8h, predicciones_RL_03_8h)
    r2_RL_03_8h = r2_score(Y_03_8h, predicciones_RL_03_8h)
    # Metricas RF
    mse_RF_03_8h = mean_squared_error(Y_03_8h, predicciones_RF_03_8h)
    mae_RF_03_8h = mean_absolute_error(Y_03_8h, predicciones_RF_03_8h)
    r2_RF_03_8h = r2_score(Y_03_8h, predicciones_RF_03_8h)
    # Metricas RN
    mse_RN_03_8h = mean_squared_error(Y_03_8h, predicciones_RN_03_8h)
    mae_RN_03_8h = mean_absolute_error(Y_03_8h, predicciones_RN_03_8h)
    r2_RN_03_8h = r2_score(Y_03_8h, predicciones_RN_03_8h)
    
    # Impresion
    print(f'03 8h')
    print(f'MSE: RL-> {mse_RL_03_8h} | RF-> {mse_RF_03_8h}  | RN-> {mse_RN_03_8h}')
    print(f'MAE: RL-> {mae_RL_03_8h} | RF-> {mae_RF_03_8h} | RN-> {mae_RN_03_8h}')
    print(f'R2: RL-> {r2_RL_03_8h} | RF-> {r2_RF_03_8h} | RN-> {r2_RN_03_8h}')
    print(f'Predicciones: RL-> {prediccion_RL_03_8h} | RF-> {prediccion_RF_03_8h} | RN-> {prediccion_RN_03_8h}')


    # PREDICCION NOX #
    # -------------- #
    # Division de columnas del DF
    X_NOX = df_group_by_date_clean[['SO2', 'PM2,5', 'PM10', 'O3 8h', 'Tolueno']]
    Y_NOX = df_group_by_date_clean['NOX']

    # Cross Validation RL
    predicciones_RL_NOX = cross_val_predict(modelo_RL, X_NOX, Y_NOX, cv=kf)
    # Cross Validation RF
    predicciones_RF_NOX = cross_val_predict(modelo_RF, X_NOX, Y_NOX, cv=kf)
    # Cross Validation RN
    predicciones_RN_NOX = cross_val_predict(modelo_RN, X_NOX, Y_NOX, cv=kf)

    # Prediccion RL
    prediccion_RL_NOX = predicciones_RL_NOX.mean()
    # Prediccion RL
    prediccion_RF_NOX = predicciones_RF_NOX.mean()
    # Prediccion RL
    prediccion_RN_NOX = predicciones_RN_NOX.mean()

    # Metricas RL
    mse_RL_NOX = mean_squared_error(Y_NOX, predicciones_RL_NOX)
    mae_RL_NOX = mean_absolute_error(Y_NOX, predicciones_RL_NOX)
    r2_RL_NOX = r2_score(Y_NOX, predicciones_RL_NOX)
    # Metricas RF
    mse_RF_NOX = mean_squared_error(Y_NOX, predicciones_RF_NOX)
    mae_RF_NOX = mean_absolute_error(Y_NOX, predicciones_RF_NOX)
    r2_RF_NOX = r2_score(Y_NOX, predicciones_RF_NOX)
    # Metricas RN
    mse_RN_NOX = mean_squared_error(Y_NOX, predicciones_RN_NOX)
    mae_RN_NOX = mean_absolute_error(Y_NOX, predicciones_RN_NOX)
    r2_RN_NOX = r2_score(Y_NOX, predicciones_RN_NOX)
    
    # Impresion
    print(f'NOX')
    print(f'MSE: RL-> {mse_RL_NOX} | RF-> {mse_RF_NOX}  | RN-> {mse_RN_NOX}')
    print(f'MAE: RL-> {mae_RL_NOX} | RF-> {mae_RF_NOX} | RN-> {mae_RN_NOX}')
    print(f'R2: RL-> {r2_RL_NOX} | RF-> {r2_RF_NOX} | RN-> {r2_RN_NOX}')
    print(f'Predicciones: RL-> {prediccion_RL_NOX} | RF-> {prediccion_RF_NOX} | RN-> {prediccion_RN_NOX}')