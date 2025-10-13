import customtkinter as ctk
import tkinter as tk
from tkinter import ttk

class ModalHistorialPagos(ctk.CTkToplevel):
    def __init__(self, parent, title="Historial de pagos", headers=None, rows=None, width=800, height=400):
        super().__init__(parent)
        self.title(title)
        self.geometry(f"{width}x{height}")
        self.transient(parent)
        self.grab_set()

        headers = headers or []
        rows = rows or []

        frame = ctk.CTkFrame(self)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # contenedor para Treeview + scrollbars
        container = tk.Frame(frame)
        container.pack(fill="both", expand=True)
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        self.tree = ttk.Treeview(container, columns=[str(i) for i in range(len(headers))], show="headings")
        vsb = ttk.Scrollbar(container, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(container, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, columnspan=2, sticky="ew")

        for i, h in enumerate(headers):
            self.tree.heading(str(i), text=h)
            self.tree.column(str(i), width=160, anchor="w", stretch=True)

        for r in rows:
            vals = r if isinstance(r, (list, tuple)) else list(r)
            self.tree.insert("", "end", values=vals)

        btn_close = ctk.CTkButton(self, text="Cerrar", command=self.close)
        btn_close.pack(pady=8)

    def close(self):
        self.grab_release()
        self.destroy()