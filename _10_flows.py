# Imports
import config
import _11_met_flows
import bdd

# Setup de fecha inicial y final
config.Year_Month_Setting(config.fecha_inicial, config.fecha_hoy)

# Numero de paginas de meter_Id
pags_totales = _11_met_flows.API_meterId_pags()

# Bucle para recorrer todos los meter_Id
while config.num_pag_meter < pags_totales:
    # Llamada a la API meter_Id
    _11_met_flows.API_meterId()
    config.num_pag_meter += 1
# Comprobación valores unicos
config.array_meterId_unicos =  list(set(config.array_meterId))

# Recorrer array de todos los meter_Id
for meterId in config.array_meterId_unicos:
    # Check de la ejecucción
    print(meterId)
    # Recorrer todos los años y meses de ese meter_Id
    for year_month in config.array_year_month:
        # Llamada a la API FLOWS
        _11_met_flows.API_flows(meterId, year_month)

# Unificar flows por meter_Id y dia
_11_met_flows.unificar_Flows()

# Insercion flows
for doc in config.array_dic_flows_unificados:
    print(doc)
    # Actualiza el documento si existe '_id', si no inserta datos
    bdd.coleccion_flows.update_one({'_id': doc['_id']}, {'$set': doc}, upsert=True)