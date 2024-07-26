# Imports
import config
import _11_met_flows
import bdd
import asyncio

# Setup de fecha inicial y final
config.Year_Month_Setting(config.fecha_inicial, config.fecha_hoy)

async def main():
    # Numero de paginas de meter_Id
    config.num_pag_meter = await _11_met_flows.API_meterId_pags()

    # Bucle para ir realizando las diferentes tareas, la cola de espera incluida
    tasks = []
    for i in range(1, config.num_pag_meter + 1):
        tasks.append(_11_met_flows.API_meterId(i))
    await asyncio.gather(*tasks)
    
    # Comprobación valores únicos
    config.array_meterId_unicos = list(set(config.array_meterId))

    # Recorrer todos los años y meses
    for year_month in config.array_year_month:
        # Recorrer todos los meterId
        for meterId in config.array_meterId_unicos:
            print(meterId)
            # Llamada API y guardar datos en array
            config.num_pag_flows = await _11_met_flows.API_flows_pags(meterId, year_month)
            
            # Verificar si config.num_pag_flows es None
            if config.num_pag_flows is not None:
                num_pag_flows = config.num_pag_flows
            else:
                num_pag_flows = 0
            
            # Para controlar las tareas en paralelo
            tasks = []
            for i in range(1, int(num_pag_flows) + 1):
                tasks.append(_11_met_flows.API_flows(meterId, year_month, i))
                # Crea una cola de espera
                if len(tasks) >= 10:
                    await asyncio.gather(*tasks)
                    tasks = []
            
            await asyncio.gather(*tasks)

    # Unificar diccionarios por meterId y fecha
    _11_met_flows.unificar_Flows()

    # Inserción flows
    for doc in config.array_dic_flows_unificados:
        # Actualiza el documento si existe '_id', si no inserta datos
        bdd.coleccion_flows.update_one({'_id': doc['_id']}, {'$set': doc}, upsert=True)

# Inicializarlo
if __name__ == '__main__':
    asyncio.run(main())
