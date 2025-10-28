# main.py

# from views.login import LoginApp
# from views.create_user import CrearUsuario
# from views.data_management import GestionUsuarios
#from bd.setup import crear_tablas
# from views.crud_employees import CrudEmpleados
# from views.crud_contracts import CrudContratos
# from views.crud_afiliations import CrudAfiliaciones
#from views.login import LoginApp
#from bd.setup import crear_tablas, migrar_datos,eliminar_base_de_datos
from views.login import LoginApp  # Agrega esta importación para poder iniciar la app
import sys
import os

# Parche: si estamos "frozen" por PyInstaller, cambiar CWD a sys._MEIPASS
if getattr(sys, "frozen", False):
    meipass = getattr(sys, "_MEIPASS", None)
    if meipass:
        try:
            os.chdir(meipass)
        except Exception:
            pass

# Forzar inclusión de módulos utils para PyInstaller (evita No module named 'utils.xxx')
try:
    # lista explícita de los módulos que te dan error
    import utils.autocomplete
    import utils.contract_filters
    import utils.contract_helpers
    # añade aquí otros módulos utils si aparecen en errores
except Exception:
    # importa dinámicamente todo el paquete utils si prefieres
    try:
        import pkgutil, importlib
        pkg_path = os.path.join(os.path.dirname(__file__), "utils")
        for m in pkgutil.iter_modules([pkg_path]):
            importlib.import_module(f"utils.{m.name}")
    except Exception:
        pass

# Forzar inclusión explícita de módulos utils que se importan dinámicamente
try:
    import utils.autocomplete
    import utils.contract_filters
    import utils.contract_helpers
    import utils.modal_history   # <- añadir esto
except Exception:
    pass

# Forzar inclusión de controllers que fallan en el exe
try:
    import controllers.user_controller
    #import controllers.user_controller  # añade otros que falten
except Exception:
    pass

# Importar vistas/despegar aplicación (después de ajustar CWD)
from views.login import LoginApp

# Parche: si estamos "frozen" por PyInstaller, cambiar CWD a sys._MEIPASS
# y escribir debug_bundle.txt para ver qué ficheros se extrajeron.
if getattr(sys, "frozen", False):
    meipass = getattr(sys, "_MEIPASS", None)
    if meipass:
        try:
            print("Ejecutando desde bundle. _MEIPASS =", meipass)
            os.chdir(meipass)
            dump = os.path.join(os.getcwd(), "debug_bundle.txt")
            with open(dump, "w", encoding="utf-8") as fh:
                for root, dirs, files in os.walk(meipass or "."):
                    fh.write(f"ROOT: {root}\n")
                    for d in dirs:
                        fh.write(f"  DIR: {d}\n")
                    for f in files:
                        fh.write(f"  FILE: {f}\n")
            print("Wrote debug bundle to:", dump)
        except Exception as e:
            print("No se pudo escribir debug_bundle.txt:", e)
else:
    print("Modo desarrollo. CWD =", os.getcwd())

#if __name__ == "__main__":
    #print("Iniciando proceso de migración de datos...")
    #eliminar_base_de_datos()
    #migrar_datos()
    #print("Proceso de migración finalizado.")

    #crear_tablas()

# crear_usuario("admin1", "admin123", "administrador")
# crear_usuario("aprendiz1", "aprendiz123", "aprendiz")

# usuarios = obtener_usuarios()
# print(usuarios)

# exito, rol = verificar_credenciales("admin1", "admin123")
# if exito:
#     print(f"Login exitoso como {rol}")
# else:
#     print("Credenciales incorrectas")
# Para ejecutar directamente
if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()
