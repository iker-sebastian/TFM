# Imports
import requests
import config
import token_jwt_euskalmet

# Devuelve el snapshot y la estacion
def GET_snaphot(cadena):
    # Se establece el separador
    particion = cadena.split('/')
    # Se establecen os valores a guardar
    est = particion[2]
    snap = particion[3]
    return est, snap

#Devuelve el sensor del sensorkey
def GET_sensorkey(cadena):
    # Se establece el separador
    particion = cadena.split('/')
    # Se establecen os valores a guardar
    sensor = particion[2]
    return sensor

# Estaciones de Euskalmet
def API_estaciones():
    # API de estaciones Euskalmet
    url_estaciones = 'https://api.euskadi.eus/euskalmet/stations'
    # Solicitud
    data = requests.get(url_estaciones, headers=token_jwt_euskalmet.headers)
    # Respuesta OK
    if data.status_code == 200:
        # Formatear respuesta a json
        data = data.json()
        for estacion in data:
            clave = estacion['key']
            est_id, snapshot = GET_snaphot(clave)
            # Añadir estaciones a array
            config.array_estaciones.append([est_id, snapshot])
    else:
        config.cont_NO_200_meteo_estaciones += 1

# Datos de las estaciones meteorlogicas segun snapshot
def API_estaciones_snapshot(est, snap):
    # API de valores estacion Euskalmet en snapshot
    url_estaciones_snapshot = f'https://api.euskadi.eus/euskalmet/stations/{est}/{snap}'
    # Solcitud
    data = requests.get(url_estaciones_snapshot, headers=token_jwt_euskalmet.headers)
    # Respuesta OK
    if data.status_code == 200:
        # Formatear respuesta a json
        data = data.json()
        # Recoger valores para introducir en el diccionario despues
        sensores = data['sensors']
        # Recorrer sensores
        for sensor in sensores:
            valor_sensor = GET_sensorkey(sensor['sensorKey'])
            config.array_sensores_por_estacion.append(valor_sensor)
        # Creo un diccionario con los datos que me interesan
        doc = {
                '_id': est,
                'tipo_estacion': data['stationType'],
                'nombre': data['name']['SPANISH'],
                'municipio': data['municipality']['SPANISH'],
                'provincia': data['province']['SPANISH'],
                'snapshot': snap,
                'sensores': list(config.array_sensores_por_estacion)
        }
        # Añade el diccionario a un array
        config.array_dic_estaciones.append(doc)
    else:
        config.cont_NO_200_meteo_estaciones_snapshot += 1