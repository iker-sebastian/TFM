#Imports
import requests
import config

# Metodo que llama a la API de calidad del aire
def API_calidad_aire(prov, inicio, fin):
    # API calidad del aire
    url_cal_aire = f'https://api.euskadi.eus/air-quality/measurements/daily/counties/{prov}/from/{inicio}/to/{fin}'
    # Solcitud
    data = requests.get(url_cal_aire)
    # Respuesta OK
    if data.status_code == 200:
        # Formatear respuesta a json
        data = data.json()
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
        config.cont_NO_200_meteo_calidad_aire += 1