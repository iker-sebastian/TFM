# Imports
from pymongo import MongoClient

# Conexion con MongoDB
conn = MongoClient('localhost',27017)

# Definicion de la bdd
bdd = conn['TFM']

# Definicion de las colecciones
coleccion_flows = bdd['flows']
coleccion_incidencias = bdd['incidencias']
coleccion_calidad_aire = bdd['calidad_aire']
coleccion_estaciones = bdd['estaciones']
coleccion_meteo = bdd['meteo']