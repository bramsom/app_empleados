import customtkinter as ctk
from tkinter import messagebox
import pandas as pd
from PIL import Image
from utils.canvas import agregar_fondo_decorativo

class ExportarExcel(ctk.CTkFrame):
    def __init__(self, parent, username, rol, obtener_datos_callback, volver_callback):
        super().__init__(parent)
        self.username = username
        self.rol = rol
        self.obtener_datos_callback = obtener_datos_callback
        self.volver_callback = volver_callback


        self.icon_excel = ctk.CTkImage(Image.open("images/excel.png"), size=(300, 300))
        self.icon_pdf = ctk.CTkImage(Image.open("images/pdf.png"), size=(300, 300))  # Debes tener una imagen pdf.png

        agregar_fondo_decorativo(self)
        self.configure(fg_color="#F5F5F5")

        self.icon_back = ctk.CTkImage(Image.open("images/arrow.png"), size=(30, 30))

        self.btn_volver = ctk.CTkButton(
            self, text="", image=self.icon_back, width=40,
            height=40, fg_color="#D3D3D3", hover_color="#F3EFEF",corner_radius=0 ,
            command=self._volver
        )
        self.btn_volver.place(relx=0.98, rely=0.02, anchor="ne")


        self.btn_exportar_pdf = ctk.CTkButton(
            self, image=self.icon_pdf, text="Exportar PDF", width=480, height=550, font=("Georgia", 30),
            fg_color="#FFEFEF", hover_color="#D9D9D9", text_color="black",
            compound="top",  # Imagen arriba del texto
            #command=self.exportar_pdf
        )
        self.btn_exportar_pdf.pack(side="left", padx=(150, 10), pady=20)


        self.btn_exportar_excel = ctk.CTkButton(
            self, image=self.icon_excel, text="Exportar Excel", width=480, height=550, font=("Georgia", 30),
            fg_color="#FFEFEF", hover_color="#D9D9D9", text_color="black",
            compound="top",  # Imagen arriba del texto
            command=self.exportar_excel
        )
        self.btn_exportar_excel.pack(side="left", padx=(130, 10), pady=20)

    def exportar_excel(self):
        try:
            datos = self.obtener_datos_callback()
            if not datos:
                messagebox.showinfo("Sin datos", "No hay datos para exportar.")
                return
            df = pd.DataFrame(datos)
            ruta = "C:/Users/Usuario/Documents/reportes app empleados/reporte.xlsx"
            df.to_excel(ruta, index=False)
            messagebox.showinfo("Éxito", f"Datos exportados correctamente a {ruta}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar: {e}")

    #def exportar_pdf(self):
        #try:
        #    datos = self.obtener_datos_callback()
        #    if not datos:
        #        messagebox.showinfo("Sin datos", "No hay datos para exportar.")
        #        return
        #    pdf = FPDF()
        #    pdf.add_page()
        #    pdf.set_font("Arial", size=12)
        #    pdf.cell(200, 10, txt="Reporte de Usuarios", ln=True, align="C")
            # Encabezados
        #    if datos:
        #        encabezados = list(datos[0].keys())
        #        for encabezado in encabezados:
        #            pdf.cell(40, 10, encabezado, border=1)
        #        pdf.ln()
                # Filas
        #        for fila in datos:
        #            for encabezado in encabezados:
        #                pdf.cell(40, 10, str(fila[encabezado]), border=1)
        #            pdf.ln()
        #    ruta = "C:/Users/Usuario/Documents/reportes app empleados/reporte.pdf"
        #    pdf.output(ruta)
        #    messagebox.showinfo("Éxito", f"PDF exportado correctamente a {ruta}")
        #except Exception as e:
        #    messagebox.showerror("Error", f"No se pudo exportar PDF: {e}")

    def _volver(self):
        if self.volver_callback:
            self.destroy()
            self.volver_callback()