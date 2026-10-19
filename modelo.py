"""Modelo (MVC) y Sujeto (Observer): lógica y estado del pago del servicio de luz."""
from entidades import Cliente, Consumo, Recibo, Tarjeta
from observer import Sujeto

PERIODO = "Enero – Febrero 2026"
FECHA_LIMITE = "01 marzo 2026"
FECHA_PAGO = "29 febrero a la 12PM"


class ModeloPagoLuz(Sujeto):
    def __init__(self):
        super().__init__()
        self.clientes = []               # coincidencias de la última búsqueda
        self.clienteSeleccionado = None
        self.consumo = None
        self.recibo = None
        self._todos = self._cargarClientes()   # "base de datos" en memoria

    @staticmethod
    def _cargarClientes():
        datos = [
            ("DAVID", "David López", 2500),
            ("DANIEL", "Daniela Gómez", 2100),
            ("MARCO", "Marco Antonio", 1800),
            ("ESMERALDA", "Esmeralda Ruiz", 2900),
            ("ESTRADA", "Carlos Estrada", 3300),
            ("ESQUER", "Fernando Esquer", 3100),
            ("PRADA", "Prada Mendoza", 1500),
            ("RODRIGO", "Rodrigo Silva", 2700),
            ("SOFIA", "Sofía Castro", 1950),
            ("VALERIA", "Valeria Morales", 3400),
            ("45678", "Andrés Pineda (45678)", 2200),
            ("89012", "Beatriz Vega (89012)", 1600),
        ]
        return [Cliente(num, nombre, [Consumo(PERIODO, importe, FECHA_LIMITE)])
                for num, nombre, importe in datos]

    # ------------------------------------------------------------ operaciones
    def buscarClientes(self, texto):
        """Filtra por número de servicio o nombre (sin distinguir mayúsculas).
        Solo cambia la lista: la información mostrada no se reinicia."""
        criterio = texto.strip().upper()
        if criterio:
            self.clientes = [c for c in self._todos
                             if criterio in c.numeroServicio.upper()
                             or criterio in c.nombre.upper()]
        else:
            self.clientes = []
        self.notificar()

    def seleccionarCliente(self, c):
        self.clienteSeleccionado = c
        self.consumo = c.consumos[-1] if c.consumos else None
        self.recibo = None
        self.notificar()

    def pagar(self, numeroTarjeta):
        if self.consumo is None:
            raise ValueError("Seleccione un cliente para ver su consumo.")
        tarjeta = self.validarTarjeta(numeroTarjeta)
        self.marcarPagado()
        self.generarRecibo(tarjeta)
        self.notificar()

    def validarTarjeta(self, numero):
        limpio = numero.strip()
        if len(limpio) < 4 or not limpio.isdigit():
            raise ValueError(
                "Por favor ingrese un número de tarjeta válido (mínimo 4 dígitos).")
        return Tarjeta(limpio)

    def marcarPagado(self):
        self.consumo.estado = "PAGADO"

    def generarRecibo(self, tarjeta):
        self.recibo = Recibo(
            folio="R-" + self.clienteSeleccionado.numeroServicio,
            importePagado=self.consumo.importe,
            fechaPago=FECHA_PAGO,
            ultimos4=tarjeta.numero[-4:],
            consumo=self.consumo,
            tarjeta=tarjeta,
        )

    # ---------------------------------------------------------------- getters
    def getClientes(self):
        return self.clientes

    def getConsumo(self):
        return self.consumo

    def getRecibo(self):
        return self.recibo
