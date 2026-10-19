"""Patrón Observer: interfaz Observador y clase abstracta Sujeto."""
from abc import ABC, abstractmethod


class Observador(ABC):
    """Interfaz que implementan los objetos que quieren enterarse de cambios."""

    @abstractmethod
    def actualizar(self) -> None:
        """Se invoca cuando el sujeto notifica un cambio de estado."""


class Sujeto(ABC):
    """Mantiene la lista de observadores y los notifica."""

    def __init__(self):
        self.observadores = []

    def agregarObservador(self, o: Observador) -> None:
        if o not in self.observadores:
            self.observadores.append(o)

    def quitarObservador(self, o: Observador) -> None:
        if o in self.observadores:
            self.observadores.remove(o)

    def notificar(self) -> None:
        for o in list(self.observadores):
            o.actualizar()
