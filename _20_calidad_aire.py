# Imports
import config
import _21_met_calidad_aire
import bdd

# Setup de fecha inicial y final
config.Year_Month_Setting(config.fecha_inicial, config.fecha_hoy)

# Bucle para recorrer todas las provincias
for provincia in config.array_provincia:
    # Llamada a la API calidad aire
    _21_met_calidad_aire.API_calidad_aire(provincia, config.fecha_inicial, config.fecha_hoy)

# Insercion calidad aire
for doc in config.array_dic_meteo_cal_aire:
    # Actualiza el documento si existe '_id', si no inserta datos
    bdd.coleccion_calidad_aire.update_one({'_id': doc['_id']}, {'$set': doc}, upsert=True)