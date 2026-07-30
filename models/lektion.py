# models/lektion.py

class Lektion:
    """Repräsentiert eine einzelne Lektion innerhalb eines Kurses."""

    def __init__(self, name: str):
        self._name = name
        self._abgeschlossen = False

    @property
    def name(self) -> str:
        return self._name

    @property
    def abgeschlossen(self) -> bool:
        return self._abgeschlossen

    @abgeschlossen.setter
    def abgeschlossen(self, wert: bool):
        self._abgeschlossen = wert

    def lektion_entfernen(self):
        """Markiert die Lektion als zu löschen — wird vom Kurs aufgerufen."""
        pass