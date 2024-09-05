# Imports
import requests
import config

# Metodo que llama a la API que devuelve todas las incidencias
def API_incidencias(year, month, day):
    # API de incidencias
    url_incidencias = f'https://api.euskadi.eus/traffic//v1.0/incidences/byDate/{year}/{month}/{day}'
    # Solicitud
    response = requests.get(url_incidencias)
    # Respuesta OK
    if response.status_code == 200:
        # Formatear respuesta a json
        data = response.json()
        # Recoger el campo 'incidences'
        data_incidencias = data['incidences']
        for documento in data_incidencias:
            cityTown = documento.get('cityTown', 'road')
            causa = documento.get('cause', 'Unknown cause')
            carretera = documento.get('road', 'Unknown road')
            # Crear un diccionario con los datos que interesan
            doc = {
                '_id': documento['incidenceId'],
                'sourceId': documento['sourceId'],
                'incidenceType': documento['incidenceType'],
                'province': documento['province'],
                'cause': causa,
                'cityTown': cityTown,
                'startDate': documento['startDate'],
                'road': carretera
            }
            # Añadir el diccionario a un array
            config.array_dic_incidencias.append(doc)
            #print(f'inc_{config.id_inc}')
            config.id_inc += 1
    else:
        print('Error en la solicitud de la API de incidencias')
