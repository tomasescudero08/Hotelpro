"""
views/cliente_view.py
────────────────────────
VISTA de clientes. Solo widgets Tkinter — sin BD ni validaciones.
requerido --> pip install tkcalendar
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
from PIL import Image, ImageTk



FIELDS = [
    ("ID_cliente:", "ID_cliente"),
    ("nombre:", "nombre"),
    ("apellido:",  "apellido"),
    ("documento:",      "documento"),
    ("nacionalidad:", "nacionalidad"),
    ("fecha_nacimiento:",   "fecha_nacimiento"),
    ("direccion:",    "direccion"),
    ("telefono:",  "telefono"),
    ("correo:",  "correo"),
    ("nivel_fidelizacion:",   "nivel_fidelizacion")
]

TREE_COLUMNS = (('ID', 30), ('Nombre', 80), ('Apellido', 80), ('Documento', 100),
                 ('Nacionalidad', 100), ('fecha_nacimiento', 100), ('direccion', 70), ('telefono', 80), ('correo', 170), ('nivel_fidelizacion', 100))


class ClienteView(ttk.Frame):

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

        tk.Label(left, text="GESTIÓN DE CLIENTES",
                 font=("Arial", 14, "bold"), fg="#2196F3").pack(pady=15)

        form = tk.Frame(left)
        form.pack(padx=20)
        for i, (label, key) in enumerate(FIELDS):
            tk.Label(form, text=label, font=("Arial", 11)).grid(
                row=i, column=0, sticky="w", padx=(0, 8), pady=6)
            if key == "fecha_nacimiento":
                entry = DateEntry(
                    form,
                    width=19,
                    font=("Arial", 11),
                    date_pattern="yyyy-mm-dd"
                )
            else:
                entry = tk.Entry(
                    form,
                    width=22,
                    font=("Arial", 11),
                    relief="solid",
                    bd=1
                )
            entry.grid(row=i, column=1, sticky="w", pady=6)
            self.entries[key] = entry

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
            imagen = Image.open(r"C:\Users\Tomas Escudero\Desktop\images.png")
            imagen = imagen.resize((150, 100))

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
        tk.Label(right, text="LISTA DE CLIENTES",
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
    def get_form_data(self) -> dict:
        return {key: entry.get() for key, entry in self.entries.items()}

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


