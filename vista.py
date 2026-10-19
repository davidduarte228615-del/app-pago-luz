"""Vista (MVC) y Observador (Observer): interfaz Tkinter del pago de luz."""
import tkinter as tk
from tkinter import ttk, messagebox

from observer import Observador

NEGRO = "#000000"
BLANCO = "#ffffff"


class VistaPagoLuz(Observador):
    def __init__(self, root, modelo):
        self.root = root
        self.modelo = modelo
        self.controlador = None
        self._listaMostrada = None
        self._construirUI()

    # ------------------------------------------------------------ Controlador
    def setControlador(self, c):
        self.controlador = c

    # ---------------------------------------------------------- Observer
    def actualizar(self):
        """El modelo cambió: la vista lee su estado y se redibuja."""
        clientes = self.modelo.getClientes()
        if clientes is not self._listaMostrada:      # solo si hubo una nueva búsqueda
            self.mostrarLista(clientes)

        recibo = self.modelo.getRecibo()
        if recibo is not None:
            self.mostrarRecibo(recibo)
            return

        consumo = self.modelo.getConsumo()
        if consumo is not None:
            self.mostrarConsumo(consumo)
        else:
            self._mostrarPlaceholder()

    # ------------------------------------------- eventos del usuario (vista)
    def teclearNumeroServicio(self, event=None):
        self.controlador.onTecleo(self.campoNumeroServicio.get())

    def seleccionarCliente(self, event=None):
        seleccion = self.listaClientes.curselection()
        if not seleccion:
            return
        cliente = self.modelo.getClientes()[seleccion[0]]
        self.campoNumeroServicio.delete(0, tk.END)
        self.campoNumeroServicio.insert(0, cliente.nombre)
        self.controlador.onSeleccion(cliente)

    def pagar(self, modal, campoTarjeta):
        try:
            self.controlador.onPagar(campoTarjeta.get())
        except ValueError as error:
            messagebox.showerror("Error", str(error), parent=modal)
            return
        modal.destroy()

    # ------------------------------------------------------- mostrar datos
    def mostrarLista(self, clientes):
        self._listaMostrada = clientes
        self.listaClientes.delete(0, tk.END)
        for c in clientes:
            self.listaClientes.insert(tk.END, c.nombre)

    def mostrarConsumo(self, consumo):
        self._limpiarPanel()
        tk.Label(self.panelDetalle, text="Datos de consumo:",
                 font=("Arial", 12, "bold"), bg=NEGRO, fg=BLANCO
                 ).pack(anchor="w", pady=(0, 10))
        texto = (
            f"Periodo: {consumo.periodo}\n\n"
            f"Importe: ${consumo.importe}\n\n"
            f"Fecha límite de pago: {consumo.fechaLimite}\n\n"
            f"Estado: {consumo.estado}"
        )
        tk.Label(self.panelDetalle, text=texto, font=("Arial", 11),
                 bg=NEGRO, fg=BLANCO, justify="left").pack(anchor="w", padx=20)
        self._botonVerde("Siguiente y pagar", self._abrirModalPago)

    def mostrarRecibo(self, recibo):
        self._limpiarPanel()
        cliente = self.modelo.clienteSeleccionado
        tk.Label(self.panelDetalle, text="Recibo:",
                 font=("Arial", 12, "bold"), bg=NEGRO, fg=BLANCO
                 ).pack(anchor="w", pady=(0, 10))
        texto = (
            f"Cliente: {cliente.nombre.upper()}\n\n"
            f"Periodo: {recibo.consumo.periodo}\n\n"
            f"Importe pagado: ${recibo.importePagado}\n\n"
            f"Fecha del pago: {recibo.fechaPago}\n\n"
            f"Tarjeta usada termina en: {recibo.ultimos4}\n\n"
            f"Estado: {recibo.consumo.estado}"
        )
        tk.Label(self.panelDetalle, text=texto, font=("Arial", 11),
                 bg=NEGRO, fg=BLANCO, justify="left").pack(anchor="w", padx=20)
        self._botonVerde("Terminar proceso e imprimir recibo", self._terminar)

    # ------------------------------------------------- métodos auxiliares
    def _construirUI(self):
        self.root.title("Pago de Servicio de Luz")
        self.root.geometry("650x550")
        self.root.resizable(False, False)
        self.root.configure(bg=NEGRO)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("THorizontal.TSeparator", background=BLANCO)

        superior = tk.Frame(self.root, bg=NEGRO, padx=10, pady=10)
        superior.pack(fill=tk.X, padx=15, pady=10)

        tk.Label(superior, text="Numero de servicio / Nombre:",
                 font=("Arial", 11, "bold"), bg=NEGRO, fg=BLANCO
                 ).grid(row=0, column=0, sticky="w", pady=2)

        self.campoNumeroServicio = tk.Entry(
            superior, font=("Arial", 12), width=25, bg=NEGRO, fg=BLANCO,
            insertbackground=BLANCO, highlightthickness=1,
            highlightbackground=BLANCO, highlightcolor="#4CAF50")
        self.campoNumeroServicio.grid(row=1, column=0, sticky="w", pady=5, padx=(0, 20))
        self.campoNumeroServicio.bind("<KeyRelease>", self.teclearNumeroServicio)

        tk.Label(superior, text="Clientes encontrados:", font=("Arial", 10),
                 bg=NEGRO, fg=BLANCO).grid(row=0, column=1, sticky="w")

        self.listaClientes = tk.Listbox(
            superior, height=5, width=25, font=("Arial", 10), bg=NEGRO, fg=BLANCO,
            selectbackground="#4CAF50", selectforeground=BLANCO,
            highlightthickness=1, highlightbackground=BLANCO)
        self.listaClientes.grid(row=1, column=1, rowspan=2, sticky="nw")
        self.listaClientes.bind("<<ListboxSelect>>", self.seleccionarCliente)

        tk.Label(superior,
                 text="Por favor, ingrese el numero unico de su\nservicio para continuar",
                 font=("Arial", 9), bg=NEGRO, fg=BLANCO, justify="left"
                 ).grid(row=2, column=0, sticky="w")

        ttk.Separator(self.root, orient="horizontal",
                      style="THorizontal.TSeparator").pack(fill=tk.X, padx=15, pady=5)

        self.panelDetalle = tk.LabelFrame(
            self.root, text=" Información ", font=("Arial", 11, "bold"),
            bg=NEGRO, fg=BLANCO, padx=15, pady=15,
            highlightthickness=1, highlightbackground=BLANCO)
        self.panelDetalle.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        self.btnAccion = tk.Button(
            self.root, text="Siguiente y pagar", font=("Arial", 11, "bold"),
            bg="#ff0000", fg=BLANCO, activebackground="#cc0000",
            activeforeground=BLANCO, state=tk.DISABLED, bd=0, relief=tk.FLAT,
            cursor="hand2")
        self.btnAccion.pack(pady=15, ipadx=10, ipady=5)

        self._mostrarPlaceholder()

    def _limpiarPanel(self):
        for widget in self.panelDetalle.winfo_children():
            widget.destroy()

    def _mostrarPlaceholder(self):
        self._limpiarPanel()
        tk.Label(self.panelDetalle, font=("Arial", 11), bg=NEGRO, fg=BLANCO,
                 text="Seleccione un cliente para ver los datos de consumo."
                 ).pack(pady=40)

    def _botonVerde(self, texto, comando):
        self.btnAccion.config(text=texto, state=tk.NORMAL, bg="#4CAF50",
                              activebackground="#45a049", command=comando)

    def _abrirModalPago(self):
        modal = tk.Toplevel(self.root)
        modal.title("Sección pagar")
        modal.geometry("350x220")
        modal.configure(bg=NEGRO)
        modal.grab_set()
        modal.resizable(False, False)

        tk.Label(modal, text="Sección pagar", font=("Arial", 12, "bold"),
                 bg=NEGRO, fg=BLANCO).pack(pady=10)
        tk.Label(modal, text="Numero de tarjeta:", font=("Arial", 10),
                 bg=NEGRO, fg=BLANCO).pack(anchor="w", padx=25)

        campoTarjeta = tk.Entry(modal, font=("Arial", 12), width=25, bg=NEGRO,
                                fg=BLANCO, insertbackground=BLANCO,
                                highlightthickness=1, highlightbackground=BLANCO)
        campoTarjeta.pack(pady=5)
        campoTarjeta.focus()

        tk.Button(modal, text="Pagar", font=("Arial", 11, "bold"), bg="#4CAF50",
                  fg=BLANCO, activebackground="#45a049", activeforeground=BLANCO,
                  command=lambda: self.pagar(modal, campoTarjeta),
                  width=20, bd=0, relief=tk.FLAT).pack(pady=20)

    def _terminar(self):
        messagebox.showinfo("Éxito", "El recibo ha sido impreso correctamente.")
        self.root.destroy()
