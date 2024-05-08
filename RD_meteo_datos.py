# Imports
import requests
import config
import token_jwt_euskalmet

def API_datos(estacion, sensor, tipo_medida, medida, year, month, day):
    # API de Euskalmet para obtener datos
    url_datos = f'https://api.euskadi.eus/euskalmet/readings/summarized/byDay/forStation/{estacion}/{sensor}/measures/{tipo_medida}/{medida}/at/{year}/{month}/{day}'
    # Excepción en caso de perdida de conexión
    try:
        # Solcitud
        data = requests.get(url_datos, headers=token_jwt_euskalmet.headers)
        # Respuesta OK
        if data.status_code == 200:
            # Formatear respuesta a json
            data = data.json()    
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
                    'max_acumulado': data['maxAccumulated']['accumulated'],
                    'min': data['min']['value'],
                    'media': data['total'],
                    'total': data['mean']
            }
            # Añade el diccionario a un array
            config.array_dic_datos_meteo.append(doc)
            print(doc)
        else:
            config.cont_NO_200_meteo_datos += 1
    # Segunda parte de la excepción
    except requests.exceptions.ConnectionError:
        print(f"Error de comunicación! Estos son los datos: [estacion: {estacion}, sensor: {sensor}, tipo de medida: {tipo_medida}, medida: {medida}, year: {year}, month: {month} y day: {day}]")