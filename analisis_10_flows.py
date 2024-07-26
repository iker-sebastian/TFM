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

    '''plt.scatter(df_flows['vehiculos'], np.zeros_like(df_flows['vehiculos']), c=df_flows['afluencia'], cmap='viridis')
    plt.xlabel('Afluencia de vehículos')
    plt.title('Clusters')
    plt.yticks([])
    plt.show()

    plt.scatter(df_flows['vel_media'], np.zeros_like(df_flows['vel_media']), c=df_flows['vel_circulacion'], cmap='viridis')
    plt.xlabel('Velocidad media de ciruculacion')
    plt.title('Clusters')
    plt.yticks([])
    plt.show()'''