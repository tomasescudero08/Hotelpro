"""
controllers/tarifa_controller.py
─────────────────────────────────────
CONTROLADOR de tarifa: valida la entrada, llama al TarifaModel y
actualiza la TarifaView con el resultado.
"""

from tkinter import messagebox, filedialog
from models.tarifa_model import TarifaModel
from views.tarifa_view import TarifaView

from utils.validators import (
    validate_required,
    validate_numeric,
    validate_text
)

from utils.exporter import (
    exportar_excel,
    exportar_pdf
)

TREE_KEYS = ["ID_tarifa", "ID_tipo", "tarifa_base",
             "impuestos", "descuento", "condiciones"]

class TarifaController:
    def cargar_tipos(self):

        success, tipos = self.model.get_tipos_habitacion()

        if success:
            self.view.set_tipos(tipos)

        else:
            messagebox.showerror(
                "Error",
                tipos
            )

    def __init__(self, parent, db):
        self.model = TarifaModel(db)
        self.view = TarifaView(parent, self)
        self.view.pack(
            fill="both",
            expand=True
        )
        self.cargar_tipos()
        self.cargar_lista()

    def guardar(self):
        data = self.view.get_form_data()

        if not validate_required(data["tarifa_base"]):
            messagebox.showerror("Validación", "La tarifa base es obligatoria.")
            return

        ok, tarifa_base = validate_numeric(data["tarifa_base"])

        if not ok:
            messagebox.showerror(
                "Validación",
                "La tarifa base debe contener únicamente números."
            )
            return
        ok, impuestos = validate_numeric(data["impuestos"])

        if not ok:
            messagebox.showerror(
                "Validación",
                "Los impuestos deben contener únicamente números."
            )
            return
        ok, descuento = validate_numeric(data["descuento"])

        if not ok:
            messagebox.showerror(
                "Validación",
                "El descuento debe contener únicamente números."
            )
            return

        if not validate_text(data["condiciones"]):
            messagebox.showerror(
                "Validación",
                "Las condiciones solo deben contener letras."
            )
            return

        success, result = self.model.insert(
            data["ID_tipo"] or None,
            data["tarifa_base"] or None, data["impuestos"] or None,
            data["descuento"] or None, data["condiciones"] or None)

        if success:
            messagebox.showinfo("Éxito", "Tarifa guardada correctamente.")
            self.limpiar()
            self.cargar_lista()
        else:
            messagebox.showerror("Error", f"Error al guardar: {result}")

    def actualizar(self):
        data = self.view.get_form_data()

        ok, ID_tarifa = validate_numeric(data["ID_tarifa"])
        if not validate_required(data["tarifa_base"]):
            messagebox.showerror("Validación", "La tarifa base es obligatoria.")
            return

        success, result = self.model.update(
            ID_tarifa, data["ID_tipo"] or None,
            data["tarifa_base"] or None, data["impuestos"] or None,
            data["descuento"] or None, data["condiciones"] or None)


        if success:
            messagebox.showinfo("Éxito", "Tarifa actualizada.")
            self.cargar_lista()
        else:
            messagebox.showerror("Error", f"Error al actualizar: {result}")

    def eliminar(self):
        data = self.view.get_form_data()

        ok, ID_tarifa = validate_numeric(data["ID_tarifa"])
        if not ok or ID_tarifa is None:
            messagebox.showerror("Error", "Ingresa una ID_tarifa válido.")
            return

        if not messagebox.askyesno("Confirmar", "¿Eliminar esta tarifa?"):
            return

        success, result = self.model.delete(ID_tarifa)
        if success:
            messagebox.showinfo("Éxito", "Tarifa eliminada.")
            self.limpiar()
            self.cargar_lista()
        else:
            messagebox.showerror("Error", f"Error al eliminar: {result}")

    def buscar(self):
        data = self.view.get_form_data()

        ok, ID_tarifa = validate_numeric(data["ID_tarifa"])
        if not ok or ID_tarifa is None:
            messagebox.showerror("Error", "Ingresa una ID_tarifa válido.")
            return

        success, result = self.model.get_by_id(ID_tarifa)
        if success and result:
            self.view.set_form_data(dict(zip(TREE_KEYS, result[0])))
        else:
            messagebox.showinfo("No encontrado", "Tarifa no encontrado.")

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

    def exportar_excel(self):

        success, rows = self.model.get_all()

        if not success:
            messagebox.showerror(
                "Error",
                f"No se pudieron obtener las tarifas: {rows}"
            )
            return

        if not rows:
            messagebox.showinfo(
                "Exportar",
                "No hay tarifas para exportar."
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
            "ID_tarifa",
            "ID_tipo",
            "tarifa_base",
            "impuestos",
            "descuento",
            "condiciones"
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
                f"No se pudieron obtener las tarifas: {rows}"
            )
            return

        if not rows:
            messagebox.showinfo(
                "Exportar",
                "No hay tarifas para exportar."
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
            "ID_tarifa",
            "ID_tipo",
            "tarifa_base",
            "impuestos",
            "descuento",
            "condiciones"
        ]

        try:

            exportar_pdf(
                rows,
                columns,
                filename,
                "REPORTE DE TARIFAS"
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