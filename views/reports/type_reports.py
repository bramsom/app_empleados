import customtkinter as ctk
from tkinter import Toplevel,messagebox
import pandas as pd
from PIL import Image
from fpdf import FPDF
from utils.canvas import agregar_fondo_decorativo
from services.pdf_generator import obtener_periodo_laborado, calcular_tiempo_laborado
from controllers.report_controller import ReportController

class ExportarTipoReporte(ctk.CTkFrame):
    def __init__(self, parent, username, rol, obtener_datos_excel_callback, obtener_datos_pdf_callback, volver_callback):
        super().__init__(parent)
        self.username = username
        self.rol = rol
        self.obtener_datos_excel_callback = obtener_datos_excel_callback
        self.obtener_datos_pdf_callback = obtener_datos_pdf_callback
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
            command=self.exportar_pdf
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
            datos = self.obtener_datos_excel_callback()
            if not datos:
                messagebox.showinfo("Sin datos", "No hay datos para exportar.")
                return
            df = pd.DataFrame(datos)
            ruta = "C:/Users/Usuario/Documents/reportes app empleados/reporte.xlsx"
            df.to_excel(ruta, index=False)
            messagebox.showinfo("Éxito", f"Datos exportados correctamente a {ruta}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar: {e}")

    def exportar_pdf(self):
        # Ventana emergente para buscar empleado
        ventana = Toplevel(self)
        ventana.title("Buscar empleado")
        ventana.geometry("400x200")
        ventana.transient(self)
        ventana.grab_set()

        ctk.CTkLabel(ventana, text="Buscar por nombre o documento:").pack(pady=10)
        entry_busqueda = ctk.CTkEntry(ventana, width=250)
        entry_busqueda.pack(pady=5)

        resultado_label = ctk.CTkLabel(ventana, text="")
        resultado_label.pack(pady=5)

        def buscar_empleado():
            texto = entry_busqueda.get().strip().lower()
            empleados = self.obtener_datos_pdf_callback()
            encontrados = ReportController.buscar_empleado_por_nombre_o_documento(empleados, texto)
            if encontrados:
                emp = encontrados[0]
                resultado_label.configure(text=f"Nombre: {emp.name}\nDocumento: {emp.document_number}")
                ventana.selected_empleado = emp
            else:
                resultado_label.configure(text="No encontrado")
                ventana.selected_empleado = None

        def aceptar():
            emp = getattr(ventana, "selected_empleado", None)
            if not emp:
                messagebox.showerror("Error", "No se ha seleccionado un empleado válido.")
                return
            fecha_inicio, fecha_fin, tiempo_laborado = ReportController.generar_info_laboral(emp.id)
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=14)
            pdf.cell(200, 10, txt="Reporte de Trabajo", ln=True, align="C")
            pdf.ln(10)
            pdf.cell(0, 10, f"Nombre: {emp.name}", ln=True)
            pdf.cell(0, 10, f"Documento: {emp.document_number}", ln=True)
            pdf.cell(0, 10, f"Cargo: {getattr(emp, 'position', 'N/A')}", ln=True)
            pdf.cell(0, 10, f"Tiempo laborado: {tiempo_laborado}", ln=True)
            pdf.cell(0, 10, f"Periodo: {fecha_inicio} a {fecha_fin}", ln=True)
            ruta = "C:/Users/Usuario/Documents/reportes app empleados/reporte_empleado.pdf"
            pdf.output(ruta)
            messagebox.showinfo("Éxito", f"PDF exportado correctamente a {ruta}")
            ventana.destroy()

        def cancelar():
            ventana.destroy()
        
        ctk.CTkButton(ventana, text="Buscar", command=buscar_empleado).pack(pady=5)
        ctk.CTkButton(ventana, text="Aceptar", command=aceptar).pack(side="left", padx=20, pady=10)
        ctk.CTkButton(ventana, text="Cancelar", command=cancelar).pack(side="right", padx=20, pady=10)

    def _volver(self):
        if self.volver_callback:
            self.destroy()
            self.volver_callback()