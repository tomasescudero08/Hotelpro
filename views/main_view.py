"""
views/main_view.py
────────────────────
VISTA principal: ventana raíz + Notebook con una pestaña por entidad.
Incluye el botón para alternar entre tema claro y oscuro.
"""

import tkinter as tk
from tkinter import ttk


class MainView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("— HOTELPRO CRUD (MVC)")
        self.geometry('1200x700')
        self.resizable(True, True)
        self.iconbitmap('C:/Users/Tomas Escudero/Desktop/favicon.ico')

        self.dark_mode = False

        # Barra superior: el botón queda separado del área de trabajo para no
        # quitar espacio horizontal a las tablas.
        self.topbar = tk.Frame(self, height=42)
        self.topbar.pack(fill="x", side="top")

        self.theme_button = tk.Button(
            self.topbar,
            text="🌙 Modo oscuro",
            font=("Arial", 9, "bold"),
            width=15,
            relief="flat",
            cursor="hand2",
            command=self.toggle_theme
        )
        self.theme_button.pack(side="left", padx=10, pady=7)

        self.notebook = ttk.Notebook(self)
        self.tab_cliente = ttk.Frame(self.notebook)
        self.tab_habitacion = ttk.Frame(self.notebook)
        self.tab_reserva = ttk.Frame(self.notebook)
        self.tab_tarifa = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_cliente, text="  Clientes  ")
        self.notebook.add(self.tab_habitacion, text="  Habitaciones")
        self.notebook.add(self.tab_reserva, text="  Reservas ")
        self.notebook.add(self.tab_tarifa, text="  Tarifas ")
        self.notebook.pack(expand=True, fill="both")

        self._configure_styles()
        self.apply_theme()

    def _configure_styles(self):
        """Configura los estilos ttk que se utilizan en toda la aplicación."""
        self.style = ttk.Style(self)
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass

    def toggle_theme(self):
        """Cambia entre tema claro y oscuro."""
        self.dark_mode = not self.dark_mode
        self.apply_theme()

    def apply_theme(self):
        """Aplica el tema actual a la ventana y a todos sus widgets."""
        if self.dark_mode:
            colors = {
                "bg": "#202124",
                "panel": "#292a2d",
                "entry": "#303134",
                "fg": "#f1f3f4",
                "muted": "#bdc1c6",
                "select": "#3c4043",
                "tree": "#292a2d",
                "tree_alt": "#303134",
                "heading": "#3c4043",
                "button": "#3c4043",
                "button_fg": "#ffffff",
            }
            self.theme_button.configure(text="☀ Modo claro")
        else:
            colors = {
                "bg": "#f0f0f0",
                "panel": "#f0f0f0",
                "entry": "#ffffff",
                "fg": "#222222",
                "muted": "#555555",
                "select": "#d9eaf7",
                "tree": "#ffffff",
                "tree_alt": "#f7f7f7",
                "heading": "#e5e5e5",
                "button": "#e0e0e0",
                "button_fg": "#222222",
            }
            self.theme_button.configure(text="🌙 Modo oscuro")

        # Ventana raíz y barra superior.
        self.configure(bg=colors["bg"])
        self.topbar.configure(bg=colors["bg"])
        self.theme_button.configure(
            bg=colors["button"],
            fg=colors["button_fg"],
            activebackground=colors["select"],
            activeforeground=colors["fg"]
        )

        # Estilos ttk compartidos por Notebook, Combobox, Treeview, etc.
        self.style.configure("TFrame", background=colors["panel"])
        self.style.configure(
            "TNotebook",
            background=colors["bg"],
            borderwidth=0
        )
        self.style.configure(
            "TNotebook.Tab",
            background=colors["button"],
            foreground=colors["fg"],
            padding=(10, 5)
        )
        self.style.map(
            "TNotebook.Tab",
            background=[("selected", colors["panel"])],
            foreground=[("selected", colors["fg"])]
        )
        self.style.configure(
            "TCombobox",
            fieldbackground=colors["entry"],
            background=colors["button"],
            foreground=colors["fg"]
        )
        self.style.map(
            "TCombobox",
            fieldbackground=[("readonly", colors["entry"])],
            foreground=[("readonly", colors["fg"])]
        )
        self.style.configure(
            "Treeview",
            background=colors["tree"],
            fieldbackground=colors["tree"],
            foreground=colors["fg"],
            rowheight=25
        )
        self.style.configure(
            "Treeview.Heading",
            background=colors["heading"],
            foreground=colors["fg"],
            font=("Arial", 9, "bold")
        )
        self.style.map(
            "Treeview",
            background=[("selected", "#1976D2")],
            foreground=[("selected", "white")]
        )
        self.style.configure(
            "Vertical.TScrollbar",
            background=colors["button"],
            troughcolor=colors["bg"],
            arrowcolor=colors["fg"]
        )

        # Aplicar a los widgets Tkinter ya creados por los módulos.
        self._apply_to_widget_tree(self, colors)

    def _apply_to_widget_tree(self, widget, colors):
        """Recorre widgets Tkinter y adapta fondos/textos sin tocar los botones
        de acciones coloreados (Guardar, Actualizar, etc.)."""
        for child in widget.winfo_children():
            try:
                widget_class = child.winfo_class()

                if widget_class in ("Frame", "Labelframe"):
                    child.configure(bg=colors["panel"])
                elif widget_class == "Label":
                    # Conserva imágenes y títulos; solo cambia el fondo/texto.
                    child.configure(bg=colors["panel"], fg=colors["fg"])
                elif widget_class == "Entry":
                    child.configure(
                        bg=colors["entry"],
                        fg=colors["fg"],
                        insertbackground=colors["fg"],
                        selectbackground="#1976D2",
                        selectforeground="white"
                    )
                elif widget_class == "Button":
                    # Los botones CRUD ya tienen colores propios. Solo se
                    # actualizan los botones neutros, como el de tema y Exportar.
                    current_bg = child.cget("background")
                    if child is self.theme_button or current_bg in ("#607D8B", "#e0e0e0"):
                        child.configure(
                            bg=colors["button"],
                            fg=colors["button_fg"],
                            activebackground=colors["select"],
                            activeforeground=colors["fg"]
                        )
                elif widget_class == "Toplevel":
                    child.configure(bg=colors["bg"])
            except (tk.TclError, AttributeError):
                pass

            self._apply_to_widget_tree(child, colors)
