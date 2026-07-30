# models/studiengang.py
"""Datenmodell für den Studiengang, reines Datenobjekt ohne eigene Logik.
Berechnungen (ECTS-Fortschritt, Durchschnitt etc.) übernimmt der
StudiengangService, dem die Kursliste jeweils als Parameter übergeben wird."""

class Studiengang:
    """Repräsentiert den Studiengang ein reines Datenobjekt."""

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
        """Gesamtzahl der für den Studiengang benötigten ECTS-Punkte (z.B. 180)."""
        return self._gesamt_ects

    @gesamt_ects.setter
    def gesamt_ects(self, wert: int):
        self._gesamt_ects = wert