"""
views/cliente_view.py
────────────────────────
VISTA de clientes.
"""

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
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

TREE_COLUMNS = (
    ('ID', 30),
    ('Nombre', 80),
    ('Apellido', 80),
    ('Documento', 100),
    ('Nacionalidad', 100),
    ('fecha_nacimiento', 100),
    ('direccion', 70),
    ('telefono', 80),
    ('correo', 170),
    ('nivel_fidelizacion', 100),
    ('imagen', 80)
)


class ClienteView(ttk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller
        self.entries = {}

        self.imagen_path = None
        self.imagen_preview = None

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

        tk.Button(
            left,
            text="Exportar",
            font=("Arial", 9, "bold"),
            bg="#607D8B",
            fg="white",
            width=9,
            command=self.controller.ventana_filtros_exportacion
        ).pack(anchor="w", padx=2, pady=(4, 12))

        self.btn_imagen = ttk.Button(
            left,
            text="Seleccionar imagen",
            command=self.seleccionar_imagen
        )
        self.btn_imagen.pack(anchor="w", padx=2, pady=(0, 5))

        # CORRECCIÓN EN EL LABEL: Usar Frame contenedor con tamaño fijo en píxeles
        self.frame_preview = tk.Frame(left, width=220, height=150, bd=1, relief="solid")
        self.frame_preview.pack_propagate(False)
        self.frame_preview.pack(pady=(5, 10))

        self.lbl_imagen = tk.Label(self.frame_preview, text="Sin imagen seleccionada")
        self.lbl_imagen.pack(fill="both", expand=True)

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
            self.tree.column(col, width=width, anchor="center")

        scrollbar_y = ttk.Scrollbar(frame_tree, orient="vertical", command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(frame_tree, orient="horizontal", command=self.tree.xview)

        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")

        # EVENTOS DEL TREEVIEW
        self.tree.bind('<<TreeviewSelect>>', lambda e: self.controller.on_select(e))
        # Clic o doble clic abre la ventana emergente con la imagen
        self.tree.bind('<ButtonRelease-1>', self._on_tree_click)
        self.tree.bind('<Double-1>', lambda e: self.controller.mostrar_imagen())

    def _on_tree_click(self, event):
        """Detecta si se hizo clic explícito en la columna 'imagen'."""
        region = self.tree.identify_region(event.x, event.y)
        if region == "cell":
            col = self.tree.identify_column(event.x)
            # La columna 11 corresponde a 'imagen'
            if col == "#11":
                self.controller.mostrar_imagen()

    # ── API usada por el controlador ──────────────────────────────────────────
    def get_form_data(self) -> dict:
        data = {
            key: entry.get()
            for key, entry in self.entries.items()
        }

        data["imagen"] = self.imagen_path
        return data

    def set_form_data(self, values: dict):
        for key, entry in self.entries.items():
            entry.delete(0, tk.END)
            val = values.get(key)
            if val is not None:
                entry.insert(0, str(val))

        # CORRECCIÓN: Mantener la ruta original en la variable interna
        ruta_img = values.get("imagen")
        self.imagen_path = ruta_img if (ruta_img and os.path.exists(str(ruta_img))) else None
        self.mostrar_imagen(self.imagen_path)

    def clear_form(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

        self.imagen_path = None
        self.imagen_preview = None

        self.lbl_imagen.configure(
            image="",
            text="Sin imagen seleccionada"
        )

    def set_tree_data(self, rows):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for row in rows:
            row_list = list(row)
            if len(row_list) > 10 and row_list[10]:
                ruta = str(row_list[10])
                row_list[10] = "📷 Ver" if os.path.exists(ruta) else "Sin foto"
            else:
                if len(row_list) <= 10:
                    row_list.append("Sin foto")
                else:
                    row_list[10] = "Sin foto"

            self.tree.insert('', 'end', values=row_list)

    def get_selected_tree_values(self):
        selection = self.tree.selection()
        if not selection:
            return None
        return self.tree.item(selection[0])['values']

    def seleccionar_imagen(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar imagen",
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
            self.lbl_imagen.configure(
                image="",
                text="Sin imagen seleccionada"
            )
            self.imagen_preview = None
            return

        try:
            imagen = Image.open(ruta)
            # Redimensionar al área del contenedor (200x130 píxeles)
            imagen.thumbnail((200, 130), Image.Resampling.LANCZOS)

            self.imagen_preview = ImageTk.PhotoImage(imagen)

            self.lbl_imagen.configure(
                image=self.imagen_preview,
                text=""
            )

        except Exception as e:
            self.lbl_imagen.configure(
                image="",
                text="Error al cargar"
            )
            self.imagen_preview = None