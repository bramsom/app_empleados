import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

# Directorio base del proyecto (donde está dev_runner.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Archivo que estás observando
ARCHIVO = os.path.join(BASE_DIR, "views", "crud_employees.py")

# Ruta al Python del entorno virtual
# Usa la ruta relativa para que funcione en cualquier equipo
PYTHON_EXECUTABLE = os.path.join(BASE_DIR, ".venv", "Scripts", "python.exe")

# Archivo principal a ejecutar (login.py o main.py)
MAIN = os.path.join(BASE_DIR, "main.py")

PROCESO = None

class Recargador(FileSystemEventHandler):
    def on_modified(self, event):
        global PROCESO
        if event.src_path.endswith(".py"):
            print("[INFO] Cambios detectados. Recargando vista...")
            if PROCESO:
                PROCESO.kill()
            ejecutar_main_con_modo_dev()

def ejecutar_main_con_modo_dev():
    global PROCESO
    env = os.environ.copy()
    env["DEV_MODE"] = "1"  # Activar modo desarrollo
    PROCESO = subprocess.Popen([PYTHON_EXECUTABLE, MAIN], env=env)

if __name__ == "__main__":
    print("[INFO] Modo desarrollo con recarga automática iniciado (CTRL+C para detener)...")

    event_handler = Recargador()
    observer = Observer()
    observer.schedule(event_handler, path="views", recursive=True)
    observer.start()

    # Ejecutar por primera vez
    ejecutar_main_con_modo_dev()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[INFO] Modo desarrollo detenido.")
        observer.stop()
        if PROCESO:
            PROCESO.kill()
    observer.join()
