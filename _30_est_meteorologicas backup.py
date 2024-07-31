# Imports
import concurrent.futures
import config
import datetime
import _31_met_est_meteorologicas
import _32_incidencias
import _33_meteorologia
import bdd

def main():
    # Setup de fecha inicial y final
    config.Year_Month_Setting(config.fecha_inicial, config.fecha_hoy)

    # Listado de las estaciones de Euskalmet
    _31_met_est_meteorologicas.API_estaciones()

    # Bucle para recorrer todas las estaciones meteorologicas
    for estacion, snapshot in config.array_estaciones:
        # Comprobar si existe clave
        if estacion in config.diccionario_estaciones:
            # Actualizar valor (es mas actual?)
            config.diccionario_estaciones[estacion] = max(config.diccionario_estaciones[estacion], snapshot)
        else:
            # No existe clave, añadir
            config.diccionario_estaciones[estacion] = snapshot

    # Guardar en un array los valores unicos
    for estacion, snapshot in config.diccionario_estaciones.items():
        config.array_estaciones_unicos.append([estacion, snapshot])

    # Llamada a la API para obtener los valores de la estacion en el snapshot mas reciente
    for elemento in config.array_estaciones_unicos:
        _31_met_est_meteorologicas.API_estaciones_snapshot(elemento[0], elemento[1])

    # Insercion estaciones meteorologicas
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
            # Recorrer todos los sensores de la estacion
            for sensor in diccionario['sensores']:
                # Recorrer todas las mediciones utiles
                for medicion in config.array_mediciones:
                    # API de insercion de datos Euskalmet
                    _33_meteorologia.API_datos(diccionario['_id'], sensor, medicion[0], medicion[1], year, month, day)
        # Dia siguiente
        config.fecha_recorrida += datetime.timedelta(days=1)

    # Insercion incidencias
    for doc in config.array_dic_incidencias:
        # Actualiza el documento si existe '_id', si no inserta datos
        bdd.coleccion_incidencias.update_one({'_id': doc['_id']}, {'$set': doc}, upsert=True)

    # Insercion datos Euskalmet
    for doc in config.array_dic_datos_meteo:
        # Actualiza el documento si existe '_id', si no inserta datos
        bdd.coleccion_meteo.update_one({'_id': doc['_id']}, {'$set': doc}, upsert=True)
