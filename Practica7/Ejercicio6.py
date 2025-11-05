import threading
from flask import Flask, render_template_string, request
from RPLCD.i2c import CharLCD
from time import sleep

# --- CONFIGURACIÓN LCD ---
lcd = CharLCD('PCF8574', 0x27)
NUM_COLS = 16

# --- FRAME BUFFER COMPARTIDO ---
framebuffer = ["", ""]
buffer_lock = threading.Lock()

# --- VARIABLES DE CONTROL (GLOBALES) ---
scroll_speed = 0.3          # Velocidad de la marquesina
scroll_direction = "left"   # Dirección: "left" o "right"
temp_mode = "C"             # "C", "F" o "BOTH"

# --- FLASK APP PARA CONTROL WEB ---
app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
  <title>Control LCD</title>
  <style>
    body { font-family: Arial; background: #f3f3f3; text-align: center; padding-top: 40px; }
    h1 { color: #333; }
    form { margin: 20px; }
    input, select { padding: 8px; font-size: 16px; }
    button { padding: 10px 20px; font-size: 16px; background: #4CAF50; color: white; border: none; border-radius: 5px; }
    button:hover { background: #45a049; }
  </style>
</head>
<body>
  <h1>Control del LCD</h1>
  <form method="POST" action="/">
    <label>Velocidad (segundos):</label>
    <input type="number" step="0.1" name="speed" value="{{speed}}"><br><br>

    <label>Dirección:</label>
    <select name="direction">
      <option value="left" {% if direction == 'left' %}selected{% endif %}>Izquierda</option>
      <option value="right" {% if direction == 'right' %}selected{% endif %}>Derecha</option>
    </select><br><br>

    <label>Modo de temperatura:</label>
    <select name="temp_mode">
      <option value="C" {% if temp_mode == 'C' %}selected{% endif %}>Centígrados</option>
      <option value="F" {% if temp_mode == 'F' %}selected{% endif %}>Fahrenheit</option>
      <option value="BOTH" {% if temp_mode == 'BOTH' %}selected{% endif %}>Ambos</option>
    </select><br><br>

    <button type="submit">Actualizar configuración</button>
  </form>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    global scroll_speed, scroll_direction, temp_mode
    if request.method == "POST":
        try:
            scroll_speed = float(request.form["speed"])
            scroll_direction = request.form["direction"]
            temp_mode = request.form["temp_mode"]
        except:
            pass
    return render_template_string(HTML_TEMPLATE, speed=scroll_speed, direction=scroll_direction, temp_mode=temp_mode)

# --- FUNCIÓN: LECTURA DE TEMPERATURA ---
def getTempRoom():
    global framebuffer, temp_mode
    path_temp = "/sys/bus/w1/devices/28-19411e356461/w1_slave"

    while True:
        try:
            with open(path_temp, "r") as f:
                lines = f.readlines()

            if lines[0].strip().endswith("YES"):
                temp_mC = int(lines[1].split("t=")[1])
                tempC = temp_mC / 1000.0
                tempF = round((tempC * 1.8) + 32, 2)

                if temp_mode == "C":
                    temp_str = "Temp: {:.2f} C".format(tempC)
                elif temp_mode == "F":
                    temp_str = "Temp: {:.2f} F".format(tempF)
                else:
                    temp_str = "{:.2f}C {:.2f}F".format(tempC, tempF)

                with buffer_lock:
                    framebuffer[1] = temp_str.ljust(NUM_COLS)
        except:
            with buffer_lock:
                framebuffer[1] = "ERROR TEMP".ljust(NUM_COLS)
        sleep(1)

# --- FUNCIÓN: MARQUESINA ---
def name_marquee():
    global framebuffer, scroll_speed, scroll_direction
    text = "     TORRES MENDOZA ANGUIANO     "
    length = len(text)

    while True:
        for i in range(length):
            with buffer_lock:
                if scroll_direction == "left":
                    segment = (text + text)[i:i+NUM_COLS]
                else:  # derecha
                    segment = (text + text)[length - i:length - i + NUM_COLS]
                framebuffer[0] = segment.ljust(NUM_COLS)
            sleep(scroll_speed)

# --- FUNCIÓN: ESCRITURA AL LCD ---
def lcd_writer():
    global framebuffer
    while True:
        with buffer_lock:
            line0 = framebuffer[0]
            line1 = framebuffer[1]
        lcd.home()
        lcd.write_string(line0)
        lcd.crlf()
        lcd.write_string(line1)
        sleep(0.1)

# --- MAIN ---
def main():
    lcd.clear()
    t1 = threading.Thread(target=getTempRoom, daemon=True)
    t2 = threading.Thread(target=name_marquee, daemon=True)
    t3 = threading.Thread(target=lcd_writer, daemon=True)

    t1.start()
    t2.start()
    t3.start()

    app.run(host="0.0.0.0", port=8080)

if __name__ == "__main__":
    main()
