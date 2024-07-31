# Imports
import config
import _11_met_flows
import bdd

def main():
    # Setup de fecha inicial y final
    config.Year_Month_Setting(config.fecha_inicial, config.fecha_hoy)

    # Numero de paginas de meter_Id
    config.num_pag_meter = _11_met_flows.API_meterId_pags()

    # Para obtener datos de meterId
    for pagina in range(int(config.num_pag_meter)):
        _11_met_flows.API_meterId(pagina)

    # Comprobacion valores unicos
    config.array_meterId_unicos = list(set(config.array_meterId))

    # Recorrer todos los años y meses
    for year_month in config.array_year_month:
        # Recorrer todos los meterId
        for meterId in config.array_meterId_unicos:
            print(meterId)
            # Llamada API y guardar datos en array
            config.num_pag_flows = _11_met_flows.API_flows_pags(meterId, year_month)
            
            # Verificar si config.num_pag_flows es None
            if config.num_pag_flows is not None:
                num_pag_flows = config.num_pag_flows
            else:
                num_pag_flows = 0
            
            # Para obtener datos de flows
            for pagina in range(int(num_pag_flows)):
                _11_met_flows.API_flows(meterId, year_month, pagina)
            
        # Unificar diccionarios por meterId y fecha
        _11_met_flows.unificar_Flows()

        # Insercion flows
        for doc in config.array_dic_flows_unificados:
            # Actualiza el documento si existe '_id', si no inserta datos
            bdd.coleccion_flows.update_one({'_id': doc['_id']}, {'$set': doc}, upsert=True)
