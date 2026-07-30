# models/profil.py
from models.kurs import Kurs


class Profil:
    """Repräsentiert das Nutzerprofil mit allen Kursen."""

    def __init__(self, name: str, matrikelnummer: str):
        self._name = name
        self._matrikelnummer = matrikelnummer
        self._kurse: list[Kurs] = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def matrikelnummer(self) -> str:
        return self._matrikelnummer

    @property
    def kurse(self) -> list[Kurs]:
        return self._kurse

    def kurs_hinzufuegen(self, kurs: Kurs):
        """Fügt einen Kurs zum Profil hinzu."""
        self._kurse.append(kurs)

    def kurs_entfernen(self, kurs: Kurs):
        """Entfernt einen Kurs aus dem Profil."""
        if kurs in self._kurse:
            self._kurse.remove(kurs)