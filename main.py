# Imports
import concurrent.futures
import _10_flows
import _20_calidad_aire
import _30_est_meteorologicas
import os

def run_10_flows():
    _10_flows.main()

def run_20_calidad_aire():
    _20_calidad_aire.main()

def run_30_meteorologia():
    _30_est_meteorologicas.main()

def main():
    num_workers = os.cpu_count()

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [
            executor.submit(run_10_flows),
            #executor.submit(run_20_calidad_aire),
            #executor.submit(run_30_meteorologia)
        ]
        
        # Espera a que todas las funciones terminen
        for tarea in concurrent.futures.as_completed(futures):
            try:
                tarea.result()
            except Exception as e:
                print(f'Ocurrio un error: {e}')

if __name__ == '__main__':
    main()