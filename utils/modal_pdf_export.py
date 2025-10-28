import customtkinter as ctk
import tkinter as tk
from tkinter import Toplevel, messagebox, filedialog
from typing import Callable, Optional, Any, List, Dict

# import opcional de la generación por defecto (si no se inyecta)
from services.pdf_generator import generar_certificado_contratos

class ModalExportPDF:
    """
    Modal reutilizable para seleccionar empleado y opciones de exportación PDF.
    Parámetros:
    - parent: widget padre (usualmente self de la vista)
    - obtener_empleados_cb: callable() -> list[dict|obj] (lista de empleados para búsqueda)
    - consultar_contratos_cb: callable(emp_id) -> list[contratos]
    - generar_cb: callable(emp, contratos, ruta, opciones) opcional. Si no se pasa usa generar_certificado_contratos.
    """
    def __init__(self,
                 parent,
                 obtener_empleados_cb: Callable[[], List[Any]],
                 consultar_contratos_cb: Callable[[Any], List[Any]],
                 generar_cb: Optional[Callable[..., str]] = None):
        self.parent = parent
        self.obtener_empleados_cb = obtener_empleados_cb
        self.consultar_contratos_cb = consultar_contratos_cb
        self.generar_cb = generar_cb or generar_certificado_contratos
        self.ventana = None
        self.selected_empleado = None

    def open(self):
        self.ventana = Toplevel(self.parent)
        self.ventana.title("Exportar certificado PDF")
        self.ventana.geometry("760x420")
        self.ventana.transient(self.parent)
        self.ventana.grab_set()

        main = ctk.CTkFrame(self.ventana, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=12, pady=12)
        main.grid_columnconfigure(0, weight=1)
        main.grid_columnconfigure(1, weight=0)
        main.grid_columnconfigure(2, weight=1)

        ctk.CTkLabel(main, text="Buscar por nombre o documento:").grid(row=0, column=0, columnspan=3, sticky="w", pady=(0,6))
        self.entry_busqueda = ctk.CTkEntry(main, width=400)
        self.entry_busqueda.grid(row=1, column=0, sticky="ew", padx=(0,8))
        btn_buscar = ctk.CTkButton(main, text="Buscar", width=110, command=self._buscar_empleado)
        btn_buscar.grid(row=1, column=1, sticky="w")
        self.resultado_label = ctk.CTkLabel(main, text="", wraplength=520)
        self.resultado_label.grid(row=1, column=2, sticky="w", padx=(12,0))

        ctk.CTkLabel(main, text="Formato del certificado:").grid(row=2, column=0, sticky="w", pady=(12,4))
        self.formato_seleccion_var = ctk.StringVar(value="Tabla de contratos")
        opt_formato = ctk.CTkOptionMenu(main, values=["Tabla de contratos", "Solo descripción"], variable=self.formato_seleccion_var)
        opt_formato.grid(row=3, column=0, sticky="w")

        self.include_pago_var = ctk.BooleanVar(value=True)
        self.chk_include_pago = ctk.CTkCheckBox(main, text="Incluir columna 'Pago' en el certificado", variable=self.include_pago_var)
        self.chk_include_pago.grid(row=3, column=1, columnspan=2, sticky="w", padx=(8,0))

        ctk.CTkLabel(main, text="Descripción de las labores (opcional):").grid(row=4, column=0, sticky="w", pady=(12,4))
        self.text_desc = tk.Text(main, height=7, width=70, wrap="word")
        self.text_desc.grid(row=5, column=0, columnspan=3, sticky="ew", pady=(0,8))

        ctk.CTkLabel(main, text="Representante legal:").grid(row=6, column=0, sticky="w", pady=(8,4))
        representantes = ["EDGAR ALFONSO PAJA FLOR", "MARÍA PÉREZ", "OTRO..."]
        self.representante_var = ctk.StringVar(value=representantes[0])
        opt_rep = ctk.CTkOptionMenu(main, values=representantes, variable=self.representante_var)
        opt_rep.grid(row=7, column=0, sticky="w")

        ctk.CTkLabel(main, text="Si desea, escriba el nombre del representante:").grid(row=6, column=1, columnspan=2, sticky="w", padx=(8,0))
        self.entry_representante = ctk.CTkEntry(main, width=360, state="disabled")
        self.entry_representante.grid(row=7, column=1, columnspan=2, sticky="ew", padx=(8,0))

        btn_frame = ctk.CTkFrame(main, fg_color="transparent")
        btn_frame.grid(row=8, column=0, columnspan=3, pady=(16,0), sticky="e")
        btn_aceptar = ctk.CTkButton(btn_frame, text="Generar PDF", fg_color="#06A051", width=140, command=self._aceptar)
        btn_cancel = ctk.CTkButton(btn_frame, text="Cancelar", fg_color="#D3D3D3", width=100, command=self.ventana.destroy)
        btn_cancel.grid(row=0, column=0, padx=(0,8))
        btn_aceptar.grid(row=0, column=1)

        # traces / bindings
        try:
            self.representante_var.trace_add("write", self._on_representante_change)
        except Exception:
            self.representante_var.trace("w", lambda *a: self._on_representante_change())
        try:
            self.formato_seleccion_var.trace_add("write", self._on_formato_change)
        except Exception:
            self.formato_seleccion_var.trace("w", lambda *a: self._on_formato_change())

        # init states
        self._on_representante_change()
        self._on_formato_change()

    def _buscar_empleado(self):
        texto = self.entry_busqueda.get().strip().lower()
        empleados = []
        try:
            empleados = self.obtener_empleados_cb() or []
        except Exception:
            pass
        # búsqueda simple por nombre o documento; asume lista de dicts/objetos
        encontrados = []
        for e in empleados:
            name = e.get("name","") if isinstance(e, dict) else getattr(e, "name", "")
            last = e.get("last_name","") if isinstance(e, dict) else getattr(e, "last_name", "")
            doc = e.get("document_number","") if isinstance(e, dict) else getattr(e, "document_number", "")
            if texto in f"{name} {last}".lower() or texto in str(doc).lower():
                encontrados.append(e)
        if encontrados:
            emp = encontrados[0]
            self.selected_empleado = emp
            nombre = (emp.get("name","") + " " + emp.get("last_name","")) if isinstance(emp, dict) else f"{getattr(emp,'name','')} {getattr(emp,'last_name','')}"
            docn = emp.get("document_number") if isinstance(emp, dict) else getattr(emp, "document_number", "")
            self.resultado_label.configure(text=f"Seleccionado: {nombre} \n(documento: {docn})")
        else:
            self.selected_empleado = None
            self.resultado_label.configure(text="No se encontró ningún empleado.")

    def _on_representante_change(self, *a):
        try:
            if self.representante_var.get() == "OTRO...":
                self.entry_representante.configure(state="normal")
                self.entry_representante.focus_set()
            else:
                self.entry_representante.delete(0, "end")
                self.entry_representante.configure(state="disabled")
        except Exception:
            pass

    def _on_formato_change(self, *a):
        sel = self.formato_seleccion_var.get()
        if sel == "Tabla de contratos":
            try:
                self.chk_include_pago.configure(state="normal")
            except Exception:
                pass
            self.include_pago_var.set(True)
            self.text_desc.configure(state=tk.NORMAL)
            self.text_desc.delete("1.0", "end")
            self.text_desc.configure(state=tk.DISABLED)
        else:
            try:
                self.chk_include_pago.configure(state="disabled")
            except Exception:
                pass
            self.include_pago_var.set(False)
            self.text_desc.configure(state=tk.NORMAL)

    def _aceptar(self):
        if not self.selected_empleado:
            messagebox.showerror("Error", "No se ha seleccionado un empleado válido.")
            return
        emp = self.selected_empleado
        emp_id = emp.get("id") if isinstance(emp, dict) else getattr(emp, "id", None)
        if emp_id is None:
            messagebox.showerror("Error", "Empleado seleccionado no tiene ID válido.")
            return
        try:
            contratos = self.consultar_contratos_cb(emp_id)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron obtener los contratos: {e}")
            return

        ruta = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")], title="Guardar reporte PDF")
        if not ruta:
            return

        selected_formato = self.formato_seleccion_var.get()
        show_table = True if selected_formato == "Tabla de contratos" else False
        include_pago = bool(self.include_pago_var.get()) and show_table

        rep_text = self.entry_representante.get().strip()
        representante_final = rep_text if rep_text else self.representante_var.get()
        labores_desc = ""
        if not show_table:
            labores_desc = self.text_desc.get("1.0", "end").strip()

        emp_dict = emp if isinstance(emp, dict) else {k: v for k, v in emp.__dict__.items() if not k.startswith("_")}

        try:
            # la callback acepta los mismos parámetros que generar_certificado_contratos
            self.generar_cb(emp_dict, contratos, ruta,
                            entidad_nombre="COLEGIO CIUDAD DE PIENDAMÓ",
                            nit="NIT.817001256-7",
                            representante=representante_final,
                            fecha_expedicion=None,
                            include_pago=include_pago,
                            labores_descripcion=labores_desc,
                            show_table=show_table)
            messagebox.showinfo("Éxito", f"Reporte guardado en: {ruta}")
            self.ventana.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el PDF: {e}")
            return