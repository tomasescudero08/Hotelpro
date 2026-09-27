"""Ventanas modales para configurar filtros antes de exportar."""

import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry


class _VentanaFiltroBase(tk.Toplevel):
    def __init__(self, parent, formato, callback_exportar, titulo, geometry="420x300"):
        super().__init__(parent)
        self.title(f"Filtros de exportación - {formato.upper()}")
        self.geometry(geometry)
        self.resizable(False, False)
        self.grab_set()

        self.formato = formato
        self.callback_exportar = callback_exportar

        tk.Label(
            self,
            text=titulo,
            font=("Arial", 14, "bold")
        ).pack(pady=15)

        self.form = tk.Frame(self)
        self.form.pack(padx=20, pady=5, fill="x")

    def _fecha(self, fila, texto):
        ttk.Label(self.form, text=texto).grid(
            row=fila, column=0, sticky="w", padx=5, pady=7
        )
        entry = DateEntry(
            self.form,
            width=18,
            date_pattern="yyyy-mm-dd"
        )
        entry.grid(row=fila, column=1, padx=5, pady=7)
        return entry

    def _combo(self, fila, texto, valores):
        ttk.Label(self.form, text=texto).grid(
            row=fila, column=0, sticky="w", padx=5, pady=7
        )
        combo = ttk.Combobox(
            self.form,
            width=20,
            state="readonly",
            values=["Todos"] + list(valores)
        )
        combo.current(0)
        combo.grid(row=fila, column=1, padx=5, pady=7)
        return combo

    def _botones(self):
        botones = tk.Frame(self)
        botones.pack(pady=18)

        tk.Button(
            botones,
            text="Exportar Excel",
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            command=lambda: self._confirmar("excel")
        ).pack(side="left", padx=5)

        tk.Button(
            botones,
            text="Exportar PDF",
            bg="#F44336",
            fg="white",
            font=("Arial", 10, "bold"),
            command=lambda: self._confirmar("pdf")
        ).pack(side="left", padx=5)

    def _confirmar(self, formato):
        filtros = self.obtener_filtros()
        self.callback_exportar(formato, filtros, self)


class VentanaFiltroCliente(_VentanaFiltroBase):
    def __init__(self, parent, callback_exportar, nacionalidades, niveles):
        super().__init__(
            parent,
            "excel/pdf",
            callback_exportar,
            "FILTROS DE EXPORTACIÓN DE CLIENTES",
            geometry="430x340"
        )

        self.usar_fecha = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            self.form,
            text="Aplicar filtro por fecha",
            variable=self.usar_fecha
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=5, pady=(0, 5))

        self.fecha_desde = self._fecha(1, "Fecha nacimiento desde:")
        self.fecha_hasta = self._fecha(2, "Fecha nacimiento hasta:")
        self.nacionalidad = self._combo(3, "Nacionalidad:", nacionalidades)
        self.nivel = self._combo(4, "Nivel de fidelización:", niveles)
        self._botones()

    def _confirmar(self, formato):
        filtros = self.obtener_filtros()
        filtros["formato"] = formato
        self.callback_exportar(formato, filtros, self)

    def obtener_filtros(self):
        return {
            "fecha_desde": self.fecha_desde.get() if self.usar_fecha.get() else None,
            "fecha_hasta": self.fecha_hasta.get() if self.usar_fecha.get() else None,
            "nacionalidad": self.nacionalidad.get(),
            "nivel_fidelizacion": self.nivel.get(),
        }


class VentanaFiltroHabitacion(_VentanaFiltroBase):
    def __init__(self, parent, callback_exportar, tipos, hoteles):
        super().__init__(
            parent,
            "excel/pdf",
            callback_exportar,
            "FILTROS DE EXPORTACIÓN DE HABITACIONES",
            geometry="430x400"
        )

        self.estado = self._combo(
            0,
            "Estado:",
            ["Disponible", "Ocupada", "Mantenimiento"]
        )
        self.tipo = self._combo(1, "Tipo de habitación:", tipos)
        self.hotel = self._combo(2, "Hotel:", hoteles)

        ttk.Label(self.form, text="Tarifa desde:").grid(
            row=3, column=0, sticky="w", padx=5, pady=7
        )
        self.tarifa_desde = ttk.Entry(self.form, width=22)
        self.tarifa_desde.grid(row=3, column=1, padx=5, pady=7)

        ttk.Label(self.form, text="Tarifa hasta:").grid(
            row=4, column=0, sticky="w", padx=5, pady=7
        )
        self.tarifa_hasta = ttk.Entry(self.form, width=22)
        self.tarifa_hasta.grid(row=4, column=1, padx=5, pady=7)

        self._botones()

    def obtener_filtros(self):
        return {
            "estado": self.estado.get(),
            "tipo": self.tipo.get(),
            "hotel": self.hotel.get(),
            "tarifa_desde": self.tarifa_desde.get().strip(),
            "tarifa_hasta": self.tarifa_hasta.get().strip(),
        }


class VentanaFiltroTarifa(_VentanaFiltroBase):
    def __init__(self, parent, callback_exportar, tipos):
        super().__init__(
            parent,
            "excel/pdf",
            callback_exportar,
            "FILTROS DE EXPORTACIÓN DE TARIFAS",
            geometry="430x350"
        )

        self.usar_fecha = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            self.form,
            text="Aplicar filtro por fecha",
            variable=self.usar_fecha
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=5, pady=(0, 5))

        self.fecha_desde = self._fecha(1, "Fecha desde:")
        self.fecha_hasta = self._fecha(2, "Fecha hasta:")
        self.tipo = self._combo(3, "Tipo de habitación:", tipos)

        ttk.Label(self.form, text="Precio desde:").grid(
            row=4, column=0, sticky="w", padx=5, pady=7
        )
        self.precio_desde = ttk.Entry(self.form, width=22)
        self.precio_desde.grid(row=4, column=1, padx=5, pady=7)

        ttk.Label(self.form, text="Precio hasta:").grid(
            row=5, column=0, sticky="w", padx=5, pady=7
        )
        self.precio_hasta = ttk.Entry(self.form, width=22)
        self.precio_hasta.grid(row=5, column=1, padx=5, pady=7)

        self._botones()

    def obtener_filtros(self):
        return {
            "fecha_desde": self.fecha_desde.get() if self.usar_fecha.get() else None,
            "fecha_hasta": self.fecha_hasta.get() if self.usar_fecha.get() else None,
            "tipo": self.tipo.get(),
            "precio_desde": self.precio_desde.get().strip(),
            "precio_hasta": self.precio_hasta.get().strip(),
        }
