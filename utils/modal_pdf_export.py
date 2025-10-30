import customtkinter as ctk
import tkinter as tk
from tkinter import Toplevel, messagebox, filedialog
from typing import Callable, Optional, Any, List
from PIL import Image, ImageTk

from services.pdf_generator import generar_certificado_contratos

# Configuración por defecto
_BASE_WIDTH = 760
_BASE_HEIGHT = 500
_EXPANDED_HEIGHT = 700
_SEARCH_ICON_PATH = "images/seeker.png"


class ModalExportPDF:
    """
    Modal reutilizable para seleccionar empleado y opciones de exportación PDF.
    """

    def __init__(
        self,
        parent,
        obtener_empleados_cb: Callable[[], List[Any]],
        consultar_contratos_cb: Callable[[Any], List[Any]],
        generar_cb: Optional[Callable[..., str]] = None,
        icon_image: Optional[Any] = None,
    ):
        self.parent = parent
        self.obtener_empleados_cb = obtener_empleados_cb
        self.consultar_contratos_cb = consultar_contratos_cb
        self.generar_cb = generar_cb or generar_certificado_contratos

        self.ventana: Optional[Toplevel] = None
        self.selected_empleado: Optional[Any] = None

        # estilos configurables
        self.entry_style = {"border_width": 0, "fg_color": "#D9D9D9", "text_color": "#000000", "height": 40}
        self.boton_style = {"font": ("Georgia", 14), "text_color": "black", "height": 50}

        # icono: puede pasarse como PhotoImage/CTkImage o ruta
        self._icon_image = None
        if icon_image:
            self._icon_image = icon_image
        else:
            try:
                pil = Image.open(_SEARCH_ICON_PATH)
                self._icon_image = ctk.CTkImage(pil, size=(20, 20))
            except Exception:
                self._icon_image = None

        # opciones de representante y títulos asociados
        self._rep_options = [
            "VICTORIA ANDREA TRUJILLO CERON",
            "MARIA ISABEL MUÑOZ GARCIA",
            "OTRO...",
        ]
        self._rep_title_map = {
            self._rep_options[0]: "Jefe de área administrativa y financiera",
            self._rep_options[1]: "Rectora",
            self._rep_options[2]: "Representante Legal",
        }

    def open(self):
        self._create_window()
        self._build_search_bar()
        self._build_info_panel()
        self._build_options_panel()
        self._build_representante_panel()
        self._build_buttons()

        # traces / bindings
        try:
            self.representante_var.trace_add("write", self._on_representante_change)
        except Exception:
            self.representante_var.trace("w", lambda *a: self._on_representante_change())
        try:
            self.formato_seleccion_var.trace_add("write", self._on_formato_change)
        except Exception:
            self.formato_seleccion_var.trace("w", lambda *a: self._on_formato_change())

        # estados iniciales
        self._on_representante_change()
        self._on_formato_change()

        self.ventana.transient(self.parent)
        self.ventana.grab_set()

    # ---------- Construcción UI ----------
    def _create_window(self):
        self.ventana = Toplevel(self.parent)
        self.ventana.title("Exportar certificado PDF")
        self.ventana.geometry(f"{_BASE_WIDTH}x{_BASE_HEIGHT}")
        self.main = ctk.CTkFrame(self.ventana, fg_color="transparent")
        self.main.pack(fill="both", expand=True, padx=12, pady=12)
        self.main.grid_columnconfigure(0, weight=1)
        self.main.grid_columnconfigure(1, weight=0)
        self.main.grid_columnconfigure(2, weight=1)

    def _build_search_bar(self):
        ctk.CTkLabel(self.main, text="Buscar por nombre o documento:").grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 6))
        barra = ctk.CTkFrame(self.main, border_width=2, border_color="#F0F0F0", fg_color="white", corner_radius=20)
        barra.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 8), padx=(0, 8))
        # estilo específico para que solo la barra de búsqueda sea blanca
        search_entry_style = {**self.entry_style, "fg_color": "white"}
        self.entry_busqueda = ctk.CTkEntry(
            barra,
            placeholder_text="Buscar por nombre...",
            width=360,
            corner_radius=20,
            **search_entry_style,
        )
        self.entry_busqueda.pack(side="left", padx=(8, 0), pady=6, fill="x", expand=True)
        self.entry_busqueda.bind("<Return>", lambda e: self._buscar_empleado())
        btn_buscar = ctk.CTkButton(barra, text="", image=self._icon_image, width=36, corner_radius=20, fg_color="white", hover_color="#F0F0F0", command=self._buscar_empleado)
        btn_buscar.pack(side="left", padx=(6, 8), pady=6)

    def _build_info_panel(self):
        info_frame = ctk.CTkFrame(self.main, fg_color="transparent")
        info_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=(0, 8), pady=(0, 6))
        info_frame.grid_columnconfigure(0, weight=3)
        info_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(info_frame, text="Empleado seleccionado:", anchor="w").grid(row=0, column=0, columnspan=2, sticky="w")
        self.entry_name = ctk.CTkEntry(info_frame, state="disabled", **self.entry_style)
        self.entry_name.grid(row=1, column=0, sticky="ew", pady=(4, 6), padx=(0, 8))
        self.entry_doc = ctk.CTkEntry(info_frame, width=140, state="disabled", **self.entry_style)
        self.entry_doc.grid(row=1, column=1, sticky="ew", pady=(4, 6))
        self.resultado_label = ctk.CTkLabel(info_frame, text="", wraplength=300, text_color="#666666")
        self.resultado_label.grid(row=2, column=0, columnspan=2, sticky="w", pady=(2, 0))

    def _build_options_panel(self):
        ctk.CTkLabel(self.main, text="Formato del certificado:").grid(row=2, column=0, sticky="w", pady=(12, 4))
        self.formato_seleccion_var = ctk.StringVar(value="Tabla de contratos")
        opt_formato = ctk.CTkOptionMenu(
            self.main,
            values=["Tabla de contratos", "Solo descripción"],
            variable=self.formato_seleccion_var,
            fg_color="#D9D9D9",
            height=40,
            text_color="black",
            button_color="#06A051",
            button_hover_color="#048B45",
            dropdown_fg_color="white",
            dropdown_text_color="black",
        )
        opt_formato.grid(row=3, column=0, sticky="ew")

        self.include_pago_var = ctk.BooleanVar(value=True)
        self.chk_include_pago = ctk.CTkCheckBox(self.main, text="Incluir columna 'Pago' en el certificado", variable=self.include_pago_var)
        self.chk_include_pago.grid(row=3, column=1, columnspan=2, sticky="w", padx=(8, 0))

        self.options_helper = ctk.CTkLabel(self.main, text="", text_color="#666666")
        self.options_helper.grid(row=3, column=0, sticky="w", padx=(0, 8))

        ctk.CTkLabel(self.main, text="Descripción de las labores (opcional):").grid(row=4, column=0, sticky="w", pady=(12, 4))
        self.text_desc = tk.Text(self.main, height=7, width=70, wrap="word")
        self.text_desc.grid(row=5, column=0, columnspan=3, sticky="ew", pady=(0, 8))

        # ocultar por defecto
        self.chk_include_pago.grid_remove()
        self.text_desc.grid_remove()
        self.options_helper.configure(text="Seleccione un empleado para ver las opciones disponibles.")

    def _build_representante_panel(self):
        ctk.CTkLabel(self.main, text="Representante legal:").grid(row=6, column=0, sticky="w", pady=(8, 4))
        self.representante_var = ctk.StringVar(value=self._rep_options[0])
        opt_rep = ctk.CTkOptionMenu(
            self.main,
            values=self._rep_options,
            variable=self.representante_var,
            fg_color="#D9D9D9",
            height=40,
            text_color="black",
            button_color="#06A051",
            button_hover_color="#048B45",
            dropdown_fg_color="white",
            dropdown_text_color="black",
        )
        opt_rep.grid(row=7, column=0, sticky="ew")
        self._lbl_rep_title = ctk.CTkLabel(self.main, text=self._rep_title_map[self._rep_options[0]], text_color="#444444")
        self._lbl_rep_title.grid(row=8, column=0, sticky="w", pady=(4, 0))
        # entry para OTRO al lado del selector, ancho fijo
        self._entry_other_rep = ctk.CTkEntry(self.main, width=260, placeholder_text="Nombre del representante", **self.entry_style)

    def _build_buttons(self):
        btn_frame = ctk.CTkFrame(self.main, fg_color="transparent")
        btn_frame.grid(row=9, column=0, columnspan=3, pady=(16, 12))
        btn_cancel = ctk.CTkButton(btn_frame, text="Cancelar", fg_color="#D12B1B", hover_color="#B81D0F", width=120, command=self.ventana.destroy, font=self.boton_style["font"], text_color=self.boton_style["text_color"], height=self.boton_style["height"])
        btn_aceptar = ctk.CTkButton(btn_frame, text="Generar PDF", fg_color="#06A051", hover_color="#048B45", width=140, command=self._aceptar, font=self.boton_style["font"], text_color=self.boton_style["text_color"], height=self.boton_style["height"])
        btn_cancel.pack(side="left", padx=(0, 12), pady=6)
        btn_aceptar.pack(side="left", padx=(12, 0), pady=6)

    # ---------- Lógica ----------
    def _adjust_window_for_description(self, show: bool):
        try:
            if show:
                self.ventana.geometry(f"{_BASE_WIDTH}x{_EXPANDED_HEIGHT}")
            else:
                self.ventana.geometry(f"{_BASE_WIDTH}x{_BASE_HEIGHT}")
        except Exception:
            pass

    def _buscar_empleado(self):
        texto = self.entry_busqueda.get().strip().lower()
        empleados = []
        try:
            empleados = self.obtener_empleados_cb() or []
        except Exception:
            empleados = []

        encontrados = []
        for e in empleados:
            name = e.get("name", "") if isinstance(e, dict) else getattr(e, "name", "")
            last = e.get("last_name", "") if isinstance(e, dict) else getattr(e, "last_name", "")
            doc = e.get("document_number", "") if isinstance(e, dict) else getattr(e, "document_number", "")
            if texto in f"{name} {last}".lower() or texto in str(doc).lower():
                encontrados.append(e)

        if not encontrados:
            self.selected_empleado = None
            for entry in (self.entry_name, self.entry_doc):
                entry.configure(state="normal")
                entry.delete(0, "end")
                entry.configure(state="disabled")
            self.resultado_label.configure(text="No se encontró ningún empleado.")
            self._update_option_visibility()
            return

        emp = encontrados[0]
        self.selected_empleado = emp
        nombre = (emp.get("name", "") + " " + emp.get("last_name", "")) if isinstance(emp, dict) else f"{getattr(emp, 'name', '')} {getattr(emp, 'last_name', '')}"
        docn = emp.get("document_number") if isinstance(emp, dict) else getattr(emp, "document_number", "")
        for entry, value in ((self.entry_name, nombre), (self.entry_doc, str(docn))):
            entry.configure(state="normal")
            entry.delete(0, "end")
            entry.insert(0, value)
            entry.configure(state="disabled")
        self.resultado_label.configure(text="Empleado seleccionado")
        self._update_option_visibility()

    def _on_representante_change(self, *a):
        sel = self.representante_var.get()
        if sel == "OTRO...":
            self._lbl_rep_title.grid_remove()
            self._entry_other_rep.grid(row=7, column=1, sticky="w", padx=(8, 0))
            try:
                self._entry_other_rep.focus_set()
            except Exception:
                pass
        else:
            try:
                self._entry_other_rep.delete(0, "end")
            except Exception:
                pass
            self._entry_other_rep.grid_remove()
            title = self._rep_title_map.get(sel, "Representante Legal")
            self._lbl_rep_title.configure(text=title)
            self._lbl_rep_title.grid(row=8, column=0, sticky="w", pady=(4, 0))

    def _on_formato_change(self, *a):
        self._update_option_visibility()

    def _update_option_visibility(self):
        sel = self.formato_seleccion_var.get()
        if not self.selected_empleado:
            self.chk_include_pago.grid_remove()
            self.text_desc.grid_remove()
            self.options_helper.configure(text="Seleccione un empleado para ver las opciones disponibles.")
            self._adjust_window_for_description(False)
            return

        self.options_helper.configure(text="")
        if sel == "Tabla de contratos":
            self.text_desc.grid_remove()
            self.chk_include_pago.grid()
            self.include_pago_var.set(True)
            self._adjust_window_for_description(False)
        else:
            self.chk_include_pago.grid_remove()
            self.text_desc.grid()
            try:
                self.text_desc.configure(state="normal")
            except Exception:
                pass
            self._adjust_window_for_description(True)

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
        show_table = selected_formato == "Tabla de contratos"
        include_pago = bool(self.include_pago_var.get()) and show_table

        if getattr(self, "_entry_other_rep", None) and self.representante_var.get() == "OTRO...":
            rep_text = self._entry_other_rep.get().strip()
            representante_final = rep_text if rep_text else "OTRO..."
            representante_titulo = self._rep_title_map.get("OTRO...", "Representante Legal")
        else:
            representante_final = self.representante_var.get()
            representante_titulo = self._rep_title_map.get(self.representante_var.get(), "Representante Legal")

        labores_desc = ""
        if not show_table:
            labores_desc = self.text_desc.get("1.0", "end").strip()

        emp_dict = emp if isinstance(emp, dict) else {k: v for k, v in emp.__dict__.items() if not k.startswith("_")}

        try:
            self.generar_cb(
                emp_dict,
                contratos,
                ruta,
                entidad_nombre="COLEGIO CIUDAD DE PIENDAMÓ",
                nit="NIT.817001256-7",
                representante=representante_final,
                representante_titulo=representante_titulo,
                fecha_expedicion=None,
                include_pago=include_pago,
                labores_descripcion=labores_desc,
                show_table=show_table,
            )
            messagebox.showinfo("Éxito", f"Reporte guardado en: {ruta}")
            self.ventana.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el PDF: {e}")
            return