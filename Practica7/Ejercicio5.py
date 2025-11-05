import threading
from RPLCD.i2c import CharLCD
from time import sleep

# Define el frame buffer global (contenido de las dos líneas)
framebuffer = [
    "TORRES MENDOZA",  # Línea 0: Marquesina (Apellidos)
    "Temp. --.-- C"      # Línea 1: Temperatura
]

buffer_lock = threading.Lock() 
lcd = CharLCD('PCF8574', 0X27)
NUM_COLS = 16

# --- Función para actualizar el buffer de temperatura ---
def getTempRoom():
    global framebuffer
    while True:
        try:
            
           
            path_temp = "/sys/bus/w1/devices/28-19411e356461/w1_slave" 
           
            with open(path_temp, "r") as f:
                lines = f.readlines()
            
            if lines[0].strip().endswith("YES"):
                temp_mC = int(lines[1].split("t=")[1])
                temp = temp_mC / 1000.0
                
                temp_string = "Temp. {t:.2f} C".format(t=temp)
                
               
                with buffer_lock:
                    framebuffer[1] = temp_string.ljust(NUM_COLS) 
            
            sleep(1) 
        except Exception as e:
            # Manejo de errores
            with buffer_lock:
                framebuffer[1] = "ERROR TEMP".ljust(NUM_COLS)
            sleep(5)
            
# --- Función para generar la marquesina y actualizar el buffer ---
def name_marquee():
    global framebuffer
    # Apellido/s del equipo para el corrimiento
    full_text = "            TORRES MENDOZA            " 
  
    
    text_len = len(full_text)
    
    while True:
        for i in range(text_len):
            # Calcula la porción de 16 caracteres a mostrar
            # Usa el operador módulo (%) para el 'corrimiento infinito'
            start_index = i % text_len
            
            # Obtiene el segmento de texto, manejando el 'wrap' alrededor del final
            if start_index + NUM_COLS <= text_len:
                scrolling_text = full_text[start_index : start_index + NUM_COLS]
            else:
                # Si se desborda, toma el resto y luego el inicio de la cadena
                segment1 = full_text[start_index:]
                segment2 = full_text[:NUM_COLS - len(segment1)]
                scrolling_text = segment1 + segment2
                
            # Usa el Lock al modificar el recurso compartido
            with buffer_lock:
                framebuffer[0] = scrolling_text
            
            # Controla la velocidad de corrimiento. 
            # 0.3 segundos es un buen valor. El ejercicio 5 no especifica la velocidad.
            sleep(0.3) 

# --- Función UNIFICADA de ESCRITURA al LCD ---
def lcd_writer():
    global framebuffer
    while True:
        # Usa el Lock para leer el recurso compartido
        with buffer_lock:
            line0 = framebuffer[0]
            line1 = framebuffer[1]
            
        # Escribe al LCD
        lcd.home() 
        lcd.write_string(line0) # Escribe la línea 0
        lcd.crlf() # Mueve el cursor a la siguiente línea
        lcd.write_string(line1) # Escribe la línea 1
        
        sleep(0.1) # Una pequeña pausa para evitar sobrecargar el bus I2C

def main():
    # Inicializa el display antes de empezar los hilos
    # No es necesario usar tu algoritmo si usas RPLCD con el adaptador I2C
    lcd.clear() 

    # Hilo 1: Lee la temperatura y actualiza el buffer de la LÍNEA 1
    hilo1 = threading.Thread(target=getTempRoom)
    
    # Hilo 2: Genera el corrimiento de la marquesina y actualiza el buffer de la LÍNEA 0
    hilo2 = threading.Thread(target=name_marquee)
    
    # Hilo 3: Lee el buffer y escribe el contenido al LCD
    hilo3 = threading.Thread(target=lcd_writer)
    
    hilo1.start()
    hilo2.start()
    hilo3.start()
if __name__ == '__main__':
    main()
