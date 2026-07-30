# models/lektion.py
"""Datenmodell für eine einzelne Lektion innerhalb eines Kurses."""

class Lektion:
    """Repräsentiert eine einzelne Lektion innerhalb eines Kurses.

    Eine Lektion hat nur einen Namen und einen Abgeschlossen-Status; der
    Lernfortschritt eines Kurses (Kurs.berechne_fortschritt()) berechnet sich
    aus dem Anteil abgeschlossener Lektionen an der Gesamtzahl.
    """

    def __init__(self, name: str):
        self._name = name
        self._abgeschlossen = False

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

    def lektion_entfernen(self):
        """Markiert die Lektion als zu löschen.

        Hinweis: Das tatsächliche Entfernen von Lektionen läuft in der Praxis
        über Kurs.lektionen_anzahl_anpassen(), das die Lektionen-Liste direkt
        anpasst. Diese Methode existiert zur Konsistenz mit dem Klassendiagramm,
        wird aktuell aber nicht aufgerufen.
        """
        pass