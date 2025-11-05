import os

def get_w1_sensor_path():
    """Busca y retorna la ruta del sensor DS18B20 (empieza con '28-')."""
    try:
        # Busca en el directorio de dispositivos 1-Wire
        base_dir = '/sys/bus/w1/devices/'
        device_folder = [name for name in os.listdir(base_dir) if name.startswith('28-')][0]
        return os.path.join(base_dir, device_folder, 'w1_slave')
    except (FileNotFoundError, IndexError):
        # Retorna una ruta de prueba si no encuentra el sensor
        print("ADVERTENCIA: No se encontró el sensor DS18B20. Usando ruta simulada.")
        return "/sys/bus/w1/devices/simulated_device/w1_slave"

W1_SENSOR_PATH = get_w1_sensor_path()