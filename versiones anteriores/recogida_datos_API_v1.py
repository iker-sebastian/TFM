# Imports
from pymongo import MongoClient
import requests
import datetime

# Conexion con MongoDB
conn = MongoClient('localhost',27017)
# Definicion de la bdd
bdd = conn['TFM']
# Definicion de las colecciones
coleccion_incidencias = bdd['incidencias']
coleccion_flows = bdd['flows']

# Setting de fechas
fecha_hoy =  datetime.date.today()
fecha_inicial = datetime.date(2023, 1, 1)
fecha_recorrida = fecha_inicial

# Funcion para obtener datos complementarios de los flows, anidados dentro de flows
def API_complementaria(meterId):
    # API de datos complementarios a los flows
    url_flows_anyadido = f'https://api.euskadi.eus/traffic/v1.0/meters/{meterId}'
    # Solcitud a la API
    data_flows_anyadido = requests.get(url_flows_anyadido)
    # Respuesta OK de la API con datos extra de los flows
    if data_flows_anyadido.status_code == 200:
        # Formatear respuesta a json
        data_flows_anyadido = data_flows_anyadido.json()
        # Recoger el campo con la informacion util
        propiedades_flows_anyadido = data_flows_anyadido['properties']
        return propiedades_flows_anyadido
    else:
        print('No se han podido introducir los datos de adicionales de los flows a MongoDB')

# Bucle para consulta de API
while fecha_recorrida <= fecha_hoy:
    # Definir variables 'year', 'month' y 'day'
    year = fecha_recorrida.year
    month = fecha_recorrida.month
    day = fecha_recorrida.day

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
            # Actualizar 'meterId'
            documento['meterId'] = API_complementaria(documento['meterId'])
            # Actualiza el documento si existe '_id', si no inserta datos
            coleccion_flows.update_one({'_id': documento['_id']}, {'$set': documento}, upsert=True)
    else:
        print('No se han podido introducir los datos de flows a MongoDB')

    fecha_recorrida += datetime.timedelta(days=1)
