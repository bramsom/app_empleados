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
