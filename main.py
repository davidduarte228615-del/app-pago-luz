"""Punto de entrada: ensambla Modelo, Vista y Controlador y registra el observador."""
import tkinter as tk

from controlador import ControladorPagoLuz
from modelo import ModeloPagoLuz
from vista import VistaPagoLuz


def main():
    root = tk.Tk()
    modelo = ModeloPagoLuz()
    vista = VistaPagoLuz(root, modelo)
    controlador = ControladorPagoLuz(modelo)

    vista.setControlador(controlador)
    modelo.agregarObservador(vista)   # la vista se suscribe a los cambios del modelo

    root.mainloop()


if __name__ == "__main__":
    main()
