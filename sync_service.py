import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class SyncEventHandler(FileSystemEventHandler):
    def init(self, folder, bluetooth_service):
        self.folder = folder
        self.bluetooth_service = bluetooth_service

    def on_modified(self, event):
        if not event.is_directory:
            print(f"Archivo modificado: {event.src_path}")
            self.bluetooth_service.send_file(event.src_path)

    def on_created(self, event):
        if not event.is_directory:
            print(f"Archivo creado: {event.src_path}")
            self.bluetooth_service.send_file(event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            print(f"Archivo eliminado: {event.src_path}")
            # Opcional: Implementar lógica para informar al dispositivo remoto

class SyncService:
    def init(self, folder, bluetooth_service):
        self.folder = folder
        self.bluetooth_service = bluetooth_service
        self.observer = Observer()

    def start(self):
        """Inicia el monitoreo de la carpeta y sincronización."""
        event_handler = SyncEventHandler(self.folder, self.bluetooth_service)
        self.observer.schedule(event_handler, self.folder, recursive=True)
        self.observer.start()
        print(f"Monitoreando la carpeta: {self.folder}")

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        """Detiene el monitoreo de la carpeta."""
        self.observer.stop()
        self.observer.join()
        print("Sincronización detenida.")