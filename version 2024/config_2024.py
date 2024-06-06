# Imports
import datetime

# Setting de fechas
fecha_hoy =  datetime.date(2024, 5, 1) #datetime.date.today()
fecha_inicial = datetime.date(2024, 1, 1)
fecha_recorrida = fecha_inicial
fecha_completa = ''
#dia_semana = [1, 2, 3, 4, 5, 6, 7]

def Fecha_Setting(fecha_recorrida):
    # Definir variables 'year', 'month' y 'day'
    year = fecha_recorrida.year
    month = str(fecha_recorrida.month).zfill(2)
    day = str(fecha_recorrida.day).zfill(2)
    # Definir variable fecha completa
    fecha_completa = str(year) + month + day
    return year, month, day, fecha_completa

def Year_Month_Setting(inicio, fin):
    while inicio <= fin:
        # Añadir a array año y mes
        array_year_month.append([inicio.year, inicio.month])
        # Mes siguiente
        inicio += datetime.timedelta(days=32)
    return array_year_month

# Arrays
array_year_month = [] # Array que guarda arrays de los años y meses
array_meterId = [] # Array donde se almacenan los valores meterId obtenidos de la API meterID
array_meterId_unicos = [] # array_meterId pero de valores unicos
diccionario_unificar_flows = dict() # Diccionario para unificar los flows por MeterId y dia
array_provincia = [1, 48, 20] # Setting de provincia (codigo)
array_estaciones = [] # Array que guarda las estaciones de euskalmet
array_estaciones_unicos = [] # array_estaciones pero de valores unicos (snapshot mas reciente)
diccionario_estaciones = dict() # Diccionario intermedio que guarda las estaciones de euskalmet
array_sensores_por_estacion = [] # Array que guarda los sensores de cada estacion
array_mediciones = [['measuresForAir','humidity'], ['measuresForAir','temperature'], ['measuresForAtmosphere','superficial_wetting'], ['measuresForAtmosphere','visibility'], ['measuresForWater','precipitation'], ['measuresForWind','mean_speed'], ['measuresForWind','direction_sigma']]

# Arrays con diccionarios
array_dic_flows = [] # Array donde se almacenan los diccionarios que contienen datos de flows
array_dic_flows_unificados = [] # Array donde se almacenan los diccionarios que contienen datos de flows (uno por dia y meterId)
array_dic_incidencias = [] # Array donde se almacenan los diccionarios que contienen datos de incidencias
array_dic_meteo_cal_aire = [] # Array donde se almacenan los diccionarios que contienen datos de la calidad del aire
array_dic_estaciones = [] # Array donde se almacenan los diccionarios que contienen datos de las estaciones de euskalmet
array_dic_datos_meteo = [] # Array donde se almacenan los diccionarios que contienen datos de euskalmet

# Iteradores
num_pag_meter = 1
intentos = 3
# Contadores de fallos
cont_NO_200_meteo_datos = 0
cont_NO_200_trafico_incidencias = 0
cont_NO_200_meteo_calidad_aire = 0
cont_NO_200_meteo_estaciones_snapshot = 0
cont_NO_200_meteo_estaciones = 0
cont_NO_200_trafico_meterId = 0
cont_NO_200_trafico_flows = 0




