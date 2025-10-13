import os, sys

# asegurar que la raíz del proyecto está en sys.path
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root not in sys.path:
    sys.path.insert(0, root)

from bd.setup import eliminar_base_de_datos, crear_tablas

def main():
    # Borra el archivo de BD si existe y crea las tablas nuevas
    eliminar_base_de_datos()
    crear_tablas()
    print("Base de datos reiniciada y tablas creadas.")

if __name__ == "__main__":
    main()