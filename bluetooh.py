import subprocess
import os
import hashlib
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

RUTA_LOCAL = "E:\\Universidad\\3er Año\\Redes\\Proyecto\\a\\a"  # Reemplazar con la ruta local
DISPOSITIVO_REMOTO = "C4:D0:E3:8B:0D:75"  # Reemplazar con la dirección MAC del dispositivo remoto

def ejecutar_comando(comando):
    try:
        print(f"Ejecutando comando: {comando}")  # Print the command for debugging
        resultado = subprocess.run(comando, capture_output=True, text=True, check=True)
        return resultado.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar comando: {e}")
        return None
    except FileNotFoundError as e:
        print(f"Archivo no encontrado: {e}")
        return None

def generar_hash(ruta_archivo):
    hasher = hashlib.sha256()
    with open(ruta_archivo, 'rb') as archivo:
        buf = archivo.read()
        hasher.update(buf)
    return hasher.hexdigest()

def obtener_lista_archivos_remotos():
    comando_listar = ["obexftp", "-b", DISPOSITIVO_REMOTO, "-l"]
    salida = ejecutar_comando(comando_listar)
    if salida:
        archivos = salida.split('\n')
        return [archivo.strip() for archivo in archivos if archivo.strip()]
    return []

def obtener_hash_remoto(nombre_archivo):
    comando_hash = ["obexftp", "-b", DISPOSITIVO_REMOTO, "--chdir", nombre_archivo, "--md5"]
    salida = ejecutar_comando(comando_hash)
    if salida:
        return salida.split()[0]  # Assuming the hash is the first part of the output
    return None

def sincronizar():
    print("Iniciando sincronización...")

    archivos_remotos = obtener_lista_archivos_remotos()
    print(f"Archivos remotos: {archivos_remotos}")

    for nombre_archivo in os.listdir(RUTA_LOCAL):
        ruta_completa = os.path.join(RUTA_LOCAL, nombre_archivo)
        print(ruta_completa)
        if os.path.isfile(ruta_completa):
            hash_local = generar_hash(ruta_completa)
            hash_remoto = obtener_hash_remoto(nombre_archivo)

            if hash_remoto is None or hash_local != hash_remoto:
                print(f"Transfiriendo archivo {nombre_archivo}...")
                comando_enviar = ["obexftp", "-b", DISPOSITIVO_REMOTO, "-p", ruta_completa]  # Ejemplo con obexftp
                ejecutar_comando(comando_enviar)
                print(f"Archivo {nombre_archivo} sincronizado.")
            else:
                print(f"Archivo {nombre_archivo} ya está sincronizado.")
    print("Sincronización completada.")

class ManejadorCambios(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            print(f"Archivo modificado: {event.src_path}")
            sincronizar()

if __name__ == "__main__":
    print("Iniciando sincronización...")
    #Monitoreo de cambios
    event_handler = ManejadorCambios()
    observer = Observer()
    observer.schedule(event_handler, RUTA_LOCAL, recursive=True)
    observer.start()

    #Sincronizacion inicial
    sincronizar()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()