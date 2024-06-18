# Imports
import config
import _11_met_flows
import bdd

# Setup de fecha inicial y final
config.Year_Month_Setting(config.fecha_inicial, config.fecha_hoy)

# Numero de paginas de meter_Id
config.num_pag_meter = _11_met_flows.API_meterId_pags()

# Bucle para recorrer todos los meter_Id
while config.contador_pags < config.num_pag_meter:
    # Llamada a la API meter_Id
    _11_met_flows.API_meterId()
    # Aumenta contador paginas
    config.contador_pags += 1
# Comprobación valores unicos
config.array_meterId_unicos =  list(set(config.array_meterId))
# Reset contador paginas
config.contador_pags = 1

# Recorrer todos los años y meses
for year_month in config.array_year_month:
    # Recorrer todos los meter_Id ene sa fecha
    for meterId in config.array_meterId_unicos:
        print(meterId)
        # Paginas de ese meterId en ese año
        config.num_pag_flows = _11_met_flows.API_flows_pags(meterId, year_month)
        # Bucle para recorrer todos los meter_Id
        while config.contador_pags < int(config.num_pag_flows):
            # Llamada a API FLOWS
            _11_met_flows.API_flows(meterId, year_month)
            # Aumenta contador paginas
            config.contador_pags += 1
            if config.temporal > 10:
                break
        # Reset contador paginas
        config.contador_pags = 1
        if config.temporal > 10:
            break
    if config.temporal > 10:
        break
        
# Unificar diccionarios por meterId y fecha
_11_met_flows.unificar_Flows()

# Insercion flows
for doc in config.array_dic_flows_unificados:
    # Actualiza el documento si existe '_id', si no inserta datos
    bdd.coleccion_flows.update_one({'_id': doc['_id']}, {'$set': doc}, upsert=True)