# Imports
import requests
import config_2024
import token_jwt_euskalmet_2024

# Metodo que devuelve el snapshot y la estacion
def GET_snaphot(cadena):
    # Se establece el separador
    particion = cadena.split('/')
    # Se establecen os valores a guardar
    est = particion[2]
    snap = particion[3]
    return est, snap

# Metodo que devuelve el sensor del sensorkey
def GET_sensorkey(cadena):
    # Se establece el separador
    particion = cadena.split('/')
    # Se establecen os valores a guardar
    sensor = particion[2]
    return sensor

# Metodo que llama a la API que facilita todas las estaciones de Euskalmet
def API_estaciones():
    # API de estaciones Euskalmet
    url_estaciones = 'https://api.euskadi.eus/euskalmet/stations'
    # Solicitud
    data = requests.get(url_estaciones, headers=token_jwt_euskalmet_2024.headers)
    # Respuesta OK
    if data.status_code == 200:
        # Formatear respuesta a json
        data = data.json()
        for estacion in data:
            clave = estacion['key']
            est_id, snapshot = GET_snaphot(clave)
            # Añadir estaciones a array
            config_2024.array_estaciones.append([est_id, snapshot])
    else:
        config_2024.cont_NO_200_meteo_estaciones += 1

def API_estaciones_snapshot(est, snap):
    # API de valores estacion Euskalmet en snapshot
    url_estaciones_snapshot = f'https://api.euskadi.eus/euskalmet/stations/{est}/{snap}'
    # Solcitud
    data = requests.get(url_estaciones_snapshot, headers=token_jwt_euskalmet_2024.headers)
    # Respuesta OK
    if data.status_code == 200:
        # Formatear respuesta a json
        data = data.json()
        # Recoger valores para introducir en el diccionario despues
        sensores = data['sensors']
        # Recorrer sensores
        for sensor in sensores:
            valor_sensor = GET_sensorkey(sensor['sensorKey'])
            config_2024.array_sensores_por_estacion.append(valor_sensor)
        # Creo un diccionario con los datos que me interesan
        doc = {
                '_id': est,
                'tipo_estacion': data['stationType'],
                'nombre': data['name']['SPANISH'],
                'municipio': data['municipality']['SPANISH'],
                'provincia': data['province']['SPANISH'],
                'snapshot': snap,
                'sensores': list(config_2024.array_sensores_por_estacion)
        }
        # Añade el diccionario a un array
        config_2024.array_dic_estaciones.append(doc)
    else:
        config_2024.cont_NO_200_meteo_estaciones_snapshot += 1