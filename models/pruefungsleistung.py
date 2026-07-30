# models/pruefungsleistung.py
"""Datenmodell für eine abgelegte Prüfung (Note + Eintragungsdatum)."""
from datetime import date

class Pruefungsleistung:
    """Speichert Note und Eintragungsdatum einer abgelegten Prüfung.

    Notenskala nach deutschem Hochschulsystem: 1.0 ist die beste Note,
    4.0 ("ausreichend") gilt gerade noch als bestanden, 5.0 ist nicht bestanden.
    """

    def __init__(self):
        self._note = None
        # Eintragungsdatum wird beim Erstellen automatisch auf heute gesetzt.
        # Beim Laden aus der JSON-Datei wird es über den Setter unten mit dem
        # tatsächlich gespeicherten Datum überschrieben (siehe ProfilRepository.laden()).
        self._eintragungsdatum = date.today()

    @property
    def note(self) -> float:
        return self._note

    @note.setter
    def note(self, wert: float):
        """Setzt die Note, wenn sie im gültigen Bereich 1.0 bis 5.0 liegt."""
        if 1.0 <= wert <= 5.0:
            self._note = wert
        else:
            raise ValueError(f"Note muss zwischen 1.0 und 5.0 liegen, war: {wert}")

    @property
    def eintragungsdatum(self) -> date:
        """Datum, an dem die Note eingetragen wurde. Wird vom ArchivService
        genutzt, um zu prüfen, wie lange ein bestandener Kurs schon sichtbar ist."""
        return self._eintragungsdatum

    @eintragungsdatum.setter
    def eintragungsdatum(self, wert: date):
        """Wird beim Laden aus der JSON-Datei benötigt, um das ursprüngliche
        Eintragungsdatum wiederherzustellen (statt date.today() aus __init__)."""
        self._eintragungsdatum = wert

    def ist_bestanden(self) -> bool:
        """Gibt True zurück, wenn die Note 4.0 oder besser (also kleiner/gleich) ist."""
        if self._note is None:
            return False
        return self._note <= 4.0

    def pruefung_entfernen(self):
        """Setzt Note und Datum zurück."""
        self._note = None
        self._eintragungsdatum = None