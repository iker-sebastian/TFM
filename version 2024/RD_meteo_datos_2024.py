# Imports
import requests
import config_2024
import token_jwt_euskalmet_2024

def API_datos(estacion, sensor, tipo_medida, medida, year, month, day):
    # API de Euskalmet para obtener datos
    url_datos = f'https://api.euskadi.eus/euskalmet/readings/summarized/byDay/forStation/{estacion}/{sensor}/measures/{tipo_medida}/{medida}/at/{year}/{month}/{day}'
    # Excepción en caso de perdida de conexión
    try:
        # Solcitud
        data = requests.get(url_datos, headers=token_jwt_euskalmet_2024.headers)
        # Respuesta OK
        if data.status_code == 200:
            # Formatear respuesta a json
            data = data.json()
            # Excepcion por si no existe maxAccumulated
            try:
                maximo_acumulado = data['maxAccumulated']['accumulated']
            except KeyError:
                maximo_acumulado = data['max']['value']
            # Creo un diccionario con los datos que me interesan
            doc = {
                    '_id': str(year) + str(month) + str(day) + '_' + medida + '_' + estacion + '_' + sensor,
                    'anyo': year,
                    'mes': month,
                    'dia': day,
                    'estacion': estacion,
                    'sensor': sensor,
                    'tipo_medida': tipo_medida,
                    'medida': medida,
                    'max': data['max']['value'],
                    'max_acumulado': maximo_acumulado,
                    'min': data['min']['value'],
                    'media': data['total'],
                    'total': data['mean']
            }
            # Añade el diccionario a un array
            config_2024.array_dic_datos_meteo.append(doc)
            print(doc)
        else:
            config_2024.cont_NO_200_meteo_datos += 1
    # Segunda parte de la excepción
    except requests.exceptions.ConnectionError:
        print(f"Error de comunicación! Estos son los datos: [estacion: {estacion}, sensor: {sensor}, tipo de medida: {tipo_medida}, medida: {medida}, year: {year}, month: {month} y day: {day}]")