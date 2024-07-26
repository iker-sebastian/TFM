# Imports
import bdd
import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout


# Dataset
dataset_meteo = list(bdd.coleccion_meteo.find())
# Df
df_meteo = pd.DataFrame(dataset_meteo)

def analisis_meteo():
    # Regresion lineal
    modelo_RL = LinearRegression()

    # Red neuronal
    modelo_RN = Sequential()
    modelo_RN.add(Dense(512, activation='relu', input_dim=5))
    modelo_RN.add(Dropout(0.1))
    modelo_RN.add(Dense(512, activation='relu'))
    modelo_RN.add(Dropout(0.1))
    modelo_RN.add(Dense(1, activation="linear"))
    # Compilar modelo
    modelo_RN.compile(optimizer='adam', loss='mse', metrics=['mae'])
    # Resumen del modelo
    modelo_RN.summary()

    # Random Forest
    modelo_RF = RandomForestRegressor(n_estimators=128)

    # PREDICCION TOLUENO #
    # ------------------ #
    X_Tolueno = df_group_by_date_clean[['SO2', 'PM10', 'PM2,5', 'O3 8h', 'NOX']]
    Y_Tolueno = df_group_by_date_clean['Tolueno']

    # Division de datos
    X_Tolueno_train, X_Tolueno_test, Y_Tolueno_train, Y_Tolueno_test = train_test_split(X_Tolueno, Y_Tolueno, test_size=0.2)

    # Entrenamiento RL
    modelo_RL.fit(X_Tolueno_train, Y_Tolueno_train)
    # Entrenamiento RN
    modelo_RN.fit(X_Tolueno_train, Y_Tolueno_train, epochs=400, batch_size=64, verbose=0)
    # Entrenamiento RF
    modelo_RF.fit(X_Tolueno_train, Y_Tolueno_train)

    # Prediccion RL
    prediccion_RL_Tolueno = modelo_RL.predict(X_Tolueno_test)
    # Prediccion RN
    prediccion_RN_Tolueno = modelo_RN.predict(X_Tolueno_test)
    # Prediccion RF
    prediccion_RF_Tolueno = modelo_RF.predict(X_Tolueno_test)

    # Evaluación RN
    mse_RN_Tolueno, mae_RN_Tolueno = modelo_RN.evaluate(X_Tolueno_test, Y_Tolueno_test)

    # Metricas
    mae_RL_Tolueno = mean_absolute_error(Y_Tolueno_test, prediccion_RL_Tolueno)
    mse_RL_Tolueno = mean_squared_error(Y_Tolueno_test, prediccion_RL_Tolueno)
    r2_RN_Tolueno = r2_score(Y_Tolueno_test, prediccion_RN_Tolueno)
    r2_RL_Tolueno = r2_score(Y_Tolueno_test, prediccion_RL_Tolueno)
    mae_RF_Tolueno = mean_absolute_error(Y_Tolueno_test, prediccion_RF_Tolueno)
    mse_RF_Tolueno = mean_squared_error(Y_Tolueno_test, prediccion_RF_Tolueno)
    r2_RF_Tolueno = r2_score(Y_Tolueno_test, prediccion_RF_Tolueno)

    # Impresion
    print(f"Tolueno")
    print(f"RL: {mse_RL_Tolueno} | {mae_RL_Tolueno} | {r2_RL_Tolueno}")
    print(f"RN: {mse_RN_Tolueno} | {mae_RN_Tolueno} | {r2_RN_Tolueno}")
    print(f"RF: {mse_RF_Tolueno} | {mae_RF_Tolueno} | {r2_RF_Tolueno}")