"""
models/cliente_model.py
─────────────────────────
MODELO de clientes. Traduce operaciones de negocio a llamadas de
Stored Procedures (sp_InsertCliente sp_UpdateCliente, sp_DeleteCliente,
sp_GetCliente, sp_GetAllClientes).
"""

from models.database import DatabaseConnector
class ClienteModel:

    def __init__(self, db: DatabaseConnector):
        self.db = db

    def get_all(self):
        return self.db.call_procedure('sp_GetAllClientes')

    def get_by_id(self, ID_cliente: int):
        return self.db.call_procedure('sp_GetCliente', (ID_cliente,))

    def insert(self, nombre, apellido, documento, nacionalidad, fecha_nacimiento, direccion, telefono, correo, nivel_fidelizacion):
        return self.db.call_procedure(
            'sp_InsertCliente',
            (nombre, apellido, documento, nacionalidad, fecha_nacimiento, direccion, telefono, correo, nivel_fidelizacion))

    def update(self, ID_cliente, nombre, apellido, documento, nacionalidad, fecha_nacimiento, direccion, telefono, correo, nivel_fidelizacion):
        return self.db.call_procedure(
            'sp_UpdateCliente',
            (ID_cliente, nombre, apellido, documento, nacionalidad, fecha_nacimiento, direccion, telefono, correo, nivel_fidelizacion))

    def delete(self, ID_cliente: int):
        return self.db.call_procedure('sp_DeleteCliente', (ID_cliente,))
