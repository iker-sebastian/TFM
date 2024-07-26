# Imports
import config
import subprocess
import multiprocessing

# Metodo para ejcutar scripts
def ejecutar(archivo_python):
    subprocess.run(['python', archivo_python])

# Definir script
if __name__ == '__main__':
    # Lista de scripts
    scripts = ['_v2_10_flows.py', '_20_calidad_aire.py', '_v2_30_est_meteorologicas.py']

    # Creamos un proceso para cada archivo
    procesos = []

    # Definir procesos
    for script in scripts:
        proceso = multiprocessing.Process(target=ejecutar, args=(script,))
        procesos.append(proceso)
        # Arrancar proceso
        proceso.start()

    # Esperamos a que todos los procesos terminen
    for proceso in procesos:
        proceso.join()