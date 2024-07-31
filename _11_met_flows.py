# Imports
import config
import requests
from collections import defaultdict
import time

# Paginas meter_Id
def API_meterId_pags():
    # API de las paginas de meterId
    url_meterId_pags = 'https://api.euskadi.eus/traffic/v1.0/meters'
    # Solcitud
    response = requests.get(url_meterId_pags)
    # Respuesta OK
    if response.status_code == 200:
        # Formatear respuesta a json
        data = response.json()
        data_totalPages = data['totalPages']
        return data_totalPages

# Valores meter_Id    
def API_meterId(page):
    # API de los datos de meterId
    url_meterId = f'https://api.euskadi.eus/traffic/v1.0/meters?_page={page}'
    # Intentos para redundancia
    for intento in range(config.intentos):
        # Excepcion
        try:
            # Solcitud
            response = requests.get(url_meterId)
            # Respuesta OK
            if response.status_code == 200:
                # Formatear respuesta a json
                data = response.json()
                data_features = data['features']
                for feature in data_features:
                    meterId = feature['properties']['meterId']
                    # Añadir meterId a array
                    config.array_meterId.append(int(meterId))
                break
        # Segunda parte excepcion (ConnectionError, HTTPError)
        except (requests.ConnectionError, requests.Timeout, requests.HTTPError):
            if intento < config.intentos - 1:
                time.sleep(5)
            else:
                print('El numero maximo de intentos ha sido alcanzado')

# Datos de flows de un mes con un meterId
def API_flows_pags(meterId, year_month):
    # API de las paginas de flows
    url_flows_pags = f'https://api.euskadi.eus/traffic/v1.0/flows/byYear/{year_month[0]}/byMeter/{meterId}'
    # Solcitud
    response = requests.get(url_flows_pags)
    # Respuesta OK
    if response.status_code == 200:
        # Formatear respuesta a json
        data = response.json()
        data_totalPages = data['totalPages']
        return data_totalPages

# Datos de flows de un mes con un meterId
def API_flows(meterId, year_month, page):
    # API de los datos de flows
    url_flows = f'https://api.euskadi.eus/traffic/v1.0/flows/byYear/{year_month[0]}/byMeter/{meterId}1?_page={page}'
    # Intentos para redundancia
    for intento in range(config.intentos):
        # Excepcion
        try:
            # Solcitud
            response = requests.get(url_flows)
            # Respuesta OK
            if response.status_code == 200:
                # Formatear respuesta a json
                data = response.json()
                data_flows = data['flows']
                # Recorrer flows
                for documento in data_flows:
                    # Si no encuentra velocidad media, es 0
                    velocidad_media = documento.get('speedAvg', 0)
                    # Crear un diccionario con los datos que interesan
                    doc = {
                        '_id': documento['meterId'] + '_' + documento['meterDate'] + '_' + documento['timeRank'],
                        'meterId': meterId,
                        'source': documento['sourceId'],
                        'fecha': documento['meterDate'],
                        'año': year_month[0],
                        'mes': year_month[1],
                        'vel_media': velocidad_media,
                        'vehiculos': documento['totalVehicles']
                    }
                    # Añadir el diccionario a un array
                    config.array_dic_flows.append(doc)
                break
        # Segunda parte excepcion (ClientConnectionError, ClientResponeError, TimeoutError)
        except (requests.ConnectionError, requests.Timeout, requests.HTTPError):
            if intento < config.intentos - 1:
                time.sleep(5)
            else:
                print('El numero maximo de intentos ha sido alcanzado')

# Obtener un unico registro por dia
def unificar_Flows():
    # Se crea un nuevo elemento con formato diccionario
    diccionarios_agrupados = defaultdict(list)
    # Se recorren los diccionarios almacenados
    for dic in config.array_dic_flows:
        # Se aplica el filtro del meterId y de la fecha
        filtro = (dic['meterId'], dic['fecha'])
        # El objeti resultante se añade al nuevo diccionario
        diccionarios_agrupados[filtro].append(dic)

    # Aplicacion del filtro para los elementos
    for filtro, lista_dic in diccionarios_agrupados.items():
        # Filtro de la agrupacion
        meterId, fecha = filtro
        # Se suman los vehiculos de un dia y un determinado meterId
        suma_vehiculos = sum(int(dic['vehiculos']) for dic in lista_dic)
         # Se suman la velocidad media en un dia y un determinado meterId
        suma_vel_media = sum(int(dic['vel_media']) for dic in lista_dic)
         # Se divide la velocidad total obtenida entre el numero de mediciones
        media_vel_media = suma_vel_media / len(lista_dic)
        # Se obtiene el primer source de todos los elementos
        source = lista_dic[0]['source']
        # Se obtiene el primer año de todos los elementos
        año = lista_dic[0]['año']
        # Se obtiene el primer mes de todos los elementos
        mes = lista_dic[0]['mes']
        # Se conforma el diccionario
        dic_unificado = {
            '_id': str(meterId) + '_' + fecha,
            'meterId': meterId,
            'source': source,
            'fecha': fecha,
            'año': año,
            'mes': mes,
            'vel_media': media_vel_media,
            'vehiculos': suma_vehiculos
        }
        # Añadir el diccionario a un array
        config.array_dic_flows_unificados.append(dic_unificado)
