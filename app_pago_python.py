import tkinter as tk
from tkinter import ttk, messagebox

class AppPagoLuz:
    def __init__(self, root):
        self.root = root
        self.root.title("Pago de Servicio de Luz")
        self.root.geometry("650x550")
        self.root.resizable(False, False)
        self.root.configure(bg="#000000")

        self.clientes_db = {
            "DAVID": {"codigo": "DAVID", "nombre": "David López", "periodo": "Enero – Febrero 2026", "importe": 2500, "fecha_limite": "01 marzo 2026", "estado": "SIN PAGAR"},
            "DANIEL": {"codigo": "DANIEL", "nombre": "Daniela Gómez", "periodo": "Enero – Febrero 2026", "importe": 2100, "fecha_limite": "01 marzo 2026", "estado": "SIN PAGAR"},
            "MARCO": {"codigo": "MARCO", "nombre": "Marco Antonio", "periodo": "Enero – Febrero 2026", "importe": 1800, "fecha_limite": "01 marzo 2026", "estado": "SIN PAGAR"},
            "ESMERALDA": {"codigo": "ESMERALDA", "nombre": "Esmeralda Ruiz", "periodo": "Enero – Febrero 2026", "importe": 2900, "fecha_limite": "01 marzo 2026", "estado": "SIN PAGAR"},
            "ESTRADA": {"codigo": "ESTRADA", "nombre": "Carlos Estrada", "periodo": "Enero – Febrero 2026", "importe": 3300, "fecha_limite": "01 marzo 2026", "estado": "SIN PAGAR"},
            "ESQUER": {"codigo": "ESQUER", "nombre": "Fernando Esquer", "periodo": "Enero – Febrero 2026", "importe": 3100, "fecha_limite": "01 marzo 2026", "estado": "SIN PAGAR"},
            "PRADA": {"codigo": "PRADA", "nombre": "Prada Mendoza", "periodo": "Enero – Febrero 2026", "importe": 1500, "fecha_limite": "01 marzo 2026", "estado": "SIN PAGAR"},
            "RODRIGO": {"codigo": "RODRIGO", "nombre": "Rodrigo Silva", "periodo": "Enero – Febrero 2026", "importe": 2700, "fecha_limite": "01 marzo 2026", "estado": "SIN PAGAR"},
            "SOFIA": {"codigo": "SOFIA", "nombre": "Sofía Castro", "periodo": "Enero – Febrero 2026", "importe": 1950, "fecha_limite": "01 marzo 2026", "estado": "SIN PAGAR"},
            "VALERIA": {"codigo": "VALERIA", "nombre": "Valeria Morales", "periodo": "Enero – Febrero 2026", "importe": 3400, "fecha_limite": "01 marzo 2026", "estado": "SIN PAGAR"},
            "45678": {"codigo": "45678", "nombre": "Andrés Pineda (45678)", "periodo": "Enero – Febrero 2026", "importe": 2200, "fecha_limite": "01 marzo 2026", "estado": "SIN PAGAR"},
            "89012": {"codigo": "89012", "nombre": "Beatriz Vega (89012)", "periodo": "Enero – Febrero 2026", "importe": 1600, "fecha_limite": "01 marzo 2026", "estado": "SIN PAGAR"}
        }

        self.cliente_seleccionado = None
        self.setup_ui()

    def setup_ui(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("THorizontal.TSeparator", background="#ffffff")

        frame_top = tk.Frame(self.root, bg="#000000", padx=10, pady=10)
        frame_top.pack(fill=tk.X, padx=15, pady=10)

        tk.Label(frame_top, text="Numero de servicio / Nombre:", font=("Arial", 11, "bold"), bg="#000000", fg="#ffffff").grid(row=0, column=0, sticky="w", pady=2)
        
        self.entry_servicio = tk.Entry(frame_top, font=("Arial", 12), width=25, bg="#000000", fg="#ffffff", insertbackground="#ffffff", highlightthickness=1, highlightbackground="#ffffff", highlightcolor="#4CAF50")
        self.entry_servicio.grid(row=1, column=0, sticky="w", pady=5, padx=(0, 20))
        self.entry_servicio.bind("<KeyRelease>", self.filtrar_clientes)

        tk.Label(frame_top, text="Clientes encontrados:", font=("Arial", 10), bg="#000000", fg="#ffffff").grid(row=0, column=1, sticky="w")
        
        self.listbox_clientes = tk.Listbox(frame_top, height=5, width=25, font=("Arial", 10), bg="#000000", fg="#ffffff", selectbackground="#4CAF50", selectforeground="#ffffff", highlightthickness=1, highlightbackground="#ffffff")
        self.listbox_clientes.grid(row=1, column=1, rowspan=2, sticky="nw")
        self.listbox_clientes.bind("<<ListboxSelect>>", self.seleccionar_cliente)

        self.lbl_instruccion = tk.Label(frame_top, text="Por favor, ingrese el numero unico de su\nservicio para continuar", font=("Arial", 9), bg="#000000", fg="#ffffff", justify="left")
        self.lbl_instruccion.grid(row=2, column=0, sticky="w")

        ttk.Separator(self.root, orient="horizontal", style="THorizontal.TSeparator").pack(fill=tk.X, padx=15, pady=5)

        self.frame_contenido = tk.LabelFrame(self.root, text=" Información ", font=("Arial", 11, "bold"), bg="#000000", fg="#ffffff", padx=15, pady=15, highlightthickness=1, highlightbackground="#ffffff")
        self.frame_contenido.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        self.lbl_placeholder = tk.Label(self.frame_contenido, text="Seleccione un cliente para ver los datos de consumo.", font=("Arial", 11), bg="#000000", fg="#ffffff")
        self.lbl_placeholder.pack(pady=40)

        self.btn_accion = tk.Button(self.root, text="Siguiente y pagar", font=("Arial", 11, "bold"), bg="#ff0000", fg="#ffffff", activebackground="#cc0000", activeforeground="#ffffff", state=tk.DISABLED, bd=0, relief=tk.FLAT, cursor="hand2")
        self.btn_accion.pack(pady=15, ipadx=10, ipady=5)

    def filtrar_clientes(self, event):
        criterio = self.entry_servicio.get().strip().upper()
        
        if not criterio:
            self.actualizar_listbox([])
            return

        coincidencias = []
        for key, data in self.clientes_db.items():
            if criterio in data["codigo"].upper() or criterio in data["nombre"].upper():
                coincidencias.append(key)
                
        self.actualizar_listbox(coincidencias)

    def actualizar_listbox(self, elementos):
        self.listbox_clientes.delete(0, tk.END)
        for item in elementos:
            self.listbox_clientes.insert(tk.END, self.clientes_db[item]["nombre"])

    def seleccionar_cliente(self, event):
        seleccion = self.listbox_clientes.curselection()
        if not seleccion:
            return

        nombre_sel = self.listbox_clientes.get(seleccion[0])
        
        for key, info in self.clientes_db.items():
            if info["nombre"] == nombre_sel:
                self.cliente_seleccionado = key
                break

        self.entry_servicio.delete(0, tk.END)
        self.entry_servicio.insert(0, self.clientes_db[self.cliente_seleccionado]["nombre"])

        self.mostrar_datos_consumo()

    def mostrar_datos_consumo(self):
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()

        datos = self.clientes_db[self.cliente_seleccionado]

        tk.Label(self.frame_contenido, text="Datos de consumo:", font=("Arial", 12, "bold"), bg="#000000", fg="#ffffff").pack(anchor="w", pady=(0, 10))
        
        info_text = (
            f"Periodo: {datos['periodo']}\n\n"
            f"Importe: ${datos['importe']}\n\n"
            f"Fecha límite de pago: {datos['fecha_limite']}\n\n"
            f"Estado: {datos['estado']}"
        )
        
        lbl_info = tk.Label(self.frame_contenido, text=info_text, font=("Arial", 11), bg="#000000", fg="#ffffff", justify="left")
        lbl_info.pack(anchor="w", padx=20)

        self.btn_accion.config(text="Siguiente y pagar", state=tk.NORMAL, bg="#4CAF50", activebackground="#45a049", command=self.abrir_modal_pago)

    def abrir_modal_pago(self):
        modal = tk.Toplevel(self.root)
        modal.title("Sección pagar")
        modal.geometry("350x220")
        modal.configure(bg="#000000")
        modal.grab_set()
        modal.resizable(False, False)

        tk.Label(modal, text="Sección pagar", font=("Arial", 12, "bold"), bg="#000000", fg="#ffffff").pack(pady=10)
        tk.Label(modal, text="Numero de tarjeta:", font=("Arial", 10), bg="#000000", fg="#ffffff").pack(anchor="w", padx=25)

        entry_tarjeta = tk.Entry(modal, font=("Arial", 12), width=25, bg="#000000", fg="#ffffff", insertbackground="#ffffff", highlightthickness=1, highlightbackground="#ffffff")
        entry_tarjeta.pack(pady=5)
        entry_tarjeta.focus()

        def procesar_pago():
            num_tarjeta = entry_tarjeta.get().strip()
            if len(num_tarjeta) < 4 or not num_tarjeta.isdigit():
                messagebox.showerror("Error", "Por favor ingrese un número de tarjeta válido (mínimo 4 dígitos).", parent=modal)
                return

            modal.destroy()
            self.mostrar_recibo_pago(num_tarjeta)

        btn_pagar = tk.Button(modal, text="Pagar", font=("Arial", 11, "bold"), bg="#4CAF50", fg="#ffffff", activebackground="#45a049", activeforeground="#ffffff", command=procesar_pago, width=20, bd=0, relief=tk.FLAT)
        btn_pagar.pack(pady=20)

    def mostrar_recibo_pago(self, tarjeta):
        self.clientes_db[self.cliente_seleccionado]["estado"] = "PAGADO"
        datos = self.clientes_db[self.cliente_seleccionado]
        ultimos_4 = tarjeta[-4:]

        for widget in self.frame_contenido.winfo_children():
            widget.destroy()

        tk.Label(self.frame_contenido, text="Recibo:", font=("Arial", 12, "bold"), bg="#000000", fg="#ffffff").pack(anchor="w", pady=(0, 10))

        recibo_text = (
            f"Cliente: {datos['nombre'].upper()}\n\n"
            f"Periodo: {datos['periodo']}\n\n"
            f"Importe pagado: ${datos['importe']}\n\n"
            f"Fecha del pago: 29 febrero a la 12PM\n\n"
            f"Tarjeta usada termina en: {ultimos_4}\n\n"
            f"Estado: {datos['estado']}"
        )

        lbl_recibo = tk.Label(self.frame_contenido, text=recibo_text, font=("Arial", 11), bg="#000000", fg="#ffffff", justify="left")
        lbl_recibo.pack(anchor="w", padx=20)

        self.btn_accion.config(
            text="Terminar proceso e imprimir recibo",
            bg="#4CAF50",
            activebackground="#45a049",
            command=self.finalizar_proceso
        )

    def finalizar_proceso(self):
        messagebox.showinfo("Éxito", "El recibo ha sido impreso correctamente.")
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AppPagoLuz(root)
    root.mainloop()