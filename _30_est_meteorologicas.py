# Imports
import config
import datetime
import _31_met_est_meteorologicas
import _32_incidencias
import _33_meteorologia
import bdd

# Setup de fecha inicial y final
config.Year_Month_Setting(config.fecha_inicial, config.fecha_hoy)

# Listado de las estaciones de Euskalmet
_31_met_est_meteorologicas.API_estaciones()

# Bucle para recorrer todas las estaciones meteorológicas
for estacion, snapshot in config.array_estaciones:
    # Comprobar si existe clave
    if estacion in config.diccionario_estaciones:
        # Actualizar valor (es más actual?)
        config.diccionario_estaciones[estacion] = max(config.diccionario_estaciones[estacion], snapshot)
    else:
        # No existe clave, añadir
        config.diccionario_estaciones[estacion] = snapshot

# Guardar en un array los valores únicos
for estacion, snapshot in config.diccionario_estaciones.items():
    config.array_estaciones_unicos.append([estacion, snapshot])

# Llamada a la API para obtener los valores de la estación en el snapshot más reciente
for elemento in config.array_estaciones_unicos:
    _31_met_est_meteorologicas.API_estaciones_snapshot(elemento[0], elemento[1])

# Inserción estaciones meteorológicas
for doc in config.array_dic_estaciones:
    # Actualiza el documento si existe '_id', si no inserta datos
    bdd.coleccion_estaciones.update_one({'_id': doc['_id']}, {'$set': doc}, upsert=True)

# Bucle para consulta de APIs con fechas de incidencias y datos de Euskalmet
while config.fecha_recorrida <= config.fecha_hoy:
    # Setting de variables relacionadas con la fecha
    year, month, day, fecha_completa = config.Fecha_Setting(config.fecha_recorrida)
    # API de incidencias
    _32_incidencias.API_incidencias(year, month, day)
    # Recorrer todas las estaciones
    for diccionario in config.array_dic_estaciones:
        # Recorrer todos los sensores de la estación
        for sensor in diccionario['sensores']:
            # Recorrer todas las mediciones útiles
            for medicion in config.array_mediciones:
                # API de inserción de datos Euskalmet
                _33_meteorologia.API_datos(diccionario['_id'], sensor, medicion[0], medicion[1], year, month, day)
    # Día siguiente
    config.fecha_recorrida += datetime.timedelta(days=1)

# Inserción incidencias
for doc in config.array_dic_incidencias:
    # Actualiza el documento si existe '_id', si no inserta datos
    bdd.coleccion_incidencias.update_one({'_id': doc['_id']}, {'$set': doc}, upsert=True)

# Inserción datos Euskalmet
for doc in config.array_dic_datos_meteo:
    # Actualiza el documento si existe '_id', si no inserta datos
    bdd.coleccion_meteo.update_one({'_id': doc['_id']}, {'$set': doc}, upsert=True)
