"""
models/habitacion_model.py
─────────────────────────
MODELO de Tarifa. Traduce operaciones de negocio a llamadas de
Stored Procedures (sp_InsertTarifa, sp_UpdateTarifa, sp_DeleteTarifa,
sp_GetTarifa, sp_GetAllTarifas).
"""

from models.database import DatabaseConnector


class TarifaModel:

    def __init__(self, db: DatabaseConnector):
        self.db = db

    def get_all(self):
        return self.db.call_procedure('sp_GetAllTarifas')

    def get_by_id(self, ID_tarifa: int):
        return self.db.call_procedure('sp_GetTarifa', (ID_tarifa,))

    def get_tipos_habitacion(self):
        return self.db.call_procedure(
            "sp_GetAllTiposHabitacion"
        )

    def insert(self, ID_tipo, tarifa_base, impuestos, descuento, condiciones):
        return self.db.call_procedure(
            'sp_InsertTarifa',
            (ID_tipo, tarifa_base, impuestos, descuento, condiciones))

    def update(self, ID_tarifa, ID_tipo, tarifa_base, impuestos, descuento, condiciones):
        return self.db.call_procedure(
            'sp_UpdateTarifa',
            (ID_tarifa, ID_tipo, tarifa_base, impuestos, descuento, condiciones))

    def delete(self, ID_tarifa: int):
        return self.db.call_procedure('sp_DeleteTarifa', (ID_tarifa,))