# Imports
from pymongo import MongoClient
import requests
import datetime
import token_jwt_euskalmet

#----------------------------------------------- CONEXION BDD ----------------------------------------------#

# Conexion con MongoDB
conn = MongoClient('localhost',27017)
# Definicion de la bdd
bdd = conn['TFM']
# Definicion de las colecciones
coleccion_incidencias = bdd['trafico_incidencias']
coleccion_flows = bdd['trafico_flows']
coleccion_calidad_aire = bdd['calidad_aire']
coleccion_estaciones_euskalmet = bdd['estaciones_euskalmet']
coleccion_sensores_euskalmet = bdd['sensores_euskalmet']
coleccion_data_euskalmet = bdd['datos_euskalmet']

#--------------------------------------------- PARAMETROS -----------------------------------------------#

# Setting de fechas
fecha_hoy =  datetime.date.today()
fecha_inicial = datetime.date(2024, 4, 1)
fecha_recorrida = fecha_inicial

# Arrays
array_estaciones = [] # Array estaciones
array_sensores = [] # Array sensores 
array_snapshot_estaciones = [] # Array para almacenar los snapshot de cada estacion

# Iteradores
pos_estacion = 0 # Iterador para array estaciones
pos_sensor = 0 # Iterador para array estaciones

#---------------------------------------------- FUNCIONES --------------------------------------------#

# FLOWS
def API_complementaria_flows(meterId):
    # API de datos complementarios a los flows
    url_flows_propiedades = f'https://api.euskadi.eus/traffic/v1.0/meters/{meterId}'
    # Solcitud a la API
    data_flows_propiedades = requests.get(url_flows_propiedades)
    # Respuesta OK de la API con propiedades de flows
    if data_flows_propiedades.status_code == 200:
        # Formatear respuesta a json
        data_flows_propiedades = data_flows_propiedades.json()
        # Recoger el campo con la informacion util
        flows_propiedades = data_flows_propiedades['properties']
        # Actualiza el documento si existe '_id', si no inserta datos
        return flows_propiedades
    else:
        print(f'No se han podido encontrar propiedades de el flow {meterId}')

# ESTACIONES EUSKALMET
def API_complementaria_estaciones(stationId):
    # API de Euskalmet para obtener informacion de una estacion
    url_estacion = f'https://api.euskadi.eus/euskalmet/stations/{stationId}'
    # Solcitud a la API
    data_estacion = requests.get(url_estacion, headers=token_jwt_euskalmet.headers)
    # Respuesta OK de la API con propiedades de flows
    if data_estacion.status_code == 200:
        # Formatear respuesta a json
        data_estacion = data_estacion.json()
        for snapshot in data_estacion:
            # Crea campo 'date'
            snapshot['date'] = snapshot['key'][-8:]
            # Añadir estaciones a array
            array_snapshot_estaciones.append(snapshot['date'])
        # Llamada API complementaria de propiedades de las estaciones
        ultima_snapshot = array_snapshot_estaciones[-1]
        API_complementaria_propiedades_estaciones(stationId, ultima_snapshot)
        array_snapshot_estaciones.clear()
    else:
        print('No se han podido introducir las estaciones a MongoDB')

# PROPIEDADES ESTACIONES EUSKALMET
def API_complementaria_propiedades_estaciones (stationId, date):
    # API de Euskalmet para obtener informacion de la estacion por fecha
    url_estaciones_propiedades = f'https://api.euskadi.eus/euskalmet/stations/{stationId}/{date}'
    # Solcitud a la API
    data_estaciones_propiedades = requests.get(url_estaciones_propiedades, headers=token_jwt_euskalmet.headers)
    # Respuesta OK de la API con propiedades de flows
    if data_estaciones_propiedades.status_code == 200:
        # Formatear respuesta a json
        data_estaciones_propiedades = data_estaciones_propiedades.json()
        # Crea campo '_id'
        data_estaciones_propiedades['_id'] = data_estaciones_propiedades['stationId'] + '_' + date
        # Crea campo 'date'
        data_estaciones_propiedades['date'] = date
        # Actualiza el documento si existe '_id', si no inserta datos
        coleccion_estaciones_euskalmet.update_one({'_id': data_estaciones_propiedades['_id']}, {'$set': data_estaciones_propiedades}, upsert=True)
    else:
        print('No se han podido introducir las propiedades de las estaciones a MongoDB')

# SENSORES EUSKALMET
def API_complementaria_sensores (sensorId):
    # API de Euskalmet para obtener datos detallados por sensor
    url_sensores_propiedades = f'https://api.euskadi.eus/euskalmet/sensors/{sensorId}'
    # Solcitud a la API
    data_sensores_propiedades = requests.get(url_sensores_propiedades, headers=token_jwt_euskalmet.headers)
    # Respuesta OK de la API con propiedades de flows
    if data_sensores_propiedades.status_code == 200:
        # Formatear respuesta a json
        data_sensores_propiedades = data_sensores_propiedades.json()
        # Crea campo '_id'
        data_sensores_propiedades['_id'] = data_sensores_propiedades['sensorId']
        # Actualiza el documento si existe '_id', si no inserta datos
        coleccion_sensores_euskalmet.update_one({'_id': data_sensores_propiedades['_id']}, {'$set': data_sensores_propiedades}, upsert=True)
    else:
        print('No se han podido introducir las propiedades de los sensores a MongoDB')

# DATOS EUSKALMET
def API_datos_euskalmet (stationId, sensorId, year, month, day):
    # API de Euskalmet para obtener todos los datos recogidos de una estacion en un dia
    url_datos_euskalmet = f'https://api.euskadi.eus/euskalmet/readings/summarized/byDay/forStation/{stationId}/{sensorId}/measures/measureForWater/precipitation/at/{year}/{month}/{day}'
    # Solcitud a la API
    data_euskalmet = requests.get(url_datos_euskalmet, headers=token_jwt_euskalmet.headers)
    # Respuesta OK de la API con propiedades de flows
    if data_euskalmet.status_code == 200:
        # Formatear respuesta a json
        data_euskalmet = data_euskalmet.json()
        # Crea campo '_id'
        data_euskalmet['_id'] = day + month + year + '_' + data_euskalmet['stationId'] + '_' + data_euskalmet['sensorId']
        # Actualiza el documento si existe '_id', si no inserta datos
        coleccion_data_euskalmet.update_one({'_id': data_euskalmet['_id']}, {'$set': data_euskalmet}, upsert=True)
    else:
        print('No se han podido introducir los datos de Euskalmet a MongoDB')

#--------------------------------------------------- APIs --------------------------------------------------#

# CALIDAD DEL AIRE
# Setting de provincia e iterador
provincia = [1, 48, 20] # Alava, Bizakia y Gipuzcoa
provincia_strings = ['Alava', 'Bizkaia', 'Gipuzcoa']
i = 0 # Iterador array provincia

for element in provincia:
    # API calidad del aire
    url_cal_aire = f'https://api.euskadi.eus/air-quality/measurements/daily/counties/{provincia[i]}/from/{fecha_inicial}/to/{fecha_hoy}'
    # Solcitud a la API de la calidad del aire
    data_cal_aire = requests.get(url_cal_aire)
    # Respuesta OK de la API incidencias
    if data_cal_aire.status_code == 200:
        # Formatear respuesta a json
        data_cal_aire = data_cal_aire.json()
        for documento in data_cal_aire:
            # Crea campo '_id'
            documento['_id'] = provincia_strings[i] + '_' + documento['date']
            # Actualiza el documento si existe '_id', si no inserta datos
            coleccion_calidad_aire.update_one({'_id': documento['_id']}, {'$set': documento}, upsert=True)
    else:
        print('No se han podido introducir los datos de la calidad del aire a MongoDB')
    i += 1

# ESTACIONES, SENSORES Y MEDICIONES EUSKALMET
# API de Euskalmet todas las estaciones
url_estaciones_all = f'https://api.euskadi.eus/euskalmet/stations'
# API de Euskalmet todos los sensores
url_sensores_all = f'https://api.euskadi.eus/euskalmet/sensors'

# Solicitudes a las API
data_estaciones_all = requests.get(url_estaciones_all, headers=token_jwt_euskalmet.headers)
data_sensores_all = requests.get(url_sensores_all, headers=token_jwt_euskalmet.headers)

# Respuesta OK de la API estaciones
if data_estaciones_all.status_code == 200:
    # Formatear respuesta a json
    data_estaciones_all = data_estaciones_all.json()
    for estacion in data_estaciones_all:
        # Añadir estaciones a array
        array_estaciones.append(estacion['stationId'])
else:
    print('No se han podido guardar las estaciones al array')

# Respuesta OK de la API sensores
if data_sensores_all.status_code == 200:
    # Formatear respuesta a json
    data_sensores_all = data_sensores_all.json()
    for sensor in data_sensores_all:
        # Añadir sensores a array
        array_sensores.append(sensor['sensorId'])
else:
    print('No se han podido guardar los sensores al array')

# Setting array con valores unicos
array_estaciones_unicos =  list(set(array_estaciones))
array_sensores_unicos =  list(set(array_sensores))

#print(array_estaciones_unicos)
#print(array_sensores_unicos)
#print(array_tipo_mediciones_unicos)
#print(array_mediciones_unicos)

# INCIDENCIAS Y FLOWS (CON BUCLE POR FECHA)
# Bucle para consulta de API
while fecha_recorrida <= fecha_hoy:
    # Definir variables 'year', 'month' y 'day'
    year = fecha_recorrida.year
    month = str(fecha_recorrida.month).zfill(2)
    day = str(fecha_recorrida.day).zfill(2)
    fecha_completa = str(year) + month + day

    # API de incidencias
    url_incidencias = f'https://api.euskadi.eus/traffic/v1.0/incidences/byDate/{year}/{month}/{day}?_page=1'
    # API de flows
    url_flows = f'https://api.euskadi.eus/traffic/v1.0/flows/byDate/{year}/{month}/{day}?_page=1'

    # Solcitud a la API
    data_incidencias = requests.get(url_incidencias)
    data_flows = requests.get(url_flows)
    
    # Respuesta OK de la API incidencias
    if data_incidencias.status_code == 200:
        # Formatear respuesta a json
        data_incidencias = data_incidencias.json()
        # Recoger el campo con la informacion util
        incidencias = data_incidencias['incidences']
        for documento in incidencias:
            # Crea campo '_id'
            documento['_id'] = documento['incidenceId']
            # Actualiza el documento si existe '_id', si no inserta datos
            coleccion_incidencias.update_one({'_id': documento['_id']}, {'$set': documento}, upsert=True)
    else:
        print('No se han podido introducir los datos de las incidencias a MongoDB')

    # Respuesta OK de la API flows
    if data_flows.status_code == 200:
        # Formatear respuesta a json
        data_flows = data_flows.json()
        # Recoger el campo con la informacion util
        flows = data_flows['flows']
        for documento in flows:
            # Crea campo '_id'
            documento['_id'] = documento['meterId'] + "_" + documento["meterDate"] + "_" + documento["timeRank"].replace(" ", "")
            # Crea campo 'properties' y llamada a la API
            documento['properties'] = API_complementaria_flows(documento['meterId'])
            # Actualiza el documento si existe '_id', si no inserta datos
            coleccion_flows.update_one({'_id': documento['_id']}, {'$set': documento}, upsert=True)
    else:
        print('No se han podido introducir los datos de flows a MongoDB')
    # Dia siguiente
    fecha_recorrida += datetime.timedelta(days=1)

# LLAMADA API PROPIEDADES ESTACIONES
for estacion in array_estaciones_unicos:
    # Llamada API complementaria estaciones
    API_complementaria_estaciones(estacion)
    pos_estacion += 1
# Reset iterador array de estaciones
pos_estacion = 0

# LLAMADA API PROPIEDADES SENSORES
for sensor in array_sensores_unicos:
    # Llamada API complementaria sensores
    API_complementaria_sensores(sensor)
    pos_sensor += 1
# Reset iterador array de estaciones
pos_sensor = 0
    
# LLAMADA API DATA EUSKALMET
for estacion in array_estaciones_unicos:
    for sensor in array_sensores_unicos:
        API_datos_euskalmet (array_estaciones_unicos[pos_estacion], array_sensores_unicos[pos_sensor], year, month, day)
        pos_sensor += 1
    pos_sensor = 0
    pos_estacion += 1 
pos_estacion = 0

