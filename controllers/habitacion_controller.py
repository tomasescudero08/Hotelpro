"""
controllers/habitacion_controller.py
─────────────────────────────────────
CONTROLADOR de habitaciones: valida la entrada, llama al HabitacionModel y
actualiza la HabitacionView con el resultado.
"""

from tkinter import messagebox, filedialog

from models.habitacion_model import HabitacionModel
from views.habitacion_view import HabitacionView
from utils.validators import (
    validate_required,
    validate_numeric
)

from utils.exporter import (
    exportar_excel,
    exportar_pdf
)

TREE_KEYS = ["ID_habitacion", "numero_habitacion", "piso", "ID_tipo", "orientacion", "estado", "tarifa_base", "ID_hotel"]

class HabitacionController:

    def __init__(self, parent, db):
        self.model = HabitacionModel(db)
        self.view = HabitacionView(parent, self)
        self.view.pack(fill="both", expand=True)

        self.cargar_tipos()
        self.cargar_hoteles()
        self.cargar_lista()

    def cargar_tipos(self):
        success, tipos = self.model.get_tipos_habitacion()

        if success:
            self.view.set_tipos(tipos)
        else:
            messagebox.showerror("Error", tipos)

    def cargar_hoteles(self):
        success, hoteles = self.model.get_hoteles()

        if success:
            self.view.set_hoteles(hoteles)
        else:
            messagebox.showerror("Error", hoteles)


    def guardar(self):
        data = self.view.get_form_data()

        if not validate_required(data["numero_habitacion"]):
            messagebox.showerror("Validación", "El número de la habitación es obligatorio.")
            return

        ok, numero_habitacion = validate_numeric(data["numero_habitacion"])

        if not ok:
            messagebox.showerror(
                "Validación",
                "El numero de habitacion debe contener únicamente números."
            )
            return

        ok, tarifa_base = validate_numeric(data["tarifa_base"])

        if not ok:
            messagebox.showerror(
                "Validación",
                "La tarifa base debe contener únicamente números."
            )
            return

        if not validate_required(data["piso"]):
            messagebox.showerror("Validación", "Piso es obligatorio.")
            return

        ok, piso = validate_numeric(data["piso"])

        if not ok:
            messagebox.showerror(
                "Validación",
                "El piso base debe contener únicamente números."
            )
            return

        success, result = self.model.insert(
            data["numero_habitacion"], data["piso"] or None,
            data["ID_tipo"] or None, data["orientacion"] or None,
            data["estado"] or None, data["tarifa_base"] or None,
            data["ID_hotel"] or None)

        if success:
            messagebox.showinfo("Éxito", "Habitación guardada correctamente.")
            self.limpiar()
            self.cargar_lista()
        else:
            messagebox.showerror("Error", f"Error al guardar: {result}")

    def actualizar(self):
        data = self.view.get_form_data()

        ok, ID_habitacion = validate_numeric(data["ID_habitacion"])
        if not ok or ID_habitacion is None:
            messagebox.showerror("Error", "Ingresa un ID de habitación válido.")
            return

        if not validate_required(data["numero_habitacion"]):
            messagebox.showerror("Validación", "El numero de la habitación es obligatorio.")
            return
        if not validate_required(data["piso"]):
            messagebox.showerror("Validación", "Piso es obligatorio.")
            return

        success, result = self.model.update(
            ID_habitacion, data["numero_habitacion"], data["piso"] or None,
            data["ID_tipo"] or None, data["orientacion"] or None,
            data["estado"] or None, data["tarifa_base"] or None,
            data["ID_hotel"] or None)

        if success:
            messagebox.showinfo("Éxito", "Habitación actualizada.")
            self.cargar_lista()
        else:
            messagebox.showerror("Error", f"Error al actualizar: {result}")

    def eliminar(self):
        data = self.view.get_form_data()

        ok, ID_habitacion = validate_numeric(data["ID_habitacion"])
        if not ok or ID_habitacion is None:
            messagebox.showerror("Error", "Ingresa un ID de habitación válido.")
            return

        if not messagebox.askyesno("Confirmar", "¿Eliminar esta habitación?"):
            return

        success, result = self.model.delete(ID_habitacion)
        if success:
            messagebox.showinfo("Éxito", "Habitación eliminada.")
            self.limpiar()
            self.cargar_lista()
        else:
            messagebox.showerror("Error", f"Error al eliminar: {result}")

    def buscar(self):
        data = self.view.get_form_data()

        ok, ID_habitacion = validate_numeric(data["ID_habitacion"])
        if not ok or ID_habitacion is None:
            messagebox.showerror("Error", "Ingresa un ID_habitacion válido.")
            return

        success, result = self.model.get_by_id(ID_habitacion)
        if success and result:
            self.view.set_form_data(dict(zip(TREE_KEYS, result[0])))
        else:
            messagebox.showinfo("No encontrada", "Habitación no encontrada.")

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
                f"No se pudieron obtener las habitaciones: {rows}"
            )
            return

        if not rows:
            messagebox.showinfo(
                "Exportar",
                "No hay habitaciones para exportar."
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
            "ID_habitacion",
            "numero_habitacion",
            "piso", "ID_tipo",
            "orientacion",
            "estado",
            "tarifa_base",
            "ID_hotel"
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
                f"No se pudieron obtener las habitaciones: {rows}"
            )
            return

        if not rows:
            messagebox.showinfo(
                "Exportar",
                "No hay habitaciones para exportar."
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
            "ID_habitacion",
            "numero_habitacion",
            "piso", "ID_tipo",
            "orientacion",
            "estado",
            "tarifa_base",
            "ID_hotel"
        ]

        try:

            exportar_pdf(
                rows,
                columns,
                filename,
                "REPORTE DE HABITACIONES"
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