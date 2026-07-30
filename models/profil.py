# models/profil.py
"""Datenmodell für das Nutzerprofil, hält die persönlichen Daten und die
Liste aller eingetragenen Kurse."""
from models.kurs import Kurs


class Profil:
    """Repräsentiert das Nutzerprofil mit allen Kursen.

    Die Kurse werden bewusst hier im Profil verwaltet (nicht im Studiengang),
    da sie individuell vom Nutzer gepflegt werden. Der Studiengang erhält die
    Kursliste bei Bedarf als Parameter für Berechnungen (siehe StudiengangService).
    """

    def __init__(self, name: str, matrikelnummer: str):
        self._name = name
        self._matrikelnummer = matrikelnummer
        self._kurse: list[Kurs] = []

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, wert: str):
        self._name = wert

    @property
    def matrikelnummer(self) -> str:
        return self._matrikelnummer

    @property
    def kurse(self) -> list[Kurs]:
        """Alle Kurse des Nutzers (aktive UND archivierte)."""
        return self._kurse

    def kurs_hinzufuegen(self, kurs: Kurs):
        """Fügt einen Kurs zum Profil hinzu."""
        self._kurse.append(kurs)

    def kurs_entfernen(self, kurs: Kurs):
        """Entfernt einen Kurs aus dem Profil (z.B. über den 'Löschen'-Button)."""
        if kurs in self._kurse:
            self._kurse.remove(kurs)