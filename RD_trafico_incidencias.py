# Imports
import requests
import config

# Metodo que llama a la API que devuelve todas las incidencias
def API_incidencias(year, month, day):
    # API de incidencias
    url_incidencias = f'https://api.euskadi.eus/traffic//v1.0/incidences/byDate/{year}/{month}/{day}'
    # Solcitud
    data = requests.get(url_incidencias)
    # Respuesta OK
    if data.status_code == 200:
        # Formatear respuesta a json
        data = data.json()
        # Recoger el campo 'incidences'
        data_incidencias = data['incidences']
        for documento in data_incidencias:
            cityTown = documento.get('cityTown', 'road')
            causa = documento.get('cause', 'Unkown cause')
            # Creo un diccionario con los datos que me interesan
            doc = {
                '_id': documento['incidenceId'],
                'sourceId': documento['sourceId'],
                'incidenceType': documento['incidenceType'],
                'province': documento['province'],
                'cause': causa,
                'cityTown': cityTown,
                'startDate': documento['startDate'],
                'road': documento['road']
            }
            # Añade el diccionario a un array
            config.array_dic_incidencias.append(doc)
    else:
        config.cont_NO_200_trafico_incidencias += 1