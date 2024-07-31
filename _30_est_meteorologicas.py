# Imports
import concurrent.futures
import config
import datetime
import _31_met_est_meteorologicas
import _32_incidencias
import _33_meteorologia
import bdd

def establecer_fecha():
    # Setup de fecha inicial y final
    config.Year_Month_Setting(config.fecha_inicial, config.fecha_hoy)

def recoger_estaciones():
    # Listado de las estaciones de Euskalmet
    _31_met_est_meteorologicas.API_estaciones()

def snapshot_estaciones():
    # Bucle para recorrer todas las estaciones meteorologicas
    for estacion, snapshot in config.array_estaciones:
        # Comprobar si existe clave
        if estacion in config.diccionario_estaciones:
            # Actualizar valor (es mas actual?)
            config.diccionario_estaciones[estacion] = max(config.diccionario_estaciones[estacion], snapshot)
        else:
            # No existe clave, añadir
            config.diccionario_estaciones[estacion] = snapshot

def estaciones_unicas():
    # Guardar en un array los valores unicos
    for estacion, snapshot in config.diccionario_estaciones.items():
        config.array_estaciones_unicos.append([estacion, snapshot])

def valores_estaciones():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(_31_met_est_meteorologicas.API_estaciones_snapshot, elemento[0], elemento[1]) for elemento in config.array_estaciones_unicos]
        for future in concurrent.futures.as_completed(futures):
            future.result()

def insertar_estaciones():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(bdd.coleccion_estaciones.update_one, {'_id': doc['_id']}, {'$set': doc}, True) for doc in config.array_dic_estaciones]
        for future in concurrent.futures.as_completed(futures):
            future.result()

def procesar_datos_dia(fecha):
    year, month, day, _ = config.Fecha_Setting(fecha)
    _32_incidencias.API_incidencias(year, month, day)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for diccionario in config.array_dic_estaciones:
            for sensor in diccionario['sensores']:
                for medicion in config.array_mediciones:
                    futures.append(executor.submit(_33_meteorologia.API_datos, diccionario['_id'], sensor, medicion[0], medicion[1], year, month, day))
        for future in concurrent.futures.as_completed(futures):
            future.result()

def insertar_incidencias():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(bdd.coleccion_incidencias.update_one, {'_id': doc['_id']}, {'$set': doc}, True) for doc in config.array_dic_incidencias]
        for future in concurrent.futures.as_completed(futures):
            future.result()

def insertar_datos_meteo():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(bdd.coleccion_meteo.update_one, {'_id': doc['_id']}, {'$set': doc}, True) for doc in config.array_dic_datos_meteo]
        for future in concurrent.futures.as_completed(futures):
            future.result()

def main():
    establecer_fecha()
    recoger_estaciones()
    snapshot_estaciones()
    estaciones_unicas()

    valores_estaciones()
    insertar_estaciones()

    futures_procesar_datos = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        fecha = config.fecha_recorrida
        while fecha <= config.fecha_hoy:
            futures_procesar_datos.append(executor.submit(procesar_datos_dia, fecha))
            fecha += datetime.timedelta(days=1)

        for future in concurrent.futures.as_completed(futures_procesar_datos):
            try:
                future.result()
            except Exception as e:
                print(f'Ocurrio un error procesando datos del dia: {e}')

    insertar_incidencias()
    insertar_datos_meteo()