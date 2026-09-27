"""
controllers/main_controller.py
─────────────────────────────────
CONTROLADOR principal: crea la conexión a BD, la ventana principal y
un controlador por cada pestaña/entidad (Products, Customers, Employees).
"""

from tkinter import messagebox

from models.database import DatabaseConnector
from views.main_view import MainView
from controllers.cliente_controller import  ClienteController
from controllers.habitacion_controller import HabitacionController
from controllers.reserva_controller import ReservaController
from controllers.tarifa_controller import TarifaController

class MainController:

    def __init__(self, db_config: dict):
        self.db = DatabaseConnector(db_config)
        self.view = MainView()

        ok, err = self.db.connect()
        if not ok:
            messagebox.showerror("Error de Conexión",
                                  f"No se pudo conectar a la base de datos:\n{err}")
            self.view.destroy()
            raise SystemExit(1)

        self.cliente_controller  = ClienteController(self.view.tab_cliente, self.db)
        self.habitacion_controller = HabitacionController(self.view.tab_habitacion, self.db)
        self.reserva_controller = ReservaController(self.view.tab_reserva, self.db)
        self.tarifa_controller = TarifaController(self.view.tab_tarifa, self.db)

        self.view.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        self.db.disconnect()
        self.view.destroy()

    def run(self):
        self.view.mainloop()