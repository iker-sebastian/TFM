# Imports
from pymongo import MongoClient

# Conexion con MongoDB
conn = MongoClient('localhost',27017)

# Definicion de la bdd
bdd = conn['TFM']

# Definicion de las colecciones para recogida de datos
coleccion_flows = bdd['flows']
coleccion_incidencias = bdd['incidencias']
coleccion_calidad_aire = bdd['calidad_aire']
coleccion_estaciones = bdd['estaciones']
coleccion_meteo = bdd['meteo']

# Definicion de las colecciones de los datos procesados
coleccion_analisis_flows = bdd['analisis_flows']
coleccion_analisis_calidad_aire = bdd['analisis_calidad_aire']
coleccion_analisis_incidencias = bdd['analisis_incidencias']
coleccion_analisis_meteo = bdd['analisis_meteo']