"""
controllers/reserva_controller.py
─────────────────────────────────────
CONTROLADOR de reserva: valida la entrada, llama al ReservaModel y
actualiza la ReservaView con el resultado.
"""

from tkinter import messagebox, filedialog

from models.reserva_model import ReservaModel
from views.reserva_view import ReservaView

from utils.validators import (
    validate_required,
    validate_numeric
)

from utils.exporter import (
    exportar_excel,
    exportar_pdf
)

from utils.export_filters import filtrar_reservas

TREE_KEYS = ["ID_reserva", "fecha_creacion", "ID_cliente", "fecha_llegada",
             "fecha_salida", "num_habitaciones", "ID_tipo", "adultos", "ninos",
             "tarifa_aplicada", "deposito", "metodo_pago", "estado"]

class ReservaController:

    def __init__(self, parent, db):
        self.model = ReservaModel(db)
        self.view = ReservaView(parent, self)
        self.view.pack(fill="both", expand=True)
        self.tipos = {}
        self.cargar_clientes()
        self.cargar_tipos()
        self.cargar_lista()

    def guardar(self):
        data = self.view.get_form_data()

        if not validate_required(data["fecha_creacion"]):
            messagebox.showerror("Validación", "La fecha de creacion es obligatorio.")
            return

        ok, num_habitaciones = validate_numeric(data["num_habitaciones"])

        if not ok:
            messagebox.showerror(
                "Validación",
                "El numero de habitaciones debe contener únicamente números."
            )
            return

        ok, adultos = validate_numeric(data["adultos"])

        if not ok:
            messagebox.showerror(
                "Validación",
                "El numero de adultos debe contener únicamente números."
            )
            return

        ok, ninos = validate_numeric(data["ninos"])

        if not ok:
            messagebox.showerror(
                "Validación",
                "El numero de ninos debe contener únicamente números."
            )
            return

        ok, tarifa_aplicada = validate_numeric(data["tarifa_aplicada"])

        if not ok:
            messagebox.showerror(
                "Validación",
                "La tarifa aplicada debe contener únicamente números."
            )
            return

        ok, deposito = validate_numeric(data["deposito"])

        if not ok:
            messagebox.showerror(
                "Validación",
                "El deposito debe contener únicamente números."
            )
            return

        success, result = self.model.insert(
            data["fecha_creacion"] or None,
            data["ID_cliente"] or None,
            data["fecha_llegada"] or None,
            data["fecha_salida"] or None,
            num_habitaciones,
            data["ID_tipo"] or None,
            adultos,
            ninos,
            tarifa_aplicada,
            deposito,
            data["metodo_pago"] or None,
            data["estado"] or None
        )

        if success:
            messagebox.showinfo("Éxito", "Reserva guardada correctamente.")
            self.limpiar()
            self.cargar_lista()
        else:
            messagebox.showerror("Error", f"Error al guardar: {result}")

    def actualizar(self):
        data = self.view.get_form_data()

        ok, ID_reserva = validate_numeric(data["ID_reserva"])
        if not ok or ID_reserva is None:
            messagebox.showerror("Error", "Ingresa un ID_reserva válido.")
            return

        if not validate_required(data["fecha_creacion"]):
            messagebox.showerror("Validación", "La fecha de creacion es obligatorio.")
            return

        success, result = self.model.update(
            ID_reserva, data["fecha_creacion"], data["ID_cliente"] or None,
            data["fecha_llegada"] or None, data["fecha_salida"] or None,
            data["num_habitaciones"] or None, data["ID_tipo"] or None,
            data["adultos"] or None, data["ninos"] or None,
            data["tarifa_aplicada"] or None, data["deposito"] or None,
            data["metodo_pago"] or None, data["estado"] or None)

        if success:
            messagebox.showinfo("Éxito", "Reserva actualizada.")
            self.cargar_lista()
        else:
            messagebox.showerror("Error", f"Error al actualizar: {result}")

    def eliminar(self):
        data = self.view.get_form_data()

        ok, ID_reserva = validate_numeric(data["ID_reserva"])
        if not ok or ID_reserva is None:
            messagebox.showerror("Error", "Ingresa un ID_reserva válido.")
            return

        if not messagebox.askyesno("Confirmar", "¿Eliminar esta reserva?"):
            return

        success, result = self.model.delete(ID_reserva)
        if success:
            messagebox.showinfo("Éxito", "Reserva eliminada.")
            self.limpiar()
            self.cargar_lista()
        else:
            messagebox.showerror("Error", f"Error al eliminar: {result}")

    def buscar(self):
        data = self.view.get_form_data()

        ok, ID_reserva = validate_numeric(data["ID_reserva"])
        if not ok or ID_reserva is None:
            messagebox.showerror("Error", "Ingresa un ID_reserva válido.")
            return

        success, result = self.model.get_by_id(ID_reserva)
        if success and result:
            self.view.set_form_data(dict(zip(TREE_KEYS, result[0])))
        else:
            messagebox.showinfo("No encontrado", "Reserva no encontrado.")

    def limpiar(self):
        self.view.clear_form()

    def cargar_lista(self):
        success, result = self.model.get_all()
        if success:
            self.view.set_tree_data(result)
        else:
            messagebox.showerror("Error", f"No se pudo cargar la lista: {result}")

    def on_select(self, event):
        values = self.view.get_selected_tree_values()
        if values:
            self.view.set_form_data(dict(zip(TREE_KEYS, values)))

    def cargar_clientes(self):

        success, clientes = self.model.get_clientes()

        if success:
            self.view.set_clientes(clientes)

        else:
            messagebox.showerror(
                "Error",
                clientes
            )

    def cargar_tipos(self):

        success, tipos = self.model.get_tipos()

        if success:
            self.view.set_tipos(tipos)

        else:
            messagebox.showerror(
                "Error",
                tipos
            )

    def exportar_excel(self):

        success, rows = self.model.get_all()

        if not success:
            messagebox.showerror(
                "Error",
                f"No se pudieron obtener las reservas: {rows}"
            )
            return

        if not rows:
            messagebox.showinfo(
                "Exportar",
                "No hay reservas para exportar."
            )
            return

        filename = filedialog.asksaveasfilename(
            title="Guardar archivo Excel",
            defaultextension=".xlsx",
            filetypes=[
                ("Excel", "*.xlsx")
            ]
        )

        if not filename:
            return

        columns = [
            "ID_reserva",
            "fecha_creacion",
            "ID_cliente",
            "fecha_llegada",
            "fecha_salida",
            "num_habitaciones",
            "ID_tipo",
            "adultos",
            "ninos",
            "tarifa_aplicada",
            "deposito",
            "metodo_pago",
            "estado"
        ]

        try:

            exportar_excel(
                rows,
                columns,
                filename
            )

            messagebox.showinfo(
                "Éxito",
                "Archivo Excel exportado correctamente."
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"No se pudo exportar el Excel:\n{e}"
            )

    def exportar_pdf(self):

        success, rows = self.model.get_all()

        if not success:
            messagebox.showerror(
                "Error",
                f"No se pudieron obtener las reservas: {rows}"
            )
            return

        if not rows:
            messagebox.showinfo(
                "Exportar",
                "No hay reservas para exportar."
            )
            return

        filename = filedialog.asksaveasfilename(
            title="Guardar archivo PDF",
            defaultextension=".pdf",
            filetypes=[
                ("PDF", "*.pdf")
            ]
        )

        if not filename:
            return

        columns = [
            "ID",
            "Fecha creación",
            "Cliente",
            "Llegada",
            "Salida",
            "Habitaciones",
            "Tipo",
            "Adultos",
            "Niños",
            "Tarifa",
            "Depósito",
            "Método pago",
            "Estado"
        ]

        try:

            exportar_pdf(
                rows,
                columns,
                filename,
                "REPORTE DE RESERVAS"
            )

            messagebox.showinfo(
                "Éxito",
                "Archivo PDF exportado correctamente."
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"No se pudo exportar el PDF:\n{e}"
            )

    def exportar_excel_filtrado(
            self,
            fecha_desde,
            fecha_hasta,
            estado,
            metodo_pago,
            ventana
    ):

        success, rows = self.model.get_all()

        if not success:
            messagebox.showerror(
                "Error",
                f"No se pudieron obtener las reservas:\n{rows}"
            )

            return

        rows_filtradas = filtrar_reservas(
            rows,
            fecha_desde,
            fecha_hasta,
            estado,
            metodo_pago
        )

        if not rows_filtradas:
            messagebox.showinfo(
                "Exportación",
                "No existen reservas que coincidan con los filtros."
            )

            return

        filename = filedialog.asksaveasfilename(
            title="Guardar Excel",
            defaultextension=".xlsx",
            filetypes=[
                ("Archivo Excel", "*.xlsx")
            ]
        )

        if not filename:
            return

        columns = [
            "ID_reserva",
            "fecha_creacion",
            "ID_cliente",
            "fecha_llegada",
            "fecha_salida",
            "num_habitaciones",
            "ID_tipo",
            "adultos",
            "ninos",
            "tarifa_aplicada",
            "deposito",
            "metodo_pago",
            "estado"
        ]

        try:

            exportar_excel(
                rows_filtradas,
                columns,
                filename
            )

            ventana.destroy()

            messagebox.showinfo(
                "Éxito",
                "Excel exportado correctamente."
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"No se pudo exportar:\n{e}"
            )

    def exportar_pdf_filtrado(
            self,
            fecha_desde,
            fecha_hasta,
            estado,
            metodo_pago,
            ventana
    ):

        success, rows = self.model.get_all()

        if not success:
            messagebox.showerror(
                "Error",
                f"No se pudieron obtener las reservas:\n{rows}"
            )

            return

        rows_filtradas = filtrar_reservas(
            rows,
            fecha_desde,
            fecha_hasta,
            estado,
            metodo_pago
        )

        if not rows_filtradas:
            messagebox.showinfo(
                "Exportación",
                "No existen reservas que coincidan con los filtros."
            )

            return

        filename = filedialog.asksaveasfilename(
            title="Guardar PDF",
            defaultextension=".pdf",
            filetypes=[
                ("Archivo PDF", "*.pdf")
            ]
        )

        if not filename:
            return

        columns = [
            "ID",
            "Fecha creación",
            "Cliente",
            "Llegada",
            "Salida",
            "Habitaciones",
            "Tipo",
            "Adultos",
            "Niños",
            "Tarifa",
            "Depósito",
            "Método pago",
            "Estado"
        ]

        try:

            exportar_pdf(
                rows_filtradas,
                columns,
                filename,
                "REPORTE DE RESERVAS"
            )

            ventana.destroy()

            messagebox.showinfo(
                "Éxito",
                "PDF exportado correctamente."
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"No se pudo exportar:\n{e}"
            )