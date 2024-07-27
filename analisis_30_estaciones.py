# Imports
import bdd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from sklearn.cluster import KMeans

# Dataset
dataset_estaciones = list(bdd.coleccion_estaciones.find())
# DF
df_estaciones = pd.DataFrame(dataset_estaciones)