# Imports
import requests
import config
import time
import asyncio
import aiohttp
from collections import defaultdict

# Paginas meter_Id
async def API_meterId_pags_async():
    url_meterId_pags = 'https://api.euskadi.eus/traffic/v1.0/meters'
    async with aiohttp.ClientSession() as session:
        async with session.get(url_meterId_pags) as response:
            if response.status == 200:
                data = await response.json()
                data_totalPages = data['totalPages']
                return data_totalPages

# Valores meter_Id    
async def API_meterId_async(page):
    url_meterId = f'https://api.euskadi.eus/traffic/v1.0/meters?_page={page}'
    async with aiohttp.ClientSession() as session:
        for intento in range(config.intentos):
            try:
                async with session.get(url_meterId) as response:
                    if response.status == 200:
                        data = await response.json()
                        data_features = data['features']
                        for feature in data_features:
                            meterId = feature['properties']['meterId']
                            config.array_meterId.append(int(meterId))
                        break
            except (aiohttp.ClientConnectionError, aiohttp.ClientResponseError):
                if intento < config.intentos - 1:
                    await asyncio.sleep(5)
                else:
                    print('El número máximo de intentos ha sido alcanzado')

# Datos de flows de un mes con un meterId
async def API_flows_pags_async(meterId, year_month):
    url_flows_pags = f'https://api.euskadi.eus/traffic/v1.0/flows/byYear/{year_month[0]}/byMeter/{meterId}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url_flows_pags) as response:
            if response.status == 200:
                data = await response.json()
                data_totalPages = data['totalPages']
                return data_totalPages

# Datos de flows de un mes con un meterId
async def API_flows_async(meterId, year_month, page):
    url_flows = f'https://api.euskadi.eus/traffic/v1.0/flows/byYear/{year_month[0]}/byMeter/{meterId}1?_page={page}'
    async with aiohttp.ClientSession() as session:
        for intento in range(config.intentos):
            try:
                async with session.get(url_flows, timeout=30) as response:
                    if response.status == 200:
                        data = await response.json()
                        data_flows = data['flows']
                        for documento in data_flows:
                            velocidad_media = documento.get('speedAvg', 0)
                            doc = {
                                '_id': documento['meterId'] + '_' + documento['meterDate'] + '_' + documento['timeRank'],
                                'meterId': meterId,
                                'source': documento['sourceId'],
                                'fecha': documento['meterDate'],
                                'año': year_month[0],
                                'mes': year_month[1],
                                'vel_media': velocidad_media,
                                'vehiculos': documento['totalVehicles']
                            }
                            config.array_dic_flows.append(doc)
                        break
            except (aiohttp.ClientConnectionError, aiohttp.ClientResponseError, asyncio.TimeoutError):
                if intento < config.intentos - 1:
                    await asyncio.sleep(5)
                else:
                    print('El número máximo de intentos ha sido alcanzado')

# Obtener un único registro por día
def unificar_Flows():
    diccionarios_agrupados = defaultdict(list)
    for dic in config.array_dic_flows:
        filtro = (dic['meterId'], dic['fecha'])
        diccionarios_agrupados[filtro].append(dic)

    for filtro, lista_dic in diccionarios_agrupados.items():
        meterId, fecha = filtro
        suma_vehiculos = sum(int(dic['vehiculos']) for dic in lista_dic)
        suma_vel_media = sum(int(dic['vel_media']) for dic in lista_dic)
        media_vel_media = suma_vel_media / len(lista_dic)
        source = lista_dic[0]['source']
        año = lista_dic[0]['año']
        mes = lista_dic[0]['mes']
        dic_unificado = {
            '_id': str(meterId) + '_' + fecha,
            'meterId': meterId,
            'source': source,
            'fecha': fecha,
            'año': año,
            'mes': mes,
            'vel_media': media_vel_media,
            'vehiculos': suma_vehiculos
        }
        config.array_dic_flows_unificados.append(dic_unificado)
