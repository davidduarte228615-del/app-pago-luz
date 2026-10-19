"""Entidades del dominio: Cliente, Consumo, Tarjeta y Recibo (solo datos)."""


class Consumo:
    def __init__(self, periodo, importe, fechaLimite, estado="SIN PAGAR"):
        self.periodo = periodo
        self.importe = importe
        self.fechaLimite = fechaLimite
        self.estado = estado


class Cliente:
    def __init__(self, numeroServicio, nombre, consumos=None):
        self.numeroServicio = numeroServicio
        self.nombre = nombre
        # Asociación Cliente 1 --- 0..* Consumo
        self.consumos = consumos if consumos is not None else []


class Tarjeta:
    def __init__(self, numero):
        self.numero = numero


class Recibo:
    def __init__(self, folio, importePagado, fechaPago, ultimos4,
                 consumo=None, tarjeta=None):
        self.folio = folio
        self.importePagado = importePagado
        self.fechaPago = fechaPago
        self.ultimos4 = ultimos4
        # Asociaciones: Consumo 1 --- 0..1 Recibo  y  Recibo 0..* --- 1 Tarjeta
        self.consumo = consumo
        self.tarjeta = tarjeta
