# Imports
import requests
import config_2024
import time

# Metodo que llama a la API meterId y devuelve las paginas de la respuesta
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

# Metodo que llama a la API meterId y devuelve los valores meterId    
def API_meterId():
    # API de meterId
    url_meterId = f'https://api.euskadi.eus/traffic/v1.0/meters?_page={config_2024.num_pag_meter}'
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
            config_2024.array_meterId.append(int(meterId))
    else:
        config_2024.cont_NO_200_trafico_meterId += 1


# Metodo que llama a la API FLOWS y devuelve datos de flows de un mes, con un meterId y en un dia de la semana en concreto
def API_flows(meterId, year_month):
    # API de flows
    url_flows = f'https://api.euskadi.eus/traffic/v1.0/flows/byYear/{year_month[0]}/{year_month[1]}/byMeter/{meterId}'
    # En caso de fallo un par de intentos adicionales
    for intento in range(config_2024.intentos):
        # Excepción en caso de perdida de conexión
        try:
            # Solcitud
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
                            'meterId': meterId,
                            'source': documento['sourceId'],
                            'fecha': documento['meterDate'],
                            'año': year_month[0],
                            'mes': year_month[1],
                            'vel_media': velocidad_media,
                            'vehiculos': documento['totalVehicles']
                        }
                    # Añade el diccionario a un array
                    config_2024.array_dic_flows.append(doc)
            else:
                config_2024.cont_NO_200_trafico_flows += 1
        # Segunda parte de la excepción
        except requests.exceptions.ConnectionError:
            print(f"Error de comunicación! Estos son los datos: [meterId: {meterId} y fecha: {year_month}")
        except requests.exceptions.ReadTimeout:
            print(f"Tiempo de espera agotado. Intento {intento + 1}. Se reintentará...")
            if intento < config_2024.intentos -1:
                time.sleep(5)
            else:
                print("El tiempo de espera se agotó definitivamente")
        intento = 0

# Metodo que llama a la API FLOWS y devuelve datos de flows de un mes, con un meterId y en un dia de la semana en concreto
def unificar_Flows():
    for doc in config_2024.array_dic_flows:
        key = (doc['meterId'], doc['fecha'])
        config_2024.diccionario_unificar_flows[key].append(doc)
    
    for documentos_agrupados in config_2024.diccionario_unificar_flows.items():
        if len(documentos_agrupados) == 1:
            doc_update = {
                '_id': documentos_agrupados[0]['meterId'] + '_' + documentos_agrupados[0]['fecha'],
                'meterId': documentos_agrupados[0]['meterId'],
                'source': documentos_agrupados[0]['source'],
                'fecha': documentos_agrupados[0]['fecha'],
                'año': documentos_agrupados[0]['año'],
                'mes': documentos_agrupados[0]['mes'],
                'vel_media': documentos_agrupados[0]['vel_media'],
                'vehiculos': documentos_agrupados[0]['vehiculos']
            }
        else:
            sum_vel_media = sum(doc['vel_media'] for doc in documentos_agrupados)
            sum_vehiculos = sum(doc['vehiculos'] for doc in documentos_agrupados)
            num_docs_agrupados = len(documentos_agrupados)
            prom_vel_media = int(sum_vel_media/num_docs_agrupados)

            doc_update = {
                '_id': doc['meterId'] + '_' + doc['fecha'],
                'meterId': documentos_agrupados[0]['meterId'],
                'source': documentos_agrupados[0]['source'],
                'fecha': documentos_agrupados[0]['fecha'],
                'año': documentos_agrupados[0]['año'],
                'mes': documentos_agrupados[0]['mes'],
                'vel_media': prom_vel_media,
                'vehiculos': sum_vehiculos
            }
        config_2024.array_dic_flows_unificados.append(doc_update)
    return config_2024.array_dic_flows_unificados
        