# Imports
import config
import datetime
import _41_incidencias
import _42_meteorologia
import bdd

# Setup de fecha inicial y final
config.Year_Month_Setting(config.fecha_inicial, config.fecha_hoy)

# Bucle para consulta de APIs con fechas de incidencias y datos de euskalmet
while config.fecha_recorrida <= config.fecha_hoy:
    # Setting de variables relacionadas con la fecha
    year, month, day, fecha_completa = config.Fecha_Setting(config.fecha_recorrida)
    # API de incidencias
    _41_incidencias.API_incidencias(year, month, day)
    # Recorrer todas las estaciones
    for diccionario in config.array_dic_estaciones:
        # Recorrer todos los sensores de la estacion
        for sensor in diccionario['sensores']:
            # Recorrer todas las mediciones utiles
            for medicion in config.array_mediciones:     
                # API de inserción de datos Euskalmet
                _42_meteorologia.API_datos(diccionario['_id'], sensor, medicion[0], medicion[1], year, month, day)
    # Dia siguiente
    config.fecha_recorrida += datetime.timedelta(days=1)

# Insercion incidencias
for doc in config.array_dic_incidencias:
    # Actualiza el documento si existe '_id', si no inserta datos
    bdd.coleccion_incidencias.update_one({'_id': doc['_id']}, {'$set': doc}, upsert=True)

# Insercion datos Euskalmet
for doc in config.array_dic_datos_meteo:
    if doc['medida'] == 'humidity':
        # Actualiza el documento si existe '_id', si no inserta datos
        bdd.coleccion_meteo_aire_humedad.update_one({'_id': doc['_id']}, {'$set': doc}, upsert=True)
    if doc['medida'] == 'temperature':
        # Actualiza el documento si existe '_id', si no inserta datos
        bdd.coleccion_meteo_aire_temperatura.update_one({'_id': doc['_id']}, {'$set': doc}, upsert=True)
    if doc['medida'] == 'superficial_wetting':
        # Actualiza el documento si existe '_id', si no inserta datos
        bdd.coleccion_meteo_atm_humedad_superficie.update_one({'_id': doc['_id']}, {'$set': doc}, upsert=True)
    if doc['medida'] == 'visibility':
        # Actualiza el documento si existe '_id', si no inserta datos
        bdd.coleccion_meteo_atm_visibilidad.update_one({'_id': doc['_id']}, {'$set': doc}, upsert=True)
    if doc['medida'] == 'precipitation':
        # Actualiza el documento si existe '_id', si no inserta datos
        bdd.coleccion_meteo_precipitaciones.update_one({'_id': doc['_id']}, {'$set': doc}, upsert=True)
    if doc['medida'] == 'mean_speed':
        # Actualiza el documento si existe '_id', si no inserta datos
        bdd.coleccion_meteo_viento_vel_media.update_one({'_id': doc['_id']}, {'$set': doc}, upsert=True)
    if doc['medida'] == 'direction_sigma':
        # Actualiza el documento si existe '_id', si no inserta datos
        bdd.coleccion_meteo_viento_direccion_sigma.update_one({'_id': doc['_id']}, {'$set': doc}, upsert=True)
