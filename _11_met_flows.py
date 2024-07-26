# Imports
import requests
import config
import time
from collections import defaultdict

# Paginas meter_Id
def API_meterId_pags():
    # API de meterId
    url_meterId_pags = f'https://api.euskadi.eus/traffic/v1.0/meters'
    # Solcitud
    data = requests.get(url_meterId_pags)
    # Respuesta OK
    if data.status_code == 200:
        # Formatear respuesta a json
        data = data.json()
        # Recoger el campo 'totalPages'
        data_totalPages = data['totalPages']
        return data_totalPages

# Valores meter_Id    
def API_meterId():
    # API de meterId
    url_meterId = f'https://api.euskadi.eus/traffic/v1.0/meters?_page={config.contador_pags}'
    # En caso de fallo un par de intentos adicionales
    for intento in range(config.intentos):
        # Excepción en caso de perdida de conexión
        try:
            # Solcitud
            data = requests.get(url_meterId)
            # Respuesta OK
            if data.status_code == 200:
                # Formatear respuesta a json
                data = data.json()
                # Recoger el campo 'features'
                data_features = data['features']
                # Recorrer las features
                for feature in data_features:
                    # Guardar meterId
                    meterId = feature['properties']['meterId']
                    # Añade el meterId a un array
                    config.array_meterId.append(int(meterId))
            else:
                print("Error en la solicitud de la API")

        # Excepción de conexión
        except requests.exceptions.ConnectionError:
            print(f'Error de comunicación!')
            if intento < config.intentos -1:
                print(f'Reintentando... Intento {intento + 1}')
                time.sleep(5)
            else:
                print('El número máximo de intentos ha sido alcanzado')
                break

        # Excepción de tiempo de espera
        except requests.exceptions.ReadTimeout:
            print(f'Tiempo de espera agotado. Intento {intento + 1}. Se reintentará...')
            if intento < config.intentos -1:
                time.sleep(5)
            else:
                print('El tiempo de espera se agotó definitivamente')
                break

# Datos de flows de un mes con un meterId
def API_flows_pags(meter, year_month):
    # API de flows
    url_flows_pags = f'https://api.euskadi.eus/traffic/v1.0/flows/byYear/{year_month[0]}/byMeter/{meter}'
    # Solcitud
    data = requests.get(url_flows_pags)
    # Obtener paginas por meterId
    if data.status_code == 200:
        # Formatear respuesta a json
        data = data.json()
        # Recoger el campo 'totalPages'
        data_totalPages = data['totalPages']
        return data_totalPages

# Datos de flows de un mes con un meterId
def API_flows(meter, year_month):
    # API de flows
    url_flows = f'https://api.euskadi.eus/traffic/v1.0/flows/byYear/{year_month[0]}/byMeter/{meter}1?_page={config.contador_pags}'
    # En caso de fallo un par de intentos adicionales
    for intento in range(config.intentos):
        # Excepción en caso de perdida de conexión
        try:
            # Solicitud
            data = requests.get(url_flows, timeout=30)
            # Respuesta OK
            if data.status_code == 200:
                # Formatear respuesta a json
                data = data.json()
                # Recoger el campo 'flows'
                data_flows = data['flows']
                for documento in data_flows:
                    velocidad_media = documento.get('speedAvg', 0)
                    # Creo un diccionario con los datos que me interesan
                    doc = {
                            '_id': documento['meterId'] + '_' + documento['meterDate'] + '_' + documento['timeRank'],
                            'meterId': meter,
                            'source': documento['sourceId'],
                            'fecha': documento['meterDate'],
                            'año': year_month[0],
                            'mes': year_month[1],
                            'vel_media': velocidad_media,
                            'vehiculos': documento['totalVehicles']
                        }
                    # Añade el diccionario a un array
                    config.array_dic_flows.append(doc)
            else:
                print("Error en la solicitud de la API")
            break

        # Excepción de conexión
        except requests.exceptions.ConnectionError:
            print(f'Error de comunicación! Estos son los datos: [meterId: {meterId} y fecha: {year_month}')
            if intento < config.intentos -1:
                print(f'Reintentando... Intento {intento + 1}')
                time.sleep(5)
            else:
                print('El número máximo de intentos ha sido alcanzado')
                break

        # Excepción de tiempo de espera
        except requests.exceptions.ReadTimeout:
            print(f'Tiempo de espera agotado. Intento {intento + 1}. Se reintentará...')
            if intento < config.intentos -1:
                time.sleep(5)
            else:
                print('El tiempo de espera se agotó definitivamente')
                break

# Obtener un unico registro por día
def unificar_Flows():
    # Definicion diccionario que agrupara conjuntos
    diccionarios_agrupados = defaultdict(list)
    # Se recorre el diccionario principañ
    for dic in config.array_dic_flows:
        # Se define el filtro de agrupacion
        filtro = (dic['meterId'], dic['fecha'])
        # Se añaden los diccionarios a diccionarios agrupados
        diccionarios_agrupados[filtro].append(dic)

    # Recorrer grupos de diccionarios (agrupados por fecha y meterId)
    for filtro, lista_dic in diccionarios_agrupados.items():
        meterId, fecha = filtro
        suma_vehiculos = sum(int(dic['vehiculos']) for dic in lista_dic)
        suma_vel_media = sum(int(dic['vel_media']) for dic in lista_dic)
        media_vel_media = suma_vel_media / len(lista_dic)
        # Parametros que no se unifican
        source = lista_dic[0]['source']
        año = lista_dic[0]['año']
        mes = lista_dic[0]['mes']
        # Conformar diccionario unificado
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
        # Añadir diccionarios unificados a array
        config.array_dic_flows_unificados.append(dic_unificado)
        