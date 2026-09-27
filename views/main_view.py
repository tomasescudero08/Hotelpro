"""
views/main_view.py
────────────────────
VISTA principal: ventana raíz + Notebook con una pestaña por entidad.
Solo construye el "esqueleto" (root + tabs); cada controlador de entidad
instala su propia vista dentro de la pestaña correspondiente.
"""

import tkinter as tk
from tkinter import ttk


class MainView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("— HOTELPRO CRUD (MVC)")
        self.geometry('1200x700')
        self.resizable(True, True)
        self.iconbitmap('C:/Users/Tomas Escudero/Desktop/favicon.ico')


        self.notebook = ttk.Notebook(self)
        self.tab_cliente  = ttk.Frame(self.notebook)
        self.tab_habitacion = ttk.Frame(self.notebook)
        self.tab_reserva = ttk.Frame(self.notebook)
        self.tab_tarifa = ttk.Frame(self.notebook)


        self.notebook.add(self.tab_cliente,  text="  Clientes  ")
        self.notebook.add(self.tab_habitacion, text="  Habitaciones")
        self.notebook.add(self.tab_reserva, text="  Reservas ")
        self.notebook.add(self.tab_tarifa, text="  Tarifas ")
        self.notebook.pack(expand=True, fill="both")