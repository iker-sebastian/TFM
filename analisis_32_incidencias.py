# Imports
import bdd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from sklearn.cluster import KMeans

# Metodo para verificar correcto formato de la fecha
def fechas_incompletas(fecha):
    # Verificar si los segundos estan presentes
    if len(fecha) == 16:
        return fecha + ':00'
    return fecha

# Dataset
dataset_incidencias = list(bdd.coleccion_incidencias.find())
# DF
df_incidencias = pd.DataFrame(dataset_incidencias)

# Metodo llamado desde analisis
def analisis_incidencias():
    # Unificar nomenclatura provincias
    df_incidencias['province'] = df_incidencias['province'].replace('Alava-Araba', 'ARABA')
    df_incidencias['province'] = df_incidencias['province'].replace('Bizkaia', 'BIZKAIA')
    df_incidencias['province'] = df_incidencias['province'].replace('Gipuzkoa', 'GIPUZKOA')
    # Aplicar conversion de fechas incompletas
    df_incidencias['startDate'] = df_incidencias['startDate'].apply(fechas_incompletas)
    # Convertir la columna startDate al formato de fecha
    df_incidencias['startDate'] = pd.to_datetime(df_incidencias['startDate'], errors='coerce', format='%Y-%m-%dT%H:%M:%S')
    # Agrupar por fecha completa y provincia y contar el número de incidencias
    df_group_by_date = df_incidencias.groupby([df_incidencias['startDate'].dt.date, 'province', 'incidenceType']).size().reset_index(name='num_incidentes')

    # Columna a agrupar por clusteres los incidencias
    X_incidencias = df_group_by_date[['num_incidentes']]
    # Definicion del algoritmo
    clustering_incidencias = KMeans(n_clusters=3)
    df_group_by_date['nivel_incidencias'] = clustering_incidencias.fit_predict(X_incidencias)

    print(df_group_by_date.head())

    plt.scatter(df_group_by_date['num_incidentes'], np.zeros_like(df_group_by_date['num_incidentes']), c=df_group_by_date['nivel_incidencias'], cmap='viridis')
    plt.xlabel('Numero de incidencias')
    plt.title('Clusters')
    plt.yticks([])
    plt.show()