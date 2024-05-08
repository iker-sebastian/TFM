# Imports
import requests
import config

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
    url_meterId = f'https://api.euskadi.eus/traffic/v1.0/meters?_page={config.num_pag_meter}'
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
        config.cont_NO_200_trafico_meterId += 1


# Metodo que llama a la API FLOWS y devuelve datos de flows de un mes, con un meterId y en un dia de la semana en concreto
def API_flows(meterId, year_month):
    # API de flows
    url_flows = f'https://api.euskadi.eus/traffic/v1.0/flows/byYear/{year_month[0]}/{year_month[1]}/byMeter/{meterId}'
    #f'https://api.euskadi.eus/traffic/v1.0/flows/byMonth/{year_month[0]}/{year_month[1]}/byMeter/{meterId}/byDayOfWeek/{dia_sem}'
    # Excepción en caso de perdida de conexión
    try:
        # Solcitud
        data = requests.get(url_flows)
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
                        #'dia_de_la_semana': dia_sem,
                        'intervalo_tiempo': documento['timeRank'],
                        'vel_media': velocidad_media,
                        'vehiculos': documento['totalVehicles']
                    }
                # Añade el diccionario a un array
                config.array_dic_flows.append(doc)
        else:
            config.cont_NO_200_trafico_flows += 1
    # Segunda parte de la excepción
    except requests.exceptions.ConnectionError:
        print(f"Error de comunicación! Estos son los datos: [meterId: {meterId} y fecha: {year_month}")
    except requests.exceptions.Timeout:
        print(f"Error de comunicación! Estos son los datos: [meterId: {meterId} y fecha: {year_month}")
        