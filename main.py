# Imports
import config
import RD_trafico_flows
import RD_trafico_incidencias
import RD_meteo_calidad_aire
import RD_meteo_estaciones
import RD_meteo_datos
import datetime
import bdd

# ----------------------------- OBETENER MESES Y AÑOS ENTRE FECHA INICIO Y FIN ------------------------------ #

config.Year_Month_Setting(config.fecha_inicial, config.fecha_hoy)

# -------------------------------------------- OBTENER METER_ID ------------------------------------------------ #
'''
# Llamada a la API para obtener el numero de paginas de la API meter_Id
pags_totales = RD_trafico_flows.API_meterId_pags()

while config.num_pag_meter < pags_totales:
    # Llamada a la API para obtener todos los MeterId
    RD_trafico_flows.API_meterId()
    config.num_pag_meter += 1
# Nos aseguramos que son valores unicos
config.array_meterId_unicos =  list(set(config.array_meterId))

# Recorrer array de todos los meter_Id
for meterId in config.array_meterId_unicos:
    print(meterId)
    # Recorrer todos los años y meses de ese meter_Id
    for year_month in config.array_year_month:
        # Llamada a la API FLOWS
        RD_trafico_flows.API_flows(meterId, year_month)'''

# Aplicar la API_calidad_aire para cada provincia
for provincia in config.array_provincia:
    # Llamada a la API CALIDAD AIRE
    RD_meteo_calidad_aire.API_calidad_aire(provincia, config.fecha_inicial, config.fecha_hoy)

# -------------------------------------------- OBTENER ESTACIONES ------------------------------------------------ #

# Llamada a la API para obtener las estaciones de Euskalmet
RD_meteo_estaciones.API_estaciones()

# Recorrer elementos de array, para obtener unica clave de todas las existentes, con snapshot mas reciente
for estacion, snapshot in config.array_estaciones:
    # Comprobar si existe clave
    if estacion in config.diccionario_estaciones:
        # Actualizar valor (es mas actual)
        config.diccionario_estaciones[estacion] = max(config.diccionario_estaciones[estacion], snapshot)
    else:
        # No existe clave, añadir
        config.diccionario_estaciones[estacion] = snapshot

# Guardar en un array los valores unicos
for estacion, snapshot in config.diccionario_estaciones.items():
    config.array_estaciones_unicos.append([estacion, snapshot])

# Llamada a la API para obtener los valores de la estacion en el snapshot mas reciente
for elemento in config.array_estaciones_unicos:
    RD_meteo_estaciones.API_estaciones_snapshot(elemento[0], elemento[1])

# -------------------------------------------- BUCLE CON FECHAS ------------------------------------------------ #

# Bucle para consulta de APIs con fechas de incidencias y datos de euskalmet
while config.fecha_recorrida <= config.fecha_hoy:
    # Setting de variables relacionadas con la fecha
    year, month, day, fecha_completa = config.Fecha_Setting(config.fecha_recorrida)
    # API de incidencias
    RD_trafico_incidencias.API_incidencias(year, month, day)
    # Recorrer todas las estaciones
    for diccionario in config.array_dic_estaciones:
        # Recorrer todos los sensores de la estacion
        for sensor in diccionario['sensores']:
            # Recorrer todas las mediciones utiles
            for medicion in config.array_mediciones:     
                # API de inserción de datos Euskalmet
                RD_meteo_datos.API_datos(diccionario['_id'], sensor, medicion[0], medicion[1], year, month, day)
    # Dia siguiente
    config.fecha_recorrida += datetime.timedelta(days=1)

# ------------------------------------ UNIFICAR FLOW POR DIA Y METERID --------------------------------------- # 

# Función que unifica los flows por meterId y dia
RD_trafico_flows.unificar_Flows()

# -------------------------------------------- INSERCION BDD ------------------------------------------------ # 
     
# Insercion flows
for doc in config.array_dic_flows_unificados:
    print(doc)
    # Actualiza el documento si existe '_id', si no inserta datos
    bdd.coleccion_trafico_flows.update_one({'_id': doc['_id']}, {'$set': doc}, upsert=True)
    
# Insercion incidencias
for doc in config.array_dic_incidencias:
    # Actualiza el documento si existe '_id', si no inserta datos
    bdd.coleccion_trafico_incidencias.update_one({'_id': doc['_id']}, {'$set': doc}, upsert=True)

# Insercion calidad aire
for doc in config.array_dic_meteo_cal_aire:
    # Actualiza el documento si existe '_id', si no inserta datos
    bdd.coleccion_meteo_calidad_aire.update_one({'_id': doc['_id']}, {'$set': doc}, upsert=True)

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
    if doc['medida'] == 'cubic_mean_speed':
        # Actualiza el documento si existe '_id', si no inserta datos
        bdd.coleccion_meteo_viento_vel_media_cubica.update_one({'_id': doc['_id']}, {'$set': doc}, upsert=True)
    if doc['medida'] == 'max_speed':
        # Actualiza el documento si existe '_id', si no inserta datos
        bdd.coleccion_meteo_viento_vel_max.update_one({'_id': doc['_id']}, {'$set': doc}, upsert=True)
    if doc['medida'] == 'mean_speed':
        # Actualiza el documento si existe '_id', si no inserta datos
        bdd.coleccion_meteo_viento_vel_media.update_one({'_id': doc['_id']}, {'$set': doc}, upsert=True)
    if doc['medida'] == 'direction_sigma':
        # Actualiza el documento si existe '_id', si no inserta datos
        bdd.coleccion_meteo_viento_direccion_sigma.update_one({'_id': doc['_id']}, {'$set': doc}, upsert=True)
    if doc['medida'] == 'max_direction':
        # Actualiza el documento si existe '_id', si no inserta datos
        bdd.coleccion_meteo_viento_direccion_max.update_one({'_id': doc['_id']}, {'$set': doc}, upsert=True)

print("Contadores de errores:")
print(f"Meteo_datos: {config.cont_NO_200_meteo_datos}")
print(f"Trafico_incidencias: {config.cont_NO_200_trafico_incidencias}")
print(f"Meteo_calidad_aire: {config.cont_NO_200_meteo_calidad_aire}")
print(f"Meteo_estaciones_snapshot: {config.cont_NO_200_meteo_estaciones_snapshot}")
print(f"Meteo_estaciones: {config.cont_NO_200_meteo_estaciones}")
print(f"Trafico_meteoId: {config.cont_NO_200_trafico_meterId}")
print(f"Trafico_flows: {config.cont_NO_200_trafico_flows}")