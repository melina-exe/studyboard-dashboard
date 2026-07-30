# services/studiengang_service.py
"""Service-Klasse für alle Berechnungen rund um den Studienfortschritt
(ECTS, Notendurchschnitt, Anzahl bestandener Kurse). Bewusst getrennt vom
reinen Datenmodell (Studiengang, Kurs), damit die Modelle selbst keine
Berechnungslogik enthalten müssen."""
from models.kurs import Kurs
from models.studiengang import Studiengang


class StudiengangService:
    """Übernimmt alle Berechnungen auf Basis der Kursliste."""

    def __init__(self, studiengang: Studiengang):
        self._studiengang = studiengang

    def berechne_bestandene_ects(self, kurse: list[Kurs]) -> int:
        """Gibt die Summe der ECTS aller bestandenen Kurse zurück
        (schließt auch bereits archivierte Kurse mit ein)."""
        return sum(k.ects for k in kurse if k.ist_bestanden())

    def berechne_ects_prozent(self, kurse: list[Kurs]) -> float:
        """Gibt den prozentualen ECTS-Fortschritt zurück (bestandene ECTS
        im Verhältnis zu den insgesamt benötigten ECTS des Studiengangs)."""
        if self._studiengang.gesamt_ects == 0:
            return 0.0
        return self.berechne_bestandene_ects(kurse) / self._studiengang.gesamt_ects * 100

    def berechne_durchschnitt(self, kurse: list[Kurs]) -> float:
        """Gibt den ECTS-gewichteten Notendurchschnitt aller bestandenen Kurse
        zurück (ein 10-ECTS-Kurs zählt also doppelt so stark wie ein
        5-ECTS-Kurs)."""
        bestandene = [k for k in kurse if k.ist_bestanden() and k.pruefungsleistung is not None]
        if not bestandene:
            return 0.0
        gesamt_ects = sum(k.ects for k in bestandene)
        if gesamt_ects == 0:
            return 0.0
        return sum(k.pruefungsleistung.note * k.ects for k in bestandene) / gesamt_ects

    def berechne_bestandene_kurse(self, kurse: list[Kurs]) -> int:
        """Gibt die Anzahl bestandener Kurse zurück."""
        return sum(1 for k in kurse if k.ist_bestanden())