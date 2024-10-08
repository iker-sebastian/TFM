#Imports
import requests
import config
import time

# Datos de calidad del aire
def API_calidad_aire(prov, inicio, fin):
    # API calidad del aire
    url_cal_aire = f'https://api.euskadi.eus/air-quality/measurements/daily/counties/{prov}/from/{inicio}/to/{fin}'
    # En caso de fallo un par de intentos adicionales
    for intento in range(config.intentos):
        # Excepcion en caso de perdida de conexion
        try:
            # Solcitud
            response = requests.get(url_cal_aire)
            # Respuesta OK
            if response.status_code == 200:
                # Formatear respuesta a json
                data = response.json()
                # Recorrer elemento end data
                for elemento in data:
                    # Recoger el campo 'station'
                    data_stations = elemento['station']
                    for estacion in data_stations:
                        # Recoger el campo 'measurements'
                        data_measurements = estacion['measurements']
                        for measure in data_measurements:
                            doc = {
                                '_id': elemento['date'] + estacion['id'],
                                'fecha': elemento['date'],
                                'id_estacion': estacion['id'],
                                'nombre': estacion['name'],
                                'provincia': prov,
                                measure['name']: measure['value'],
                                'unidad_medicion': measure['unit']
                            }
                        # Añade el diccionario a un array
                        config.array_dic_meteo_cal_aire.append(doc)
            else:
                print('Error en la solicitud de la API')

        # Excepcion de conexion
        except requests.exceptions.ConnectionError:
            print(f'Error de comunicacion! Estos son los datos: [provincia: {prov} y fechas de inicio y fin: {inicio} {fin}')
            if intento < config.intentos -1:
                print(f'Reintentando... Intento {intento + 1}')
                time.sleep(5)
            else:
                print('El numero maximo de intentos ha sido alcanzado')
                break

        # Excepcion de tiempo de espera
        except requests.exceptions.ReadTimeout:
            print(f'Tiempo de espera agotado. Intento {intento + 1}. Se reintentara...')
            if intento < config.intentos -1:
                time.sleep(5)
            else:
                print('El tiempo de espera se agoto definitivamente')
                break
