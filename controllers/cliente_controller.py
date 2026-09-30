"""
controllers/cliente_controller.py
"""

import os
import tkinter as tk
from tkinter import messagebox, filedialog, Toplevel, ttk
from PIL import Image, ImageTk

from models.cliente_model import ClienteModel
from views.cliente_view import ClienteView
from utils.validators import (
    validate_required,
    validate_numeric,
    validate_text,
    validate_email
)
from utils.exporter import exportar_excel, exportar_pdf
from utils.export_filters import filtrar_clientes
from views.export_dialogs import VentanaFiltroCliente

# Incluimos 'imagen' en TREE_KEYS para mapear los 11 valores recibidos de la base de datos
TREE_KEYS = [
    "ID_cliente", "nombre", "apellido", "documento",
    "nacionalidad", "fecha_nacimiento", "direccion",
    "telefono", "correo", "nivel_fidelizacion", "imagen"
]

class ClienteController:

    def __init__(self, parent, db):
        self.model = ClienteModel(db)
        self.view = ClienteView(parent, self)
        self.view.pack(fill="both", expand=True)
        self.cargar_lista()

    def cargar_lista(self):
        success, result = self.model.get_all()
        if success:
            self.view.set_tree_data(result)
        else:
            messagebox.showerror("Error", f"No se pudo cargar la lista: {result}")

    def guardar(self):
        data = self.view.get_form_data()

        # Validaciones de campos
        if not validate_required(data["nombre"]):
            messagebox.showerror("Validación", "El nombre es obligatorio.")
            return
        if not validate_text(data["nombre"]):
            messagebox.showerror("Validación", "El nombre solo debe contener letras.")
            return
        if not validate_required(data["apellido"]):
            messagebox.showerror("Validación", "El apellido es obligatorio.")
            return
        if not validate_text(data["apellido"]):
            messagebox.showerror("Validación", "El apellido solo debe contener letras.")
            return
        if not validate_required(data["nacionalidad"]):
            messagebox.showerror("Validación", "La nacionalidad es obligatoria.")
            return
        if not validate_text(data["nacionalidad"]):
            messagebox.showerror("Validación", "La nacionalidad solo debe contener letras.")
            return
        ok, telefono = validate_numeric(data["telefono"])
        if not ok:
            messagebox.showerror("Validación", "El teléfono debe contener únicamente números.")
            return
        if not validate_required(data["correo"]):
            messagebox.showerror("Validación", "El correo es obligatorio.")
            return
        if not validate_email(data["correo"]):
            messagebox.showerror("Validación", "Ingrese un correo electrónico válido.")
            return
        ok, nivel = validate_numeric(data["nivel_fidelizacion"])
        if not ok:
            messagebox.showerror("Validación", "El nivel de fidelización debe ser numérico.")
            return
        if not validate_required(data["documento"]):
            messagebox.showerror("Validación", "El documento es obligatorio.")
            return

        success, result = self.model.insert(
            data["nombre"], data["apellido"] or None,
            data["documento"] or None, data["nacionalidad"] or None,
            data["fecha_nacimiento"] or None, data["direccion"] or None,
            data["telefono"] or None, data["correo"] or None,
            data["nivel_fidelizacion"] or None, data["imagen"] or None
        )

        if success:
            messagebox.showinfo("Éxito", "Cliente guardado correctamente.")
            self.limpiar()
            self.cargar_lista()
        else:
            messagebox.showerror("Error", f"Error al guardar: {result}")

    def actualizar(self):
        data = self.view.get_form_data()

        ok, ID_cliente = validate_numeric(data["ID_cliente"])
        if not ok or ID_cliente is None:
            messagebox.showerror("Error", "Ingresa un ID_cliente válido.")
            return

        if not validate_required(data["documento"]):
            messagebox.showerror("Validación", "El documento es obligatorio.")
            return

        success, result = self.model.update(
            ID_cliente, data["nombre"], data["apellido"] or None,
            data["documento"] or None, data["nacionalidad"] or None,
            data["fecha_nacimiento"] or None, data["direccion"] or None,
            data["telefono"] or None, data["correo"] or None,
            data["nivel_fidelizacion"] or None, data["imagen"] or None
        )

        if success:
            messagebox.showinfo("Éxito", "Cliente actualizado.")
            self.limpiar()
            self.cargar_lista()
        else:
            messagebox.showerror("Error", f"Error al actualizar: {result}")

    def eliminar(self):
        data = self.view.get_form_data()

        ok, ID_cliente = validate_numeric(data["ID_cliente"])
        if not ok or ID_cliente is None:
            messagebox.showerror("Error", "Ingresa un ID_cliente válido.")
            return

        if not messagebox.askyesno("Confirmar", "¿Eliminar este cliente?"):
            return

        success, result = self.model.delete(ID_cliente)
        if success:
            messagebox.showinfo("Éxito", "Cliente eliminado.")
            self.limpiar()
            self.cargar_lista()
        else:
            messagebox.showerror("Error", f"Error al eliminar: {result}")

    def buscar(self):
        data = self.view.get_form_data()

        ok, ID_cliente = validate_numeric(data["ID_cliente"])
        if not ok or ID_cliente is None:
            messagebox.showerror("Error", "Ingresa un ID_cliente válido.")
            return

        success, result = self.model.get_by_id(ID_cliente)
        if success and result:
            self.view.set_form_data(dict(zip(TREE_KEYS, result[0])))
        else:
            messagebox.showinfo("No encontrado", "Cliente no encontrado.")

    def limpiar(self):
        self.view.clear_form()

    def on_select(self, event):
        values = self.view.get_selected_tree_values()
        if values:
            # Consultamos los datos completos directo del modelo para traer la ruta real del campo 'imagen'
            ID_cliente = values[0]
            success, result = self.model.get_by_id(ID_cliente)
            if success and result:
                self.view.set_form_data(dict(zip(TREE_KEYS, result[0])))

    def mostrar_imagen(self):
        """Abre la foto del cliente en una ventana que se ajusta exactamente al tamaño de la imagen sin permitir redimensionar."""
        data = self.view.get_form_data()
        ruta_imagen = data.get("imagen")

        if not ruta_imagen or not os.path.exists(str(ruta_imagen)):
            messagebox.showwarning("Sin Imagen", "El cliente seleccionado no tiene una imagen o ruta válida.")
            return

        try:
            # Cargar imagen original
            img = Image.open(ruta_imagen)

            img.thumbnail((500, 500), Image.Resampling.LANCZOS)

            ancho_img, alto_img = img.size

            top = Toplevel(self.view)
            top.title("Imagen del Cliente")

            top.resizable(False, False)

            top.geometry(f"{ancho_img}x{alto_img}")

            photo = ImageTk.PhotoImage(img)

            lbl_img = ttk.Label(top, image=photo)
            lbl_img.image = photo  
            lbl_img.pack(fill="both", expand=True)

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen:\n{e}")

    def ventana_filtros_exportacion(self):
        success, rows = self.model.get_all()
        if not success or not rows:
            messagebox.showinfo("Exportar", "No hay datos para exportar.")
            return

        nacionalidades = sorted({str(row[4]) for row in rows if len(row) > 4 and row[4] is not None})
        niveles = sorted({str(row[9]) for row in rows if len(row) > 9 and row[9] is not None})

        VentanaFiltroCliente(
            self.view,
            self.exportar_filtrado,
            nacionalidades,
            niveles
        )

    def exportar_filtrado(self, formato, filtros, ventana):
        success, rows = self.model.get_all()
        if not success:
            return

        rows_filtradas = filtrar_clientes(
            rows,
            filtros.get("fecha_desde"),
            filtros.get("fecha_hasta"),
            filtros.get("nacionalidad"),
            filtros.get("nivel_fidelizacion")
        )

        if not rows_filtradas:
            messagebox.showinfo("Exportación", "No existen clientes con estos filtros.")
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
            "ID cliente", "nombre", "apellido", "documento",
            "nacionalidad", "fecha_nacimiento", "direccion",
            "telefono", "correo", "nivel_fidelizacion"
        ]

        try:
            if formato == "excel":
                exportar_excel(rows_filtradas, columns, filename)
            else:
                exportar_pdf(rows_filtradas, columns, filename, "REPORTE DE CLIENTES")

            ventana.destroy()
            messagebox.showinfo("Éxito", f"{tipo_archivo} exportado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar:\n{e}")