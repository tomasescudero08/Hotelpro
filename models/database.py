"""
models/database.py
───────────────────
Capa de acceso a datos (MODELO base). Es la única parte de la app que
conoce mysql.connector. Ni las vistas ni los controladores importan
mysql.connector directamente — todos pasan por aquí.
"""
"""requiere --> pip install my-sql-connector-python"""

import mysql.connector
from mysql.connector import Error


class DatabaseConnector:
    """Maneja la conexión y la ejecución de Stored Procedures."""

    def __init__(self, config: dict):
        self.config     = config
        self.connection = None
        self.cursor     = None

    def connect(self) -> tuple[bool, str | None]:
        try:
            self.connection = mysql.connector.connect(**self.config)
            self.cursor = self.connection.cursor(buffered=True)
            return True, None
        except Error as e:
            self.connection = None
            self.cursor = None
            return False, str(e)

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        self.cursor = None
        self.connection = None

    @property
    def is_connected(self) -> bool:
        return self.connection is not None and self.connection.is_connected()

    def call_procedure(self, procedure_name: str, params: tuple = ()) -> tuple[bool, list | str]:
        """
        Ejecuta un SP y retorna (True, filas) o (False, mensaje_de_error).
        """
        if not self.is_connected:
            ok, err = self.connect()
            if not ok:
                return False, err
        try:
            self.cursor.callproc(procedure_name, params)
            results = []
            for result in self.cursor.stored_results():
                results.extend(result.fetchall())
            self.connection.commit()
            return True, results
        except Error as e:
            self.connection.rollback()
            return False, str(e)

    