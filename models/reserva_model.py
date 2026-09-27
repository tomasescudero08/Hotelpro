"""
models/habitacion_model.py
─────────────────────────
MODELO de Reserva. Traduce operaciones de negocio a llamadas de
Stored Procedures (sp_InsertReserva, sp_UpdateReserva, sp_DeleteReserva,
sp_GetReserva, sp_GetAllReservas).
"""

from models.database import DatabaseConnector


class ReservaModel:

    def __init__(self, db: DatabaseConnector):
        self.db = db

    def get_all(self):
        return self.db.call_procedure('sp_GetAllReservas')

    def get_by_id(self, ID_reserva: int):
        return self.db.call_procedure('sp_GetReserva', (ID_reserva,))

    def get_clientes(self):
        return self.db.call_procedure(
            "sp_GetAllClientes"
        )

    def get_tipos_clientes(self):
        return self.db.call_procedure(
            'sp_GetAllGetAllTiposClientes'
        )

    def get_tipos(self):
        return self.db.call_procedure(
            "sp_GetAllTiposHabitacion"
        )

    def insert(self,fecha_creacion, ID_cliente, fecha_llegada, fecha_salida, num_habitaciones, ID_tipo, adultos, ninos, tarifa_aplicada, deposito, metodo_pago, estado):
        return self.db.call_procedure(
            'sp_InsertReserva',
            (fecha_creacion, ID_cliente, fecha_llegada, fecha_salida, num_habitaciones, ID_tipo, adultos, ninos, tarifa_aplicada, deposito, metodo_pago, estado))

    def update(self, ID_reserva, fecha_creacion, ID_cliente, fecha_llegada, fecha_salida, num_habitaciones, ID_tipo, adultos, ninos, tarifa_aplicada, deposito, metodo_pago, estado):
        return self.db.call_procedure(
            'sp_UpdateReserva',
            (ID_reserva, fecha_creacion, ID_cliente, fecha_llegada, fecha_salida, num_habitaciones, ID_tipo, adultos, ninos, tarifa_aplicada, deposito, metodo_pago, estado))

    def delete(self, ID_reserva: int):
        return self.db.call_procedure('sp_DeleteReserva', (ID_reserva,))