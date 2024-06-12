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
coleccion_meteo_aire_humedad = bdd['meteo_aire_humedad']
coleccion_meteo_aire_temperatura = bdd['meteo_aire_temperatura']
coleccion_meteo_atm_humedad_superficie = bdd['meteo_atm_humedad_superficie']
coleccion_meteo_atm_visibilidad = bdd['meteo_atm_visibilidad']
coleccion_meteo_precipitaciones = bdd['meteo_precipitaciones']
coleccion_meteo_viento_vel_media = bdd['meteo_viento_vel_media']
coleccion_meteo_viento_direccion_sigma = bdd['meteo_viento_direccion_sigma']
