# models/studiengang.py

class Studiengang:
    """Repräsentiert den Studiengang — reines Datenobjekt."""

    def __init__(self, name: str, gesamt_ects: int):
        self._name = name
        self._gesamt_ects = gesamt_ects

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, wert: str):
        self._name = wert

    @property
    def gesamt_ects(self) -> int:
        return self._gesamt_ects

    @gesamt_ects.setter
    def gesamt_ects(self, wert: int):
        self._gesamt_ects = wert