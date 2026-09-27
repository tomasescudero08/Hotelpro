"""
views/tarifa_view.py
────────────────────────
VISTA de Tarifa. Solo widgets Tkinter — sin BD ni validaciones.
Usa DateEntry (tkcalendar) para BirthDate, igual que 03_GUI_DB/03_crud_empleados_sp.py.
"""

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

FIELDS = [
    ("ID_tarifa:", "ID_tarifa"),
    ("ID_tipo:",   "ID_tipo"),
    ("tarifa_base:",  "tarifa_base"),
    ("impuestos:", "impuestos"),
    ("descuento:", "descuento"),
    ("condiciones:", "condiciones")
]

TREE_COLUMNS = (('ID', 40), ('ID_tipo', 40), ('tarifa_base', 40),
                 ('impuestos', 40), ('descuento', 80), ('condiciones', 80))


class TarifaView(ttk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.entries = {}
        self.tipos = {}
        self._crear_widgets()


    def _crear_widgets(self):
        main = tk.Frame(self)
        main.pack(fill="both", expand=True, padx=10, pady=10)

        left = tk.Frame(main)
        left.pack(side="left", fill="y", padx=(0, 10))

        tk.Label(left, text="GESTIÓN DE TARIFAS",
                 font=("Arial", 14, "bold"), fg="#f44336").pack(pady=15)

        form = tk.Frame(left)
        form.pack(padx=20)

        tk.Label(form, text="ID_tarifa:", font=("Arial", 11)).grid(
            row=0, column=0, sticky="w", padx=(0, 8), pady=6)
        e = tk.Entry(form, width=22, font=("Arial", 11), relief="solid", bd=1)
        e.grid(row=0, column=1, sticky="w", pady=6)
        self.entries["ID_tarifa"] = e

        tk.Label(
            form,
            text="ID_tipo:",
            font=("Arial", 11)
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=(0, 8),
            pady=6
        )

        self.combo_tipo = ttk.Combobox(
            form,
            width=20,
            state="readonly"
        )

        self.combo_tipo.grid(
            row=1,
            column=1,
            sticky="w",
            pady=6
        )

        self.entries["ID_tipo"] = self.combo_tipo

        tk.Label(form, text="tarifa_base:", font=("Arial", 11)).grid(
            row=2, column=0, sticky="w", padx=(0, 8), pady=6)
        e = tk.Entry(form, width=22, font=("Arial", 11), relief="solid", bd=1)
        e.grid(row=2, column=1, sticky="w", pady=6)
        self.entries["tarifa_base"] = e

        tk.Label(form, text="impuestos:", font=("Arial", 11)).grid(
            row=3, column=0, sticky="w", padx=(0, 8), pady=6)
        e = tk.Entry(form, width=22, font=("Arial", 11), relief="solid", bd=1)
        e.grid(row=3, column=1, sticky="w", pady=6)
        self.entries["impuestos"] = e

        tk.Label(form, text="descuento:", font=("Arial", 11)).grid(
            row=4, column=0, sticky="w", padx=(0, 8), pady=6)
        e = tk.Entry(form, width=22, font=("Arial", 11), relief="solid", bd=1)
        e.grid(row=4, column=1, sticky="w", pady=6)
        self.entries["descuento"] = e

        tk.Label(form, text="condiciones:", font=("Arial", 11)).grid(
            row=5, column=0, sticky="w", padx=(0, 8), pady=6)
        e = tk.Entry(form, width=22, font=("Arial", 11), relief="solid", bd=1)
        e.grid(row=5, column=1, sticky="w", pady=6)
        self.entries["condiciones"] = e

        btns = tk.Frame(left)
        btns.pack(pady=12)
        for txt, color, cmd in [
            ("Guardar",    "#4CAF50", lambda: self.controller.guardar()),
            ("Actualizar", "#2196F3", lambda: self.controller.actualizar()),
            ("Eliminar",   "#f44336", lambda: self.controller.eliminar()),
            ("Buscar",     "#FF9800", lambda: self.controller.buscar()),
            ("Limpiar",    "#9E9E9E", lambda: self.controller.limpiar()),
            ("Excel", "#4CAF50", lambda: self.controller.exportar_excel()),
            ("PDF", "#F44336", lambda: self.controller.exportar_pdf()),
        ]:
            tk.Button(btns, text=txt, font=("Arial", 9, "bold"),
                      bg=color, fg="white", width=9, command=cmd).pack(side="left", padx=2)

        try:
            imagen = Image.open(r"C:\Users\Tomas Escudero\Desktop\tarifas.png")
            imagen = imagen.resize((250, 200))

            self.imagen_habitacion = ImageTk.PhotoImage(imagen)

            self.label_imagen = tk.Label(
                left,
                image=self.imagen_habitacion,
                bg="#F5F5F5"
            )

            self.label_imagen.pack(
                pady=(15, 0)
            )

        except Exception as e:
            print("No se pudo cargar la imagen:", e)

        right = tk.Frame(main)
        right.pack(side="right", fill="both", expand=True)
        tk.Label(right, text="LISTA DE TARIFAS",
                 font=("Arial", 12, "bold")).pack(pady=8)

        frame_tree = tk.Frame(right)
        frame_tree.pack(fill="both", expand=True, padx=10)

        cols = [c for c, _ in TREE_COLUMNS]
        self.tree = ttk.Treeview(frame_tree, columns=cols, show='headings', height=18)
        for col, width in TREE_COLUMNS:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width)

        scrollbar = ttk.Scrollbar(frame_tree, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.tree.bind('<<TreeviewSelect>>', lambda e: self.controller.on_select(e))

    # ── API usada por el controlador ──────────────────────────────────────────
    def get_form_data(self):

        data = {
            key: entry.get()
            for key, entry in self.entries.items()
        }

        if self.combo_tipo.get():
            data["ID_tipo"] = self.tipos[self.combo_tipo.get()]
        else:
            data["ID_tipo"] = None

        return data

    def set_form_data(self, values: dict):
        for key, entry in self.entries.items():
            entry.delete(0, tk.END)
            val = values.get(key)
            if val is not None:
                entry.insert(0, str(val))

    def clear_form(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def set_tree_data(self, rows):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for row in rows:
            self.tree.insert('', 'end', values=row)

    def get_selected_tree_values(self):
        selection = self.tree.selection()
        if not selection:
            return None
        return self.tree.item(selection[0])['values']

    def set_tipos(self, tipos):

        self.tipos = {}

        nombres = []

        for ID_tipo, nombre in tipos:
            self.tipos[nombre] = ID_tipo
            nombres.append(nombre)

        self.combo_tipo["values"] = nombres