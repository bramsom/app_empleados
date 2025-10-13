import customtkinter as ctk
from tkinter import Toplevel,messagebox
import pandas as pd
from PIL import Image
from fpdf import FPDF
from utils.canvas import agregar_fondo_decorativo
from controllers.report_controller import obtener_datos_para_excel
from services.pdf_generator import obtener_periodo_laborado, calcular_tiempo_laborado
from controllers.contract_controller import consultar_contratos_por_empleado
from services.pdf_generator import generar_certificado_contratos
from controllers.report_controller import ReportController
from tkinter import filedialog
from utils.modal_excel_selection import ModalSeleccionExcel

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
            compound="top",
            command=self.exportar_excel
        )
        self.btn_exportar_excel.pack(side="left", padx=(130, 10), pady=20)

    def exportar_excel(self):
        def exportar_callback(tablas_a_exportar):
            ruta = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")],
                title="Guardar reporte Excel"
            )
            if not ruta:
                return  # El usuario canceló

            # Mapa de columnas (ajusta las claves a las que devuelve tu controlador)
            column_map = {
                "id": "ID",
                "name": "Nombre",
                "last_name": "Apellido",
                "document_type": "Tipo documento",
                "document_number": "Número documento",
                "document_issuance": "Lugar expedición",
                "birthdate": "Fecha nacimiento",
                "phone_number": "Teléfono",
                "residence_address": "Dirección",
                "RUT": "RUT",
                "email": "Correo",
                "position": "Cargo",
                "employee_id": "ID Empleado",
                "type_contract": "Tipo contrato",
                "start_date": "Fecha inicio",
                "end_date": "Fecha fin",
                "state": "Estado",
                "contractor": "Contratante",
                "total_payment": "Pago total",
                "payment_frequency": "Número de cuotas",
                "monthly_payment": "Salario mensual",
                "transport": "Transporte",
                "value_hour": "Valor hora",
                "number_hour": "Número horas",
                "eps": "EPS",
                "arl": "ARL",
                "risk_level": "Nivel de riesgo",
                "afp": "AFP",
                "compensation_box": "Caja compensación",
                "bank": "Banco",
                "account_number": "Número cuenta",
                "account_type": "Tipo cuenta"
                # añade/ajusta según necesites
            }

            contract_type_map = {
                "CONTRATO INDIVIDUAL DE TRABAJO TERMINO FIJO": ("C.I.T.T.F", "Contrato Individual de Trabajo a Término Fijo"),
                "CONTRATO INDIVIDUAL DE TRABAJO TERMINO INDEFINIDO": ("C.I.T.T.I", "Contrato Individual de Trabajo a Término Indefinido"),
                "CONTRATO SERVICIO HORA CATEDRA": ("C.S.H.C", "Contrato de Prestación de Servicios - Hora Cátedra"),
                "CONTRATO APRENDIZAJE SENA": ("C.A.S", "Contrato de Aprendizaje SENA"),
                "ORDEN PRESTACION DE SERVICIOS": ("O.P.S", "Orden de Prestación de Servicios")
            }
            # Usa el controlador para obtener los datos
            datos = obtener_datos_para_excel(tablas_a_exportar)
            import pandas as pd
            with pd.ExcelWriter(ruta) as writer:
                if "empleados" in tablas_a_exportar and "empleados" in datos:
                    df_emp = pd.DataFrame(datos["empleados"])
                    df_emp = df_emp.rename(columns=column_map)
                    df_emp.to_excel(writer, sheet_name="Empleados", index=False)

                if "contratos" in tablas_a_exportar and "contratos" in datos:
                    df_con = pd.DataFrame(datos["contratos"])
                    df_con = df_con.rename(columns=column_map)
                    df_con.to_excel(writer, sheet_name="Contratos", index=False)

                if "afiliaciones" in tablas_a_exportar and "afiliaciones" in datos:
                    df_afi = pd.DataFrame(datos["afiliaciones"])
                    df_afi = df_afi.rename(columns=column_map)
                    df_afi.to_excel(writer, sheet_name="Afiliaciones", index=False)
            messagebox.showinfo("Éxito", f"Datos exportados correctamente a {ruta}")

        ModalSeleccionExcel(self, exportar_callback)

    def exportar_pdf(self):
        # Ventana emergente para buscar empleado
        ventana = Toplevel(self)
        ventana.title("Buscar empleado")
        ventana.geometry("420x220")
        ventana.transient(self)
        ventana.grab_set()

        ctk.CTkLabel(ventana, text="Buscar por nombre o documento:").pack(pady=10)
        entry_busqueda = ctk.CTkEntry(ventana, width=280)
        entry_busqueda.pack(pady=5)

        resultado_label = ctk.CTkLabel(ventana, text="", wraplength=380)
        resultado_label.pack(pady=5)

        def buscar_empleado():
            texto = entry_busqueda.get().strip().lower()
            # obtener listado de empleados (usa callback si fue pasado al crear la vista)
            if hasattr(self, "obtener_datos_pdf_callback") and callable(self.obtener_datos_pdf_callback):
                empleados = self.obtener_datos_pdf_callback()
            else:
                # fallback: ReportController debe proveer una lista si no hay callback
                empleados = ReportController.obtener_todos_los_empleados() if hasattr(ReportController, "obtener_todos_los_empleados") else []

            encontrados = ReportController.buscar_empleado_por_nombre_o_documento(empleados, texto)
            if encontrados:
                emp = encontrados[0]
                ventana.selected_empleado = emp
                nombre = emp.get("name") + " " + emp.get("last_name") if isinstance(emp, dict) else f"{getattr(emp,'name','')} {getattr(emp,'last_name','')}"
                resultado_label.configure(text=f"Seleccionado: {nombre} \n(numero documento: {emp.get('document_number') if isinstance(emp, dict) else getattr(emp,'document_number','')})")
            else:
                ventana.selected_empleado = None
                resultado_label.configure(text="No se encontró ningún empleado.")

        btn_buscar = ctk.CTkButton(ventana, text="Buscar", command=buscar_empleado)
        btn_buscar.pack(pady=(5,10))

        def aceptar():
            emp = getattr(ventana, "selected_empleado", None)
            if not emp:
                messagebox.showerror("Error", "No se ha seleccionado un empleado válido.")
                return

            emp_id = emp.get("id") if isinstance(emp, dict) else getattr(emp, "id", None)
            if emp_id is None:
                messagebox.showerror("Error", "Empleado seleccionado no tiene ID válido.")
                return

            # obtener contratos del empleado
            try:
                contratos = consultar_contratos_por_empleado(emp_id)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudieron obtener los contratos: {e}")
                return

            # pedir ruta de guardado
            ruta = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")],
                title="Guardar reporte PDF"
            )
            if not ruta:
                return

            try:
                # pasar emp como dict al generador
                emp_dict = emp if isinstance(emp, dict) else {k: v for k, v in emp.__dict__.items() if not k.startswith("_")}
                generar_certificado_contratos(emp_dict, contratos, ruta,
                                              entidad_nombre="COLEGIO CIUDAD DE PIENDAMÓ",
                                              nit="NIT.817001256-7",
                                              representante="EDGAR ALFONSO PAJA FLOR")
                messagebox.showinfo("Éxito", f"Reporte guardado en: {ruta}")
                ventana.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo generar el PDF: {e}")

        btn_aceptar = ctk.CTkButton(ventana, text="Generar PDF", fg_color="#06A051", command=aceptar)
        btn_aceptar.pack(pady=(0,10))

    def _volver(self):
        if self.volver_callback:
            self.destroy()
            self.volver_callback()