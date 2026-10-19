"""Controlador (MVC): recibe los eventos de la vista y llama al modelo."""


class ControladorPagoLuz:
    def __init__(self, modelo):
        self.modelo = modelo

    def onTecleo(self, texto):
        self.modelo.buscarClientes(texto)

    def onSeleccion(self, c):
        self.modelo.seleccionarCliente(c)

    def onPagar(self, numero):
        self.modelo.pagar(numero)
