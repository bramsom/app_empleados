import customtkinter as ctk
from PIL import Image

class MenuDesplegable(ctk.CTkFrame):
    def __init__(self, master, usuario):
        super().__init__(master, width=20, corner_radius=20, fg_color="#2F2F2F")
        self.pack(side="left", fill="y")
        self.usuario = usuario
        self.expanded = False
        self._hover_id=None
        self.hover_count = 0  # Rastrea el número de widgets donde el mouse está encima

        # Vincula eventos al propio frame
        self.bind("<Enter>", self._hover_in, add="+")
        self.bind("<Leave>", self._hover_out, add="+")

        self.botones = []

        # Ejemplo para botón de Inicio
        icono_inicio = ctk.CTkImage(Image.open("C:/Users/Usuario/Documents/proyectos python/app_empleados/images/logo.png"), size=(24, 24))

        self.boton_inicio = ctk.CTkButton(
            self,
            text="Inicio",
            image=icono_inicio,
            compound="left",
            anchor="w",
            fg_color="transparent",
            hover_color="#3F3F3F",
            command=self.ir_inicio
        )
        self.boton_inicio.pack(pady=5, padx=10, fill="x")

        # Guardamos el botón y su texto original
        self.botones.append((self.boton_inicio, "Inicio"))


    def crear_boton(self, texto, comando):
        boton = ctk.CTkButton(
            self, text=texto, anchor="w",
            fg_color="transparent", hover_color="#3F3F3F",
            command=comando
        )
        boton.pack(pady=10, padx=10, fill="x")
        boton.bind("<Enter>", self._hover_in, add="+")
        boton.bind("<Leave>", self._hover_out, add="+")
        return boton
        
        #self._hover_id = None  # Variable para controlar cancelación de temporizador

    def _hover_in(self, event=None):
        if self._hover_id:
            self.after_cancel(self._hover_id)
            self._hover_id = None
        self.expandir_menu()

    def _hover_out(self, event=None):
        self._hover_id = self.after(300, self.verificar_mouse_fuera)

    def verificar_mouse_fuera(self):
        x, y = self.winfo_pointerxy()
        widget_bajo_cursor = self.winfo_containing(x, y)
        if widget_bajo_cursor not in self.winfo_children() + [self]:
            self.colapsar_menu()

    def expandir_menu(self):
        self.configure(width=200)  # Ajusta el ancho del menú
        for boton, texto in self.botones:
            boton.configure(text=texto, anchor="w", compound="left")

    def colapsar_menu(self):
        self.configure(width=60)
        for boton, _ in self.botones:
            boton.configure(text="", anchor="center", compound="left")

    # Funciones simuladas
    def ir_inicio(self):
        print("Ir a Inicio")

    def ir_usuarios(self):
        print("Ir a Usuarios")

# Uso
if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("700x500")
    menu = MenuDesplegable(app, usuario="Laura Pérez")
    app.mainloop()
