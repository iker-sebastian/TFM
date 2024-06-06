# Imports
import config_2024
import RD_trafico_flows_2024
import RD_trafico_incidencias_2024
import RD_meteo_calidad_aire_2024
import RD_meteo_estaciones_2024
import RD_meteo_datos_2024
import datetime
import bdd_2024

# ----------------------------- OBETENER MESES Y AÑOS ENTRE FECHA INICIO Y FIN ------------------------------ #

config_2024.Year_Month_Setting(config_2024.fecha_inicial, config_2024.fecha_hoy)

# -------------------------------------------- OBTENER METER_ID ------------------------------------------------ #
'''
# Llamada a la API para obtener el numero de paginas de la API meter_Id
pags_totales = RD_trafico_flows_2024.API_meterId_pags()

while config_2024.num_pag_meter < pags_totales:
    # Llamada a la API para obtener todos los MeterId
    RD_trafico_flows_2024.API_meterId()
    config_2024.num_pag_meter += 1
# Nos aseguramos que son valores unicos
config_2024.array_meterId_unicos =  list(set(config_2024.array_meterId))

# Recorrer array de todos los meter_Id
for meterId in config_2024.array_meterId_unicos:
    print(meterId)
    # Recorrer todos los años y meses de ese meter_Id
    for year_month in config_2024.array_year_month:
        # Llamada a la API FLOWS
        RD_trafico_flows_2024.API_flows(meterId, year_month)
'''
# Aplicar la API_calidad_aire para cada provincia
for provincia in config_2024.array_provincia:
    # Llamada a la API CALIDAD AIRE
    RD_meteo_calidad_aire_2024.API_calidad_aire(provincia, config_2024.fecha_inicial, config_2024.fecha_hoy)

# ------------------------------------ UNIFICAR FLOW POR DIA Y METERID --------------------------------------- # 
'''
# Función que unifica los flows por meterId y dia
RD_trafico_flows_2024.unificar_Flows()

# -------------------------------------------- INSERCION bdd_2024 ------------------------------------------------ # 
     
# Insercion flows
for doc in config_2024.array_dic_flows_unificados:
    print(doc)
    # Actualiza el documento si existe '_id', si no inserta datos
    bdd_2024.coleccion_trafico_flows.update_one({'_id': doc['_id']}, {'$set': doc}, upsert=True)

# Insercion incidencias
for doc in config_2024.array_dic_incidencias:
    # Actualiza el documento si existe '_id', si no inserta datos
    bdd_2024.coleccion_trafico_incidencias.update_one({'_id': doc['_id']}, {'$set': doc}, upsert=True)'''

# -------------------------------------------- OBTENER ESTACIONES ------------------------------------------------ #

# Llamada a la API para obtener las estaciones de Euskalmet
RD_meteo_estaciones_2024.API_estaciones()

# Recorrer elementos de array, para obtener unica clave de todas las existentes, con snapshot mas reciente
for estacion, snapshot in config_2024.array_estaciones:
    # Comprobar si existe clave
    if estacion in config_2024.diccionario_estaciones:
        # Actualizar valor (es mas actual)
        config_2024.diccionario_estaciones[estacion] = max(config_2024.diccionario_estaciones[estacion], snapshot)
    else:
        # No existe clave, añadir
        config_2024.diccionario_estaciones[estacion] = snapshot

# Guardar en un array los valores unicos
for estacion, snapshot in config_2024.diccionario_estaciones.items():
    config_2024.array_estaciones_unicos.append([estacion, snapshot])

# Llamada a la API para obtener los valores de la estacion en el snapshot mas reciente
for elemento in config_2024.array_estaciones_unicos:
    RD_meteo_estaciones_2024.API_estaciones_snapshot(elemento[0], elemento[1])

# -------------------------------------------- BUCLE CON FECHAS ------------------------------------------------ #

# Bucle para consulta de APIs con fechas de incidencias y datos de euskalmet
while config_2024.fecha_recorrida <= config_2024.fecha_hoy:
    # Setting de variables relacionadas con la fecha
    year, month, day, fecha_completa = config_2024.Fecha_Setting(config_2024.fecha_recorrida)
    # API de incidencias
    RD_trafico_incidencias_2024.API_incidencias(year, month, day)
    # Recorrer todas las estaciones
    for diccionario in config_2024.array_dic_estaciones:
        # Recorrer todos los sensores de la estacion
        for sensor in diccionario['sensores']:
            # Recorrer todas las mediciones utiles
            for medicion in config_2024.array_mediciones:     
                # API de inserción de datos Euskalmet
                RD_meteo_datos_2024.API_datos(diccionario['_id'], sensor, medicion[0], medicion[1], year, month, day)
    # Dia siguiente
    config_2024.fecha_recorrida += datetime.timedelta(days=1)

# -------------------------------------------- INSERCION bdd_2024 ------------------------------------------------ # 

# Insercion calidad aire
for doc in config_2024.array_dic_meteo_cal_aire:
    # Actualiza el documento si existe '_id', si no inserta datos
    bdd_2024.coleccion_meteo_calidad_aire.update_one({'_id': doc['_id']}, {'$set': doc}, upsert=True)

# Insercion datos Euskalmet
for doc in config_2024.array_dic_datos_meteo:
    if doc['medida'] == 'humidity':
        # Actualiza el documento si existe '_id', si no inserta datos
        bdd_2024.coleccion_meteo_aire_humedad.update_one({'_id': doc['_id']}, {'$set': doc}, upsert=True)
    if doc['medida'] == 'temperature':
        # Actualiza el documento si existe '_id', si no inserta datos
        bdd_2024.coleccion_meteo_aire_temperatura.update_one({'_id': doc['_id']}, {'$set': doc}, upsert=True)
    if doc['medida'] == 'superficial_wetting':
        # Actualiza el documento si existe '_id', si no inserta datos
        bdd_2024.coleccion_meteo_atm_humedad_superficie.update_one({'_id': doc['_id']}, {'$set': doc}, upsert=True)
    if doc['medida'] == 'visibility':
        # Actualiza el documento si existe '_id', si no inserta datos
        bdd_2024.coleccion_meteo_atm_visibilidad.update_one({'_id': doc['_id']}, {'$set': doc}, upsert=True)
    if doc['medida'] == 'precipitation':
        # Actualiza el documento si existe '_id', si no inserta datos
        bdd_2024.coleccion_meteo_precipitaciones.update_one({'_id': doc['_id']}, {'$set': doc}, upsert=True)
    if doc['medida'] == 'cubic_mean_speed':
        # Actualiza el documento si existe '_id', si no inserta datos
        bdd_2024.coleccion_meteo_viento_vel_media_cubica.update_one({'_id': doc['_id']}, {'$set': doc}, upsert=True)
    if doc['medida'] == 'max_speed':
        # Actualiza el documento si existe '_id', si no inserta datos
        bdd_2024.coleccion_meteo_viento_vel_max.update_one({'_id': doc['_id']}, {'$set': doc}, upsert=True)
    if doc['medida'] == 'mean_speed':
        # Actualiza el documento si existe '_id', si no inserta datos
        bdd_2024.coleccion_meteo_viento_vel_media.update_one({'_id': doc['_id']}, {'$set': doc}, upsert=True)
    if doc['medida'] == 'direction_sigma':
        # Actualiza el documento si existe '_id', si no inserta datos
        bdd_2024.coleccion_meteo_viento_direccion_sigma.update_one({'_id': doc['_id']}, {'$set': doc}, upsert=True)
    if doc['medida'] == 'max_direction':
        # Actualiza el documento si existe '_id', si no inserta datos
        bdd_2024.coleccion_meteo_viento_direccion_max.update_one({'_id': doc['_id']}, {'$set': doc}, upsert=True)

print("Contadores de errores:")
print(f"Meteo_datos: {config_2024.cont_NO_200_meteo_datos}")
print(f"Trafico_incidencias: {config_2024.cont_NO_200_trafico_incidencias}")
print(f"Meteo_calidad_aire: {config_2024.cont_NO_200_meteo_calidad_aire}")
print(f"Meteo_estaciones_snapshot: {config_2024.cont_NO_200_meteo_estaciones_snapshot}")
print(f"Meteo_estaciones: {config_2024.cont_NO_200_meteo_estaciones}")
print(f"Trafico_meteoId: {config_2024.cont_NO_200_trafico_meterId}")
print(f"Trafico_flows: {config_2024.cont_NO_200_trafico_flows}")