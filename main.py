"""
main.py
───────
04 — hotelpro CRUD con arquitectura MVC
Tkinter + MySQL · GUI carpeta

Requiere: pip install mysql-connector-python tkcalendar
"""

from config import DB_CONFIG
from controllers.main_controller import MainController

if __name__ == "__main__":
    app = MainController(DB_CONFIG)
    app.run()


