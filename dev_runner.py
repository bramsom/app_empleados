import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

# Ruta directa al archivo que estás observando
ARCHIVO = "views/apprentice_panel.py"

# Ruta completa al Python del entorno virtual (ajústala si es necesario)
PYTHON_EXECUTABLE = r"C:\Users\Usuario\Documents\proyectos python\app_empleados\venv\Scripts\python.exe"

PROCESO = None

class Recargador(FileSystemEventHandler):
    def on_modified(self, event):
        global PROCESO
        if event.src_path.endswith("apprentice_panel.py"):
            print("[INFO] Cambios detectados. Recargando vista...")
            if PROCESO:
                PROCESO.kill()
            PROCESO = subprocess.Popen([PYTHON_EXECUTABLE, ARCHIVO])

if __name__ == "__main__":
    print("[INFO] Modo desarrollo iniciado (CTRL+C para detener)...")

    event_handler = Recargador()
    observer = Observer()
    observer.schedule(event_handler, path="views", recursive=False)
    observer.start()

    # Ejecutar por primera vez
    PROCESO = subprocess.Popen([PYTHON_EXECUTABLE, ARCHIVO])

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[INFO] Modo desarrollo detenido.")
        observer.stop()
        if PROCESO:
            PROCESO.kill()
    observer.join()
