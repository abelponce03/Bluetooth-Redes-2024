import bluetooth


class BluetoothService:
    def init(self, device_name):
        self.device_name = device_name
        self.socket = None
        self.target_address = None

    def connect(self):
        """Establece conexión con el dispositivo remoto usando Bluetooth."""
        print(f"Buscando el dispositivo {self.device_name}...")
        nearby_devices = bluetooth.discover_devices(duration=8, lookup_names=True, flush_cache=True)

        for addr, name in nearby_devices:
            if name == self.device_name or addr == self.device_name:
                self.target_address = addr
                break

        if not self.target_address:
            raise Exception(f"No se encontró el dispositivo {self.device_name}")

        print(f"Conectando al dispositivo {self.device_name} en la dirección {self.target_address}...")
        self.socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.socket.connect((self.target_address, 1))
        print("Conexión establecida.")

    def send_file(self, file_path):
        """Envía un archivo al dispositivo remoto."""
        if not self.socket:
            raise Exception("No hay conexión activa.")

        print(f"Enviando archivo: {file_path}...")
        with open(file_path, 'rb') as file:
            data = file.read()
            self.socket.sendall(data)
        print(f"Archivo {file_path} enviado correctamente.")

    def receive_file(self, save_path):
        """Recibe un archivo del dispositivo remoto."""
        if not self.socket:
            raise Exception("No hay conexión activa.")

        print("Recibiendo archivo...")
        data = self.socket.recv(1024)
        with open(save_path, 'wb') as file:
            file.write(data)
        print(f"Archivo recibido y guardado en {save_path}.")

    def disconnect(self):
        """Cierra la conexión Bluetooth."""
        if self.socket:
            self.socket.close()
            print("Conexión Bluetooth cerrada.")
            