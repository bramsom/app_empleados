# main.py

from views.login import iniciar_app
from bd.setup import crear_tablas

if __name__ == "__main__":
    crear_tablas()