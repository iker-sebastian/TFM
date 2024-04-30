# Imports
from pymongo import MongoClient
import requests
import datetime

#----------------------------------------------- CONEXION BDD ----------------------------------------------#

# Conexion con MongoDB
conn = MongoClient('localhost',27017)
# Definicion de la bdd
bdd = conn['TFM']
# Definicion de las colecciones
coleccion_incidencias = bdd['incidencias']
coleccion_flows = bdd['flows']
coleccion_propiedades_flows = bdd['propiedades_flows']
coleccion_calidad_aire = bdd['calidad_aire']

#---------------------------------------- SETTING DE FECHAS ----------------------------------------#

# Setting de fechas
fecha_hoy =  datetime.date.today()
fecha_inicial = datetime.date(2024, 3, 28)
fecha_recorrida = fecha_inicial

#---------------------------------------- API PROPIEDADES FLOWS ----------------------------------------#

# API de datos complementarios a los flows
url_propiedades_flows = f'https://api.euskadi.eus/traffic/v1.0/meters'
# Solcitud a la API
data_propiedades_flows = requests.get(url_propiedades_flows)
# Respuesta OK de la API con propiedades de flows
if data_propiedades_flows.status_code == 200:
    # Formatear respuesta a json
    data_propiedades_flows = data_propiedades_flows.json()
    # Recoger el campo con la informacion util
    documentos_flows = data_propiedades_flows['features']
    for documento in documentos_flows:
        propiedades_flows = documento['properties']
        # Crea campo '_id'
        propiedades_flows['_id'] = propiedades_flows['meterId']
        # Actualiza el documento si existe '_id', si no inserta datos
        coleccion_propiedades_flows.update_one({'_id': propiedades_flows['_id']}, {'$set': propiedades_flows}, upsert=True)
else:
    print('No se han podido introducir las propiedades de flows a MongoDB')

#---------------------------------------- API CALIDAD AIRE ----------------------------------------#

# Set variable country e iterador
provincia = [1, 48, 20] # Alava, Bizakia y Gipuzcoa
i = 0 # Iterador

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
            documento['_id'] = documento['date']
            # Actualiza el documento si existe '_id', si no inserta datos
            coleccion_calidad_aire.update_one({'_id': documento['_id']}, {'$set': documento}, upsert=True)
    else:
        print('No se han podido introducir los datos de la calidad del aire a MongoDB')

#---------------------------------------- API INCIDENCIAS & FLOWS ----------------------------------------#

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
            # Actualiza el documento si existe '_id', si no inserta datos
            coleccion_flows.update_one({'_id': documento['_id']}, {'$set': documento}, upsert=True)
    else:
        print('No se han podido introducir los datos de flows a MongoDB')

    fecha_recorrida += datetime.timedelta(days=1)