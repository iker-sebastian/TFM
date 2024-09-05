# Imports
import requests
import config
import token_jwt_euskalmet

def API_datos(estacion, sensor, tipo_medida, medida, year, month, day):
    # API de Euskalmet para obtener datos
    url_datos = f'https://api.euskadi.eus/euskalmet/readings/summarized/byDay/forStation/{estacion}/{sensor}/measures/{tipo_medida}/{medida}/at/{year}/{month}/{day}'
    # Excepcion en caso de perdida de conexion
    try:
        # Solicitud
        response = requests.get(url_datos, headers=token_jwt_euskalmet.headers)
        # Respuesta OK
        if response.status_code == 200:
            # Formatear respuesta a json
            data = response.json()
            # Excepcion por si no existe maxAccumulated
            try:
                maximo_acumulado = data['maxAccumulated']['accumulated']
            except KeyError:
                maximo_acumulado = data['max']['value']
            # Crear un diccionario con los datos que interesan
            doc = {
                    '_id': medida + '_' + str(year) + str(month) + str(day) + '_' + estacion + '_' + sensor,
                    'año': year,
                    'mes': int(month),
                    'dia': int(day),
                    'estacion': estacion,
                    'sensor': sensor,
                    'tipo_medida': tipo_medida,
                    'medida': medida,
                    'max': data['max']['value'],
                    'max_acumulado': maximo_acumulado,
                    'min': data['min']['value'],
                    'media': data['mean'],
                    'total': data['total']
            }
            # Añadir el diccionario a un array
            config.array_dic_datos_meteo.append(doc)
            #print(f'met_{config.id_met}')
            config.id_met += 1
        #else:
            # Se comenta el print por tema de tiempos de ejecucion
            #print('Error en la solicitud de la API de meteorologia')
    # Segunda parte de la excepcion
    except requests.exceptions.ConnectionError:
        print(f'Error de comunicacion! Estos son los datos: [estacion: {estacion}, sensor: {sensor}, tipo de medida: {tipo_medida}, medida: {medida}, year: {year}, month: {month} y day: {day}]')