import os
import threading
from bluetooth_service import BluetoothService
from sync_service import SyncService

# Configuración inicial
LOCAL_FOLDER = input("Introduce la ruta de la carpeta local a sincronizar: ")
if not os.path.exists(LOCAL_FOLDER):
    print(f"La ruta {LOCAL_FOLDER} no existe. Creando carpeta...")
    os.makedirs(LOCAL_FOLDER)

REMOTE_DEVICE_NAME = input("Introduce el nombre o dirección del dispositivo remoto Bluetooth: ")

# Inicialización de servicios
bluetooth_service = BluetoothService(REMOTE_DEVICE_NAME)
sync_service = SyncService(LOCAL_FOLDER, bluetooth_service)

def start_services():
    try:
        # Conectar al dispositivo Bluetooth remoto
        bluetooth_service.connect()

        # Iniciar la sincronización de carpetas
        sync_service.start()
    except Exception as e:
        print(f"Error al iniciar los servicios: {e}")

def stop_services():
    # Detener sincronización y conexión Bluetooth
    sync_service.stop()
    bluetooth_service.disconnect()

# Control principal
try:
    print("Iniciando sincronización...")
    service_thread = threading.Thread(target=start_services)
    service_thread.start()
    
    input("Presiona Enter para detener el servicio...\n")
    stop_services()
except KeyboardInterrupt:
    print("\nInterrupción detectada. Deteniendo servicios...")
    stop_services()
    
    
    






