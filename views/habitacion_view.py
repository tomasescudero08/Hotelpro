"""
views/habitacion_view.py
────────────────────────
VISTA de Habitacion. Solo widgets Tkinter — sin BD ni validaciones.
"""

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

FIELDS = [
    ("ID_habitacion:", "ID_habitacion"),
    ("numero_habitacion:",   "numero_habitacion"),
    ("piso:",  "piso"),
    ("ID_tipo:", "ID_tipo"),
    ("orientacion:", "orientacion"),
    ("estado:", "estado"),
    ("tarifa_base:", "tarifa_base"),
    ("ID_hotel:", "ID_hotel")
]

TREE_COLUMNS = (('ID', 40), ('numero_habitacion', 60), ('piso', 40),
                 ('ID_tipo', 40), ('orientacion', 80), ('estado', 80), ('tarifa_base',100), ('ID_hotel', 40))


class HabitacionView(ttk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.entries = {}
        self._crear_widgets()

    def _crear_widgets(self):
        main = tk.Frame(self)
        main.pack(fill="both", expand=True, padx=10, pady=10)

        left = tk.Frame(main)
        left.pack(side="left", fill="y", padx=(0, 10))

        tk.Label(left, text="GESTIÓN DE HABITACIONES",
                 font=("Arial", 14, "bold"), fg="#f44336").pack(pady=15)

        form = tk.Frame(left)
        form.pack(padx=20)
        tk.Label(
            form,
            text="ID_habitacion:",
            font=("Arial", 11)
        ).grid(row=0, column=0, sticky="w", padx=(0, 8), pady=6)

        e = tk.Entry(
            form,
            width=22,
            font=("Arial", 11),
            relief="solid",
            bd=1
        )
        e.grid(row=0, column=1, sticky="w", pady=6)
        self.entries["ID_habitacion"] = e
        # numero_habitacion
        tk.Label(
            form,
            text="numero_habitacion:",
            font=("Arial", 11)
        ).grid(row=1, column=0, sticky="w", padx=(0, 8), pady=6)

        e = tk.Entry(
            form,
            width=22,
            font=("Arial", 11),
            relief="solid",
            bd=1
        )
        e.grid(row=1, column=1, sticky="w", pady=6)
        self.entries["numero_habitacion"] = e

        # piso
        tk.Label(
            form,
            text="piso:",
            font=("Arial", 11)
        ).grid(row=2, column=0, sticky="w", padx=(0, 8), pady=6)

        e = tk.Entry(
            form,
            width=22,
            font=("Arial", 11),
            relief="solid",
            bd=1
        )
        e.grid(row=2, column=1, sticky="w", pady=6)
        self.entries["piso"] = e

        # TIPO DE HABITACIÓN
        tk.Label(
            form,
            text="Tipo de habitación:",
            font=("Arial", 11)
        ).grid(row=3, column=0, sticky="w", padx=(0, 8), pady=6)

        self.combo_tipo = ttk.Combobox(
            form,
            width=20,
            state="readonly"
        )

        self.combo_tipo.grid(
            row=3,
            column=1,
            sticky="w",
            pady=6
        )

        self.entries["ID_tipo"] = self.combo_tipo

        # ORIENTACIÓN
        tk.Label(
            form,
            text="orientacion:",
            font=("Arial", 11)
        ).grid(row=4, column=0, sticky="w", padx=(0, 8), pady=6)

        self.combo_orientacion = ttk.Combobox(
            form,
            width=20,
            state="readonly",
            values=["Norte", "Sur", "Este", "Oeste"]
        )
        self.combo_orientacion.grid(
            row=4,
            column=1,
            sticky="w",
            pady=6
        )
        self.entries["orientacion"] = self.combo_orientacion

        # ESTADO
        tk.Label(
            form,
            text="estado:",
            font=("Arial", 11)
        ).grid(row=5, column=0, sticky="w", padx=(0, 8), pady=6)

        self.combo_estado = ttk.Combobox(
            form,
            width=20,
            state="readonly",
            values=["Disponible", "Ocupada", "Mantenimiento"]
        )
        self.combo_estado.grid(
            row=5,
            column=1,
            sticky="w",
            pady=6
        )
        self.entries["estado"] = self.combo_estado

        # TARIFA BASE
        tk.Label(
            form,
            text="tarifa_base:",
            font=("Arial", 11)
        ).grid(row=6, column=0, sticky="w", padx=(0, 8), pady=6)

        e = tk.Entry(
            form,
            width=22,
            font=("Arial", 11),
            relief="solid",
            bd=1
        )
        e.grid(row=6, column=1, sticky="w", pady=6)
        self.entries["tarifa_base"] = e

        # HOTEL
        tk.Label(
            form,
            text="Hotel:",
            font=("Arial", 11)
        ).grid(row=7, column=0, sticky="w", padx=(0, 8), pady=6)

        self.combo_hotel = ttk.Combobox(
            form,
            width=20,
            state="readonly"
        )

        self.combo_hotel.grid(
            row=7,
            column=1,
            sticky="w",
            pady=6
        )

        self.entries["ID_hotel"] = self.combo_hotel

        btns = tk.Frame(left)
        btns.pack(pady=(12, 0), anchor="w")
        for txt, color, cmd in [
            ("Guardar",    "#4CAF50", lambda: self.controller.guardar()),
            ("Actualizar", "#2196F3", lambda: self.controller.actualizar()),
            ("Eliminar",   "#f44336", lambda: self.controller.eliminar()),
            ("Buscar",     "#FF9800", lambda: self.controller.buscar()),
            ("Limpiar",    "#9E9E9E", lambda: self.controller.limpiar()),
        ]:
            tk.Button(btns, text=txt, font=("Arial", 9, "bold"),
                      bg=color, fg="white", width=9, command=cmd).pack(side="left", padx=2)

        # Exportar queda debajo de Guardar para reducir el ancho del panel izquierdo.
        tk.Button(
            left,
            text="Exportar",
            font=("Arial", 9, "bold"),
            bg="#607D8B",
            fg="white",
            width=9,
            command=self.controller.ventana_filtros_exportacion
        ).pack(anchor="w", padx=2, pady=(4, 12))
        try:
            imagen = Image.open(r"C:\Users\Tomas Escudero\Desktop\caption.png")
            imagen = imagen.resize((350, 300))

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
        tk.Label(right, text="LISTA DE HABITACIONES",
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
        data = {}

        for key, entry in self.entries.items():
            data[key] = entry.get()

        if self.combo_tipo.get():
            data["ID_tipo"] = self.tipos[self.combo_tipo.get()]
        else:
            data["ID_tipo"] = None

        if self.combo_hotel.get():
            data["ID_hotel"] = self.hoteles[self.combo_hotel.get()]
        else:
            data["ID_hotel"] = None

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

    def set_hoteles(self, hoteles):
        self.hoteles = {}

        nombres = []

        for ID_hotel, nombre in hoteles:
            self.hoteles[nombre] = ID_hotel
            nombres.append(nombre)

        self.combo_hotel["values"] = nombres

    def set_tipos(self, tipos):
        self.tipos = {}

        nombres = []

        for ID_tipo, nombre in tipos:
            self.tipos[nombre] = ID_tipo
            nombres.append(nombre)

        self.combo_tipo["values"] = nombres