"""
views/habitacion_view.py
────────────────────────
VISTA de Habitacion. Solo widgets Tkinter — sin BD ni validaciones.
"""

import os
import tkinter as tk
from tkinter import ttk, filedialog
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

TREE_COLUMNS = (
    ('ID', 40),
    ('numero_habitacion', 70),
    ('piso', 40),
    ('ID_tipo', 60),
    ('orientacion', 80),
    ('estado', 80),
    ('tarifa_base', 90),
    ('ID_hotel', 60),
    ('imagen', 80)
)


class HabitacionView(ttk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.entries = {}
        self.tipos = {}
        self.hoteles = {}

        self.imagen_path = None
        self.imagen_preview = None

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

        # ID_habitacion
        tk.Label(form, text="ID_habitacion:", font=("Arial", 11)).grid(row=0, column=0, sticky="w", padx=(0, 8), pady=4)
        e = tk.Entry(form, width=22, font=("Arial", 11), relief="solid", bd=1)
        e.grid(row=0, column=1, sticky="w", pady=4)
        self.entries["ID_habitacion"] = e

        # numero_habitacion
        tk.Label(form, text="numero_habitacion:", font=("Arial", 11)).grid(row=1, column=0, sticky="w", padx=(0, 8), pady=4)
        e = tk.Entry(form, width=22, font=("Arial", 11), relief="solid", bd=1)
        e.grid(row=1, column=1, sticky="w", pady=4)
        self.entries["numero_habitacion"] = e

        # piso
        tk.Label(form, text="piso:", font=("Arial", 11)).grid(row=2, column=0, sticky="w", padx=(0, 8), pady=4)
        e = tk.Entry(form, width=22, font=("Arial", 11), relief="solid", bd=1)
        e.grid(row=2, column=1, sticky="w", pady=4)
        self.entries["piso"] = e

        # TIPO DE HABITACIÓN
        tk.Label(form, text="Tipo de habitación:", font=("Arial", 11)).grid(row=3, column=0, sticky="w", padx=(0, 8), pady=4)
        self.combo_tipo = ttk.Combobox(form, width=20, state="readonly")
        self.combo_tipo.grid(row=3, column=1, sticky="w", pady=4)
        self.entries["ID_tipo"] = self.combo_tipo

        # ORIENTACIÓN
        tk.Label(form, text="orientacion:", font=("Arial", 11)).grid(row=4, column=0, sticky="w", padx=(0, 8), pady=4)
        self.combo_orientacion = ttk.Combobox(
            form, width=20, state="readonly", values=["Norte", "Sur", "Este", "Oeste"]
        )
        self.combo_orientacion.grid(row=4, column=1, sticky="w", pady=4)
        self.entries["orientacion"] = self.combo_orientacion

        # ESTADO
        tk.Label(form, text="estado:", font=("Arial", 11)).grid(row=5, column=0, sticky="w", padx=(0, 8), pady=4)
        self.combo_estado = ttk.Combobox(
            form, width=20, state="readonly", values=["Disponible", "Ocupada", "Mantenimiento"]
        )
        self.combo_estado.grid(row=5, column=1, sticky="w", pady=4)
        self.entries["estado"] = self.combo_estado

        # TARIFA BASE
        tk.Label(form, text="tarifa_base:", font=("Arial", 11)).grid(row=6, column=0, sticky="w", padx=(0, 8), pady=4)
        e = tk.Entry(form, width=22, font=("Arial", 11), relief="solid", bd=1)
        e.grid(row=6, column=1, sticky="w", pady=4)
        self.entries["tarifa_base"] = e

        # HOTEL
        tk.Label(form, text="Hotel:", font=("Arial", 11)).grid(row=7, column=0, sticky="w", padx=(0, 8), pady=4)
        self.combo_hotel = ttk.Combobox(form, width=20, state="readonly")
        self.combo_hotel.grid(row=7, column=1, sticky="w", pady=4)
        self.entries["ID_hotel"] = self.combo_hotel

        btns = tk.Frame(left)
        btns.pack(pady=(10, 0), anchor="w")
        for txt, color, cmd in [
            ("Guardar",    "#4CAF50", lambda: self.controller.guardar()),
            ("Actualizar", "#2196F3", lambda: self.controller.actualizar()),
            ("Eliminar",   "#f44336", lambda: self.controller.eliminar()),
            ("Buscar",     "#FF9800", lambda: self.controller.buscar()),
            ("Limpiar",    "#9E9E9E", lambda: self.controller.limpiar()),
        ]:
            tk.Button(btns, text=txt, font=("Arial", 9, "bold"),
                      bg=color, fg="white", width=9, command=cmd).pack(side="left", padx=2)

        tk.Button(
            left,
            text="Exportar",
            font=("Arial", 9, "bold"),
            bg="#607D8B",
            fg="white",
            width=9,
            command=self.controller.ventana_filtros_exportacion
        ).pack(anchor="w", padx=2, pady=(4, 8))

        # CONTROLES Y PREVISUALIZACIÓN DE IMAGEN
        self.btn_imagen = ttk.Button(
            left,
            text="Seleccionar imagen",
            command=self.seleccionar_imagen
        )
        self.btn_imagen.pack(anchor="w", padx=2, pady=(0, 5))

        self.frame_preview = tk.Frame(left, width=220, height=130, bd=1, relief="solid")
        self.frame_preview.pack_propagate(False)
        self.frame_preview.pack(pady=(2, 10))

        self.lbl_imagen = tk.Label(self.frame_preview, text="Sin imagen seleccionada")
        self.lbl_imagen.pack(fill="both", expand=True)

        right = tk.Frame(main)
        right.pack(side="right", fill="both", expand=True)
        tk.Label(right, text="LISTA DE HABITACIONES", font=("Arial", 12, "bold")).pack(pady=8)

        frame_tree = tk.Frame(right)
        frame_tree.pack(fill="both", expand=True, padx=10)

        cols = [c for c, _ in TREE_COLUMNS]
        self.tree = ttk.Treeview(frame_tree, columns=cols, show='headings', height=18)
        for col, width in TREE_COLUMNS:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor="center")

        scrollbar_y = ttk.Scrollbar(frame_tree, orient="vertical", command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(frame_tree, orient="horizontal", command=self.tree.xview)

        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")

        # EVENTOS DEL TREEVIEW
        self.tree.bind('<<TreeviewSelect>>', lambda e: self.controller.on_select(e))
        self.tree.bind('<ButtonRelease-1>', self._on_tree_click)
        self.tree.bind('<Double-1>', lambda e: self.controller.mostrar_imagen())

    # ── API usada por el controlador ──────────────────────────────────────────
    def get_form_data(self):
        data = {}

        for key, entry in self.entries.items():
            if key in ["ID_tipo", "ID_hotel", "orientacion", "estado"]:
                data[key] = entry.get()
            else:
                data[key] = entry.get()

        if self.combo_tipo.get():
            data["ID_tipo"] = self.tipos.get(self.combo_tipo.get(), self.combo_tipo.get())
        else:
            data["ID_tipo"] = None

        if self.combo_hotel.get():
            data["ID_hotel"] = self.hoteles.get(self.combo_hotel.get(), self.combo_hotel.get())
        else:
            data["ID_hotel"] = None

        data["imagen"] = self.imagen_path
        return data

    def set_form_data(self, values: dict):
        for key, entry in self.entries.items():
            if key in ["ID_tipo", "ID_hotel"]:
                continue
            entry.delete(0, tk.END)
            val = values.get(key)
            if val is not None:
                entry.insert(0, str(val))
        id_tipo = values.get("ID_tipo")
        if id_tipo is not None:
            for nombre, id_val in self.tipos.items():
                if str(id_val) == str(id_tipo) or nombre == str(id_tipo):
                    self.combo_tipo.set(nombre)
                    break

        id_hotel = values.get("ID_hotel")
        if id_hotel is not None:
            for nombre, id_val in self.hoteles.items():
                if str(id_val) == str(id_hotel) or nombre == str(id_hotel):
                    self.combo_hotel.set(nombre)
                    break

        ruta_img = values.get("imagen")
        self.imagen_path = ruta_img if (ruta_img and os.path.exists(str(ruta_img))) else None
        self.mostrar_imagen(self.imagen_path)

    def clear_form(self):
        for entry in self.entries.values():
            if isinstance(entry, ttk.Combobox):
                entry.set('')
            else:
                entry.delete(0, tk.END)

        self.imagen_path = None
        self.imagen_preview = None
        self.lbl_imagen.configure(image="", text="Sin imagen seleccionada")

    def _on_tree_click(self, event):
        region = self.tree.identify_region(event.x, event.y)
        if region == "cell":
            col = self.tree.identify_column(event.x)
            # Como la columna 'imagen' es la última (9a columna), corresponde a #9
            if col == f"#{len(TREE_COLUMNS)}":
                self.controller.mostrar_imagen()

    def set_tree_data(self, rows):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for row in rows:
            row_list = list(row)

            if len(row_list) >= 9:
                ruta = row_list[8]

                if ruta and str(ruta).strip() != "":
                    row_list[8] = "📷 Ver"
                else:
                    row_list[8] = "Sin foto"
            else:
                row_list.append("Sin foto")
            self.tree.insert('', 'end', values=row_list[:9])

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

    def seleccionar_imagen(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar imagen de habitación",
            filetypes=[
                ("Imágenes", "*.jpg *.jpeg *.png *.gif"),
                ("JPG", "*.jpg *.jpeg"),
                ("PNG", "*.png"),
                ("GIF", "*.gif")
            ]
        )

        if not ruta:
            return

        self.imagen_path = ruta
        self.mostrar_imagen(ruta)

    def mostrar_imagen(self, ruta):
        if not ruta or not os.path.exists(str(ruta)):
            self.lbl_imagen.configure(image="", text="Sin imagen seleccionada")
            self.imagen_preview = None
            return

        try:
            imagen = Image.open(ruta)
            imagen.thumbnail((200, 120), Image.Resampling.LANCZOS)
            self.imagen_preview = ImageTk.PhotoImage(imagen)

            self.lbl_imagen.configure(image=self.imagen_preview, text="")
        except Exception as e:
            self.lbl_imagen.configure(image="", text="Error al cargar")
            self.imagen_preview = None