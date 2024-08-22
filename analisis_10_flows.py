# Imports
import bdd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from sklearn.cluster import KMeans

# Dataset
dataset_flows = list(bdd.coleccion_flows.find())
# DF
df_flows = pd.DataFrame(dataset_flows)

# Metodo llamado desde analisis
def analisis_flows():
    # Columna a agrupar por clusteres los vehiculos
    X_flows_vehiculos = df_flows[['vehiculos']]
    # Definicion del algoritmo
    clustering_flows_vehiculos = KMeans(n_clusters=5)
    df_flows['afluencia'] = clustering_flows_vehiculos.fit_predict(X_flows_vehiculos)
 
    # Columna a agrupar por clusteres la velocidad media
    X_flows_vel_circulacion = df_flows[['vel_media']]
    # Definicion del algoritmo
    clustering_flows_vel_circulacion = KMeans(n_clusters=5)
    df_flows['vel_circulacion'] = clustering_flows_vel_circulacion.fit_predict(X_flows_vel_circulacion)

    plt.scatter(df_flows['vehiculos'], np.zeros_like(df_flows['vehiculos']), c=df_flows['afluencia'], cmap='viridis')
    plt.xlabel('Afluencia de vehiculos')
    plt.title('Clusters')
    plt.yticks([])
    plt.show()

    plt.scatter(df_flows['vel_media'], np.zeros_like(df_flows['vel_media']), c=df_flows['vel_circulacion'], cmap='viridis')
    plt.xlabel('Velocidad media de ciruculacion')
    plt.title('Clusters')
    plt.yticks([])
    plt.show()

    # Conformacion diccionario de datos
    data_10 = df_flows.to_dict(orient='records')

    for doc in data_10:
        bdd.coleccion_analisis_flows.update_one({'_id': doc['_id']}, {'$set': doc}, upsert=True)

    # Insercion de datos para el analisis en MongoDB
    # Actualiza el documento si existe '_id', si no inserta datos
    
    #bdd.coleccion_analisis_flows.insert_many(data_10)