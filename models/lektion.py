# models/lektion.py
"""Datenmodell für eine einzelne Lektion innerhalb eines Kurses."""

class Lektion:
    """Repräsentiert eine einzelne Lektion innerhalb eines Kurses.

    Speichert nur Name und ob sie abgeschlossen ist. Der Fortschritt eines
    Kurses (Kurs.berechne_fortschritt()) ergibt sich daraus, wie viele
    Lektionen schon abgehakt sind."""

    def __init__(self, name: str):
        self._name = name
        self._abgeschlossen = False
        self._geloescht = False

    @property
    def name(self) -> str:
        """Name der Lektion, z.B. 'Lektion 1'."""
        return self._name

    @property
    def abgeschlossen(self) -> bool:
        """True, wenn die Lektion vom Nutzer als erledigt markiert wurde."""
        return self._abgeschlossen

    @abgeschlossen.setter
    def abgeschlossen(self, wert: bool):
        self._abgeschlossen = wert

    @property
    def geloescht(self) -> bool:
        """True, wenn die Lektion über lektion_entfernen() gelöscht wurde.
        Kurs.lektionen blendet gelöschte Lektionen aus, siehe dort."""
        return self._geloescht

    def lektion_entfernen(self):
        """Markiert die Lektion als gelöscht.

        Kurs.lektionen filtert gelöschte Lektionen automatisch raus, die
        Lektion bleibt also nur intern im Objekt erhalten, nicht mehr sichtbar."""
        self._geloescht = True