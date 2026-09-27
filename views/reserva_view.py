"""
views/cliente_view.py
────────────────────────
VISTA de reserva. Solo widgets Tkinter — sin BD ni validaciones.
requerido --> pip install tkcalendar
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry

FIELDS = [
    ("ID_reserva:",   "ID_reserva"),
    ("fecha_creacion:", "fecha_creacion"),
    ("ID_cliente:",  "ID_cliente"),
    ("fecha_llegada:",      "fecha_llegada"),
    ("fecha_salida:", "fecha_salida"),
    ("num_habitaciones:",   "num_habitaciones"),
    ("ID_tipo:",    "ID_tipo"),
    ("adultos:",  "adultos"),
    ("ninos:",  "ninos"),
    ("tarifa_aplicada:",   "tarifa_aplicada"),
    ("deposito:",   "deposito"),
    ("metodo_pago:",   "metodo_pago"),
    ("estado:",   "estado")
]

TREE_COLUMNS = (('ID', 40), ('fecha_creacion', 100), ('ID_cliente', 60), ('fecha_llegada', 100),
                 ('fecha_salida', 100), ('num_habitaciones', 60), ('ID_tipo', 60), ('adultos', 60), ('niños', 50), ('tarifa_aplicada', 80),('deposito', 80), ('metodo_pago', 80), ('estado', 80))


class ReservaView(ttk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller
        self.entries = {}

        self.clientes = {}
        self.tipos = {}

        self._crear_widgets()

    def set_tipos(self, tipos):

        self.tipos = {}

        nombres = []

        for tipo in tipos:
            ID_tipo = tipo[0]
            nombre = tipo[1]

            self.tipos[nombre] = ID_tipo
            nombres.append(nombre)

        self.entries["ID_tipo"]["values"] = nombres

    def _crear_widgets(self):
        main = tk.Frame(self)
        main.pack(fill="both", expand=True, padx=10, pady=10)

        left = tk.Frame(main)
        left.pack(side="left", fill="y", padx=(0, 10))

        tk.Label(left, text="GESTIÓN DE RESERVAS",
                 font=("Arial", 14, "bold"), fg="#2196F3").pack(pady=15)

        form = tk.Frame(left)
        form.pack(padx=20)
        for i, (label, key) in enumerate(FIELDS):

            tk.Label(
                form,
                text=label,
                font=("Arial", 11)
            ).grid(
                row=i,
                column=0,
                sticky="w",
                padx=(0, 8),
                pady=6
            )

            if key in ("fecha_creacion", "fecha_llegada", "fecha_salida"):

                entry = DateEntry(
                    form,
                    width=19,
                    font=("Arial", 11),
                    date_pattern="yyyy-mm-dd"
                )

            elif key == "ID_cliente":

                entry = ttk.Combobox(
                    form,
                    width=20,
                    state="readonly"
                )

            elif key == "ID_tipo":

                entry = ttk.Combobox(
                    form,
                    width=20,
                    state="readonly"
                )

            elif key == "metodo_pago":

                entry = ttk.Combobox(
                    form,
                    width=20,
                    state="readonly",
                    values=[
                        "Efectivo",
                        "Tarjeta",
                        "Transferencia"
                    ]
                )

            elif key == "estado":

                entry = ttk.Combobox(
                    form,
                    width=20,
                    state="readonly",
                    values=[
                        "Pendiente",
                        "Confirmada",
                        "Cancelada",
                        "Finalizada"
                    ]
                )

            else:

                entry = tk.Entry(
                    form,
                    width=22,
                    font=("Arial", 11),
                    relief="solid",
                    bd=1
                )

            entry.grid(
                row=i,
                column=1,
                sticky="w",
                pady=6
            )

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

        right = tk.Frame(main)
        right.pack(side="right", fill="both", expand=True)
        tk.Label(right, text="LISTA DE RESERVAS",
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

        cliente_seleccionado = self.entries["ID_cliente"].get()

        if cliente_seleccionado:
            data["ID_cliente"] = self.clientes.get(
                cliente_seleccionado
            )
        else:
            data["ID_cliente"] = None

        tipo_seleccionado = self.entries["ID_tipo"].get()

        if tipo_seleccionado:
            data["ID_tipo"] = self.tipos.get(
                tipo_seleccionado
            )
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

    def set_clientes(self, clientes):

        self.clientes = {}

        nombres = []

        for cliente in clientes:
            ID_cliente = cliente[0]
            nombre = cliente[1]
            apellido = cliente[2]

            nombre_completo = f"{nombre} {apellido}"

            self.clientes[nombre_completo] = ID_cliente
            nombres.append(nombre_completo)

        self.entries["ID_cliente"]["values"] = nombres

    def ventana_filtros_exportacion(self):

        ventana = tk.Toplevel(self)
        ventana.title("Filtros de exportación")
        ventana.geometry("400x350")
        ventana.resizable(False, False)

        tk.Label(
            ventana,
            text="FILTROS DE EXPORTACIÓN",
            font=("Arial", 14, "bold")
        ).pack(pady=15)

        form = tk.Frame(ventana)
        form.pack(padx=20, pady=10)


        tk.Label(
            form,
            text="Fecha desde:"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=5,
            pady=8
        )

        fecha_desde = DateEntry(
            form,
            width=18,
            date_pattern="yyyy-mm-dd"
        )

        fecha_desde.grid(
            row=0,
            column=1,
            padx=5,
            pady=8
        )


        tk.Label(
            form,
            text="Fecha hasta:"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=5,
            pady=8
        )

        fecha_hasta = DateEntry(
            form,
            width=18,
            date_pattern="yyyy-mm-dd"
        )

        fecha_hasta.grid(
            row=1,
            column=1,
            padx=5,
            pady=8
        )


        tk.Label(
            form,
            text="Estado:"
        ).grid(
            row=2,
            column=0,
            sticky="w",
            padx=5,
            pady=8
        )

        combo_estado = ttk.Combobox(
            form,
            width=20,
            state="readonly",
            values=[
                "Todos",
                "Pendiente",
                "Confirmada",
                "Cancelada",
                "Finalizada"
            ]
        )

        combo_estado.current(0)

        combo_estado.grid(
            row=2,
            column=1,
            padx=5,
            pady=8
        )

        tk.Label(
            form,
            text="Método de pago:"
        ).grid(
            row=3,
            column=0,
            sticky="w",
            padx=5,
            pady=8
        )

        combo_pago = ttk.Combobox(
            form,
            width=20,
            state="readonly",
            values=[
                "Todos",
                "Efectivo",
                "Tarjeta",
                "Transferencia"
            ]
        )

        combo_pago.current(0)

        combo_pago.grid(
            row=3,
            column=1,
            padx=5,
            pady=8
        )

        botones = tk.Frame(ventana)
        botones.pack(pady=20)

        tk.Button(
            botones,
            text="Exportar Excel",
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            command=lambda: self.controller.exportar_excel_filtrado(
                fecha_desde.get(),
                fecha_hasta.get(),
                combo_estado.get(),
                combo_pago.get(),
                ventana
            )
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            botones,
            text="Exportar PDF",
            bg="#F44336",
            fg="white",
            font=("Arial", 10, "bold"),
            command=lambda: self.controller.exportar_pdf_filtrado(
                fecha_desde.get(),
                fecha_hasta.get(),
                combo_estado.get(),
                combo_pago.get(),
                ventana
            )
        ).pack(
            side="left",
            padx=5
        )