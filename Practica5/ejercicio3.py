import vlc
import time
import os
import pyudev
import subprocess as sp
import threading

# ----------------------------
# Configuración inicial
# ----------------------------
video_path = "/home/artsol/videos/video.mp4"   # ruta del video
video_duration = 20                            # ahora dura 20 segundos
default_image_folder = "/home/artsol/pictures" # carpeta con imágenes por defecto
image_duration = 3                             # segundos por imagen

instance = vlc.Instance()
player = instance.media_player_new()

# Variable global que almacena la carpeta de imágenes a mostrar
current_image_folder = default_image_folder
usb_inserted = False


# ----------------------------
# Funciones multimedia
# ----------------------------
def play_video(path, duration):
    """
    Reproduce un video con transición de volumen:
    - 0 a 5s: fade-in (0% → 100%)
    - 5 a 15s: volumen máximo
    - 15 a 20s: fade-out (100% → 0%)
    """
    media = instance.media_new(path)
    player.set_media(media)
    player.play()

    # Esperar a que arranque realmente la reproducción
    time.sleep(0.5)

    # FADE IN (5s, sube 0 → 100 en pasos de 20)
    for vol in range(0, 101, 20):
        player.audio_set_volume(vol)
        time.sleep(1)  # total ~5s

    # VOLUMEN MÁXIMO durante 10s
    player.audio_set_volume(100)
    time.sleep(10)

    # FADE OUT (5s, baja 100 → 0 en pasos de 20)
    for vol in range(100, -1, -20):
        player.audio_set_volume(vol)
        time.sleep(1)  # total ~5s

    player.stop()


def show_images(duration):
    global current_image_folder
    while True:
        if not os.path.isdir(current_image_folder):
            time.sleep(1)
            continue

        images = [os.path.join(current_image_folder, f)
                  for f in os.listdir(current_image_folder)
                  if f.lower().endswith((".jpg", ".png"))]

        if not images:
            time.sleep(1)
            continue

        for image_path in images:
            media = instance.media_new(image_path)
            player.set_media(media)
            player.play()
            time.sleep(duration)
            player.stop()


# ----------------------------
# Funciones USB
# ----------------------------
def auto_mount(path):
    args = ["udisksctl", "mount", "-b", path]
    sp.run(args)


def get_mount_point(path):
    args = ["findmnt", "-unl", "-S", path]
    cp = sp.run(args, capture_output=True, text=True)
    out = cp.stdout.split(" ")[0]
    return out


def usb_monitor():
    """
    Monitorea inserción de dispositivos USB y cambia
    la carpeta de imágenes cuando se detecta.
    """
    global current_image_folder, usb_inserted

    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by(subsystem="block", device_type="partition")

    for action, device in monitor:
        if action == "add" and not usb_inserted:
            usb_path = "/dev/" + device.sys_name
            auto_mount(usb_path)
            mp = get_mount_point(usb_path)
            print(f"USB detectada en: {mp}")
            current_image_folder = mp  # usar carpeta de USB
            usb_inserted = True


# ----------------------------
# Programa principal
# ----------------------------
if __name__ == "__main__":
    # Hilo en segundo plano para detección de USB
    t = threading.Thread(target=usb_monitor, daemon=True)
    t.start()

    play_video(video_path, video_duration)   # primero se reproduce el video (20s con control de volumen)
    show_images(image_duration)              # luego se muestran imágenes en loop
