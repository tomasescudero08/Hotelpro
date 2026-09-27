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
from utils.export_filters import filtrar_tarifas, detectar_indice_fecha_tarifa
from views.export_dialogs import VentanaFiltroTarifa

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

    def ventana_filtros_exportacion(self):
        success, rows = self.model.get_all()

        if not success:
            messagebox.showerror("Error", f"No se pudieron obtener las tarifas: {rows}")
            return

        if not rows:
            messagebox.showinfo("Exportar", "No hay tarifas para exportar.")
            return

        tipos = list(self.view.tipos.keys())

        VentanaFiltroTarifa(
            self.view,
            self.exportar_filtrado,
            tipos
        )

    @staticmethod
    def _numero_valido(valor):
        if valor in (None, ""):
            return True
        try:
            float(valor)
            return True
        except (TypeError, ValueError):
            return False

    def exportar_filtrado(self, formato, filtros, ventana):
        precio_desde = filtros.get("precio_desde")
        precio_hasta = filtros.get("precio_hasta")

        if not self._numero_valido(precio_desde) or not self._numero_valido(precio_hasta):
            messagebox.showerror(
                "Validación",
                "El rango de precio debe contener únicamente números."
            )
            return

        if precio_desde and precio_hasta and float(precio_desde) > float(precio_hasta):
            messagebox.showerror(
                "Validación",
                "El precio desde no puede ser mayor que el precio hasta."
            )
            return

        success, rows = self.model.get_all()

        if not success:
            messagebox.showerror(
                "Error",
                f"No se pudieron obtener las tarifas: {rows}"
            )
            return

        tipo = filtros.get("tipo")
        ID_tipo = self.view.tipos.get(tipo) if tipo and tipo != "Todos" else None

        fecha_index = detectar_indice_fecha_tarifa(rows)

        if (filtros.get("fecha_desde") or filtros.get("fecha_hasta")) and fecha_index is None:
            messagebox.showwarning(
                "Filtro por fecha",
                "El módulo de Tarifas actualmente no recibe una fecha desde "
                "sp_GetAllTarifas. El filtro por fecha no puede aplicarse hasta "
                "que el procedimiento devuelva una columna de fecha."
            )
            return

        rows_filtradas = filtrar_tarifas(
            rows,
            filtros.get("fecha_desde"),
            filtros.get("fecha_hasta"),
            ID_tipo,
            precio_desde or None,
            precio_hasta or None,
            fecha_index
        )

        if not rows_filtradas:
            messagebox.showinfo(
                "Exportación",
                "No existen tarifas que coincidan con los filtros."
            )
            return

        extension = ".xlsx" if formato == "excel" else ".pdf"
        tipo_archivo = "Excel" if formato == "excel" else "PDF"
        filename = filedialog.asksaveasfilename(
            title=f"Guardar {tipo_archivo}",
            defaultextension=extension,
            filetypes=[(tipo_archivo, f"*{extension}")]
        )

        if not filename:
            return

        columns = [
            "ID_tarifa", "ID_tipo", "tarifa_base",
            "impuestos", "descuento", "condiciones"
        ]

        # Si una versión de la BD devuelve una fecha adicional, también se
        # incluye en el archivo exportado para no perder ese dato.
        if fecha_index is not None and fecha_index == 6:
            columns.append("fecha")

        try:
            if formato == "excel":
                exportar_excel(rows_filtradas, columns, filename)
            else:
                exportar_pdf(
                    rows_filtradas,
                    columns,
                    filename,
                    "REPORTE DE TARIFAS"
                )

            ventana.destroy()
            messagebox.showinfo(
                "Éxito",
                f"{tipo_archivo} exportado correctamente."
            )

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"No se pudo exportar:\n{e}"
            )
