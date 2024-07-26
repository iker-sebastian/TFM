# Imports
import bdd
import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

# Dataset
dataset_calidad_aire = list(bdd.coleccion_calidad_aire.find())
# DF
df_calidad_aire = pd.DataFrame(dataset_calidad_aire)

def analisis_calidad_aire():
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

    # DF para eliminar los campos que no aportan información
    df_numerico = df_calidad_aire.drop(columns=['_id', 'id_estacion', 'nombre', 'unidad_medicion'])

    # Borrar valores atipicos o erroneos
    df_numerico_clean = df_numerico.drop(df_numerico[df_numerico['SO2'] == -1].index)

    # DF agrupado
    df_group_by_date = df_numerico_clean.groupby(['fecha', 'provincia']).mean().reset_index()

    # Rellenar valores nulos con 0 para prediccion
    df_group_by_date_clean = df_group_by_date.fillna(0)


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
    print(f'Tolueno')
    print(f'RL: {mse_RL_Tolueno} | {mae_RL_Tolueno} | {r2_RL_Tolueno}')
    print(f'RN: {mse_RN_Tolueno} | {mae_RN_Tolueno} | {r2_RN_Tolueno}')
    print(f'RF: {mse_RF_Tolueno} | {mae_RF_Tolueno} | {r2_RF_Tolueno}')


    # PREDICCION SO2 #
    # -------------- #
    X_SO2 = df_group_by_date_clean[['PM2,5', 'PM10', 'O3 8h', 'Tolueno', 'NOX']]
    Y_SO2 = df_group_by_date_clean['SO2']

    # Division de datos
    X_SO2_train, X_SO2_test, Y_SO2_train, Y_SO2_test = train_test_split(X_SO2, Y_SO2, test_size=0.2)

    # Entrenamiento RL
    modelo_RL.fit(X_SO2_train, Y_SO2_train)
    # Entrenamiento RN
    modelo_RN.fit(X_SO2_train, Y_SO2_train, epochs=400, batch_size=64, verbose=0)
    # Entrenamiento RF
    modelo_RF.fit(X_SO2_train, Y_SO2_train)

    # Prediccion RL
    prediccion_RL_SO2 = modelo_RL.predict(X_SO2_test)
    # Prediccion RN
    prediccion_RN_SO2 = modelo_RN.predict(X_SO2_test)
    # Prediccion RF
    prediccion_RF_SO2 = modelo_RF.predict(X_SO2_test)

    # Evaluación
    mse_RN_SO2, mae_RN_SO2 = modelo_RN.evaluate(X_SO2_test, Y_SO2_test)

    # Metricas
    mae_RL_SO2 = mean_absolute_error(Y_SO2_test, prediccion_RL_SO2)
    mse_RL_SO2 = mean_squared_error(Y_SO2_test, prediccion_RL_SO2)
    r2_RL_SO2 = r2_score(Y_SO2_test, prediccion_RL_SO2)
    r2_RN_SO2 = r2_score(Y_SO2_test, prediccion_RN_SO2)
    mae_RF_SO2 = mean_absolute_error(Y_SO2_test, prediccion_RF_SO2)
    mse_RF_SO2 = mean_squared_error(Y_SO2_test, prediccion_RF_SO2)
    r2_RF_SO2 = r2_score(Y_SO2_test, prediccion_RF_SO2)

    # Impresion
    print(f'SO2')
    print(f'RL: {mse_RL_SO2} | {mae_RL_SO2} | {r2_RL_SO2}')
    print(f'RN: {mse_RN_SO2} | {mae_RN_SO2} | {r2_RN_SO2}')
    print(f'RF: {mse_RF_SO2} | {mae_RF_SO2} | {r2_RF_SO2}')


    # PREDICCION PM25 #
    # --------------- #
    X_PM25 = df_group_by_date_clean[['SO2', 'PM10', 'O3 8h', 'Tolueno', 'NOX']]
    Y_PM25 = df_group_by_date_clean['PM2,5']

    # Division de datos
    X_PM25_train, X_PM25_test, Y_PM25_train, Y_PM25_test = train_test_split(X_PM25, Y_PM25, test_size=0.2)

    # Entrenamiento RL
    modelo_RL.fit(X_PM25_train, Y_PM25_train)
    # Entrenamiento RN
    modelo_RN.fit(X_PM25_train, Y_PM25_train, epochs=400, batch_size=64, verbose=0)
    # Entrenamiento RF
    modelo_RF.fit(X_PM25_train, Y_PM25_train)

    # Prediccion RL
    prediccion_RL_PM25 = modelo_RL.predict(X_PM25_test)
    # Prediccion RN
    prediccion_RN_PM25 = modelo_RN.predict(X_PM25_test)
    # Prediccion RF
    prediccion_RF_PM25 = modelo_RF.predict(X_PM25_test)

    # Evaluación
    mse_RN_PM25, mae_RN_PM25 = modelo_RN.evaluate(X_PM25_test, Y_PM25_test)

    # Metricas
    mae_RL_PM25 = mean_absolute_error(Y_PM25_test, prediccion_RL_PM25)
    mse_RL_PM25 = mean_squared_error(Y_PM25_test, prediccion_RL_PM25)
    r2_RL_PM25 = r2_score(Y_PM25_test, prediccion_RL_PM25)
    r2_RN_PM25 = r2_score(Y_PM25_test, prediccion_RN_PM25)
    mae_RF_PM25 = mean_absolute_error(Y_PM25_test, prediccion_RF_PM25)
    mse_RF_PM25 = mean_squared_error(Y_PM25_test, prediccion_RF_PM25)
    r2_RF_PM25 = r2_score(Y_PM25_test, prediccion_RF_PM25)

    # Impresion
    print(f'PM2,5')
    print(f'RL: {mse_RL_PM25} | {mae_RL_PM25} | {r2_RL_PM25}')
    print(f'RN: {mse_RN_PM25} | {mae_RN_PM25} | {r2_RN_PM25}')
    print(f'RF: {mse_RF_PM25} | {mae_RF_PM25} | {r2_RF_PM25}')


    # PREDICCION PM10 #
    # --------------- #
    X_PM10 = df_group_by_date_clean[['SO2', 'PM2,5', 'O3 8h', 'Tolueno', 'NOX']]
    Y_PM10 = df_group_by_date_clean['PM10']

    # Division de datos
    X_PM10_train, X_PM10_test, Y_PM10_train, Y_PM10_test = train_test_split(X_PM10, Y_PM10, test_size=0.2)

    # Entrenamiento RL
    modelo_RL.fit(X_PM10_train, Y_PM10_train)
    # Entrenamiento RN
    modelo_RN.fit(X_PM10_train, Y_PM10_train, epochs=400, batch_size=64, verbose=0)
    # Entrenamiento RF
    modelo_RF.fit(X_PM10_train, Y_PM10_train)

    # Prediccion RL
    prediccion_RL_PM10 = modelo_RL.predict(X_PM10_test)
    # Prediccion RN
    prediccion_RN_PM10 = modelo_RN.predict(X_PM10_test)
    # Prediccion RF
    prediccion_RF_PM10 = modelo_RF.predict(X_PM10_test)

    # Evaluación
    mse_RN_PM10, mae_RN_PM10 = modelo_RN.evaluate(X_PM10_test, Y_PM10_test)

    # Metricas
    mae_RL_PM10 = mean_absolute_error(Y_PM10_test, prediccion_RL_PM10)
    mse_RL_PM10 = mean_squared_error(Y_PM10_test, prediccion_RL_PM10)
    r2_RL_PM10 = r2_score(Y_PM10_test, prediccion_RL_PM10)
    r2_RN_PM10 = r2_score(Y_PM10_test, prediccion_RN_PM10)
    mae_RF_PM10 = mean_absolute_error(Y_PM10_test, prediccion_RF_PM10)
    mse_RF_PM10 = mean_squared_error(Y_PM10_test, prediccion_RF_PM10)
    r2_RF_PM10 = r2_score(Y_PM10_test, prediccion_RF_PM10)

    # Impresion
    print(f'PM10')
    print(f'RL: {mse_RL_PM10} | {mae_RL_PM10} | {r2_RL_PM10}')
    print(f'RN: {mse_RN_PM10} | {mae_RN_PM10} | {r2_RN_PM10}')
    print(f'RF: {mse_RF_PM10} | {mae_RF_PM10} | {r2_RF_PM10}')


    # PREDICCION 03 8h #
    # ---------------- #
    X_03_8h = df_group_by_date_clean[['SO2', 'PM2,5', 'PM10', 'Tolueno', 'NOX']]
    Y_03_8h = df_group_by_date_clean['O3 8h']

    # Division de datos
    X_03_8h_train, X_03_8h_test, Y_03_8h_train, Y_03_8h_test = train_test_split(X_03_8h, Y_03_8h, test_size=0.2)

    # Entrenamiento RL
    modelo_RL.fit(X_03_8h_train, Y_03_8h_train)
    # Entrenamiento RN
    modelo_RN.fit(X_03_8h_train, Y_03_8h_train, epochs=400, batch_size=64, verbose=0)
    # Entrenamiento RF
    modelo_RF.fit(X_03_8h_train, Y_03_8h_train)

    # Prediccion RL
    prediccion_RL_03_8h = modelo_RL.predict(X_03_8h_test)
    # Prediccion RN
    prediccion_RN_03_8h = modelo_RN.predict(X_03_8h_test)
    # Prediccion RF
    prediccion_RF_03_8h = modelo_RF.predict(X_03_8h_test)

    # Evaluación
    mse_RN_03_8h, mae_RN_03_8h = modelo_RN.evaluate(X_03_8h_test, Y_03_8h_test)

    # Metricas
    mae_RL_03_8h = mean_absolute_error(Y_03_8h_test, prediccion_RL_03_8h)
    mse_RL_03_8h = mean_squared_error(Y_03_8h_test, prediccion_RL_03_8h)
    r2_RL_03_8h = r2_score(Y_03_8h_test, prediccion_RL_03_8h)
    r2_RN_03_8h = r2_score(Y_03_8h_test, prediccion_RN_03_8h)
    mae_RF_03_8h = mean_absolute_error(Y_03_8h_test, prediccion_RF_03_8h)
    mse_RF_03_8h = mean_squared_error(Y_03_8h_test, prediccion_RF_03_8h)
    r2_RF_03_8h = r2_score(Y_03_8h_test, prediccion_RF_03_8h)

    # Impresion
    print(f'03 8h')
    print(f'RL: {mse_RL_03_8h} | {mae_RL_03_8h} | {r2_RL_03_8h}')
    print(f'RN: {mse_RN_03_8h} | {mae_RN_03_8h} | {r2_RN_03_8h}')
    print(f'RF: {mse_RF_03_8h} | {mae_RF_03_8h} | {r2_RF_03_8h}')


    # PREDICCION NOX #
    # -------------- #
    X_NOX = df_group_by_date_clean[['SO2', 'PM2,5', 'PM10', 'O3 8h', 'Tolueno']]
    Y_NOX = df_group_by_date_clean['NOX']

    # Division de datos
    X_NOX_train, X_NOX_test, Y_NOX_train, Y_NOX_test = train_test_split(X_NOX, Y_NOX, test_size=0.2)

    # Entrenamiento RL
    modelo_RL.fit(X_NOX_train, Y_NOX_train)
    # Entrenamiento RN
    modelo_RN.fit(X_NOX_train, Y_NOX_train, epochs=400, batch_size=64, verbose=0)
    # Entrenamiento RF
    modelo_RF.fit(X_NOX_train, Y_NOX_train)

    # Prediccion RL
    prediccion_RL_NOX = modelo_RL.predict(X_NOX_test)
    # Prediccion RN
    prediccion_RN_NOX = modelo_RL.predict(X_NOX_test)
    # Prediccion RF
    prediccion_RF_NOX = modelo_RF.predict(X_NOX_test)

    # Evaluación
    mse_RN_NOX, mae_RN_NOX = modelo_RN.evaluate(X_NOX_test, Y_NOX_test)

    # Metricas
    mae_RL_NOX = mean_absolute_error(Y_NOX_test, prediccion_RL_NOX)
    mse_RL_NOX = mean_squared_error(Y_NOX_test, prediccion_RL_NOX)
    r2_RL_NOX = r2_score(Y_NOX_test, prediccion_RL_NOX)
    r2_RN_NOX = r2_score(Y_NOX_test, prediccion_RN_NOX)
    mae_RF_NOX = mean_absolute_error(Y_NOX_test, prediccion_RF_NOX)
    mse_RF_NOX = mean_squared_error(Y_NOX_test, prediccion_RF_NOX)
    r2_RF_NOX = r2_score(Y_NOX_test, prediccion_RF_NOX)

    # Impresion
    print(f'NOX')
    print(f'RL: {mse_RL_NOX} | {mae_RL_NOX} | {r2_RL_NOX}')
    print(f'RN: {mse_RN_NOX} | {mae_RN_NOX} | {r2_RN_NOX}')
    print(f'RF: {mse_RF_NOX} | {mae_RF_NOX} | {r2_RF_NOX}')