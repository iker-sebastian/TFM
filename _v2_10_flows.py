# Imports
import config
import _v2_11_met_flows
import bdd
import asyncio

# Setup de fecha inicial y final
config.Year_Month_Setting(config.fecha_inicial, config.fecha_hoy)

async def main():
    # Numero de paginas de meter_Id
    config.num_pag_meter = await _v2_11_met_flows.API_meterId_pags_async()

    # Bucle para recorrer todos los meter_Id
    tasks = []
    for i in range(1, config.num_pag_meter + 1):
        tasks.append(_v2_11_met_flows.API_meterId_async(i))
    await asyncio.gather(*tasks)
    
    # Comprobación valores únicos
    config.array_meterId_unicos = list(set(config.array_meterId))

    # Recorrer todos los años y meses
    for year_month in config.array_year_month:
        for meterId in config.array_meterId_unicos:
            print(meterId)
            config.num_pag_flows = await _v2_11_met_flows.API_flows_pags_async(meterId, year_month)
            
            # Verificar y asignar valor por defecto si config.num_pag_flows es None
            num_pag_flows = config.num_pag_flows if config.num_pag_flows is not None else 0
            
            tasks = []
            for i in range(1, int(num_pag_flows) + 1):
                tasks.append(_v2_11_met_flows.API_flows_async(meterId, year_month, i))
                if len(tasks) >= 10:  # Controlar la cantidad de tareas en paralelo
                    await asyncio.gather(*tasks)
                    tasks = []
            
            await asyncio.gather(*tasks)

    # Unificar diccionarios por meterId y fecha
    _v2_11_met_flows.unificar_Flows()

    # Inserción flows
    for doc in config.array_dic_flows_unificados:
        # Actualiza el documento si existe '_id', si no inserta datos
        bdd.coleccion_flows.update_one({'_id': doc['_id']}, {'$set': doc}, upsert=True)

if __name__ == '__main__':
    asyncio.run(main())
