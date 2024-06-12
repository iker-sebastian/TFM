# Imports
import config
import _31_met_est_meteorologicas
import bdd

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