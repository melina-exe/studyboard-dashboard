# models/kurs.py
from datetime import date
from models.lektion import Lektion
from models.pruefungsleistung import Pruefungsleistung
from models.status import Status


class Kurs:
    """Repräsentiert einen einzelnen Kurs im Studium."""

    def __init__(self, name: str, ects: int, semester: int = 1):
        self._name = name
        self._ects = None
        self._semester = None
        self.ects = ects
        self.semester = semester
        self._pruefungstermin: date | None = None
        self._archiviert: bool = False
        self._pruefungsleistung: Pruefungsleistung | None = None
        self._lektionen: list[Lektion] = []

    # -- Properties --

    @property
    def name(self) -> str:
        return self._name

    @property
    def ects(self) -> int:
        return self._ects

    @ects.setter
    def ects(self, wert: int):
        """Setzt die ECTS, wenn der Wert in einem realistischen Bereich liegt."""
        if wert <= 0:
            raise ValueError(f"ECTS müssen größer als 0 sein, war: {wert}")
        if wert > 20:
            raise ValueError(f"ECTS dürfen nicht größer als 20 sein, war: {wert}")
        self._ects = wert

    @property
    def semester(self) -> int:
        return self._semester

    @semester.setter
    def semester(self, wert: int):
        """Setzt das Semester, wenn der Wert in einem realistischen Bereich liegt."""
        if wert <= 0:
            raise ValueError(f"Semester muss größer als 0 sein, war: {wert}")
        if wert > 8:
            raise ValueError(f"Semester darf nicht größer als 8 sein, war: {wert}")
        self._semester = wert

    @property
    def pruefungstermin(self) -> date | None:
        return self._pruefungstermin

    @pruefungstermin.setter
    def pruefungstermin(self, wert: date | None):
        if wert is not None:
            fruehestes_jahr = 2015
            spaetestes_jahr = date.today().year + 10
            if not (fruehestes_jahr <= wert.year <= spaetestes_jahr):
                raise ValueError(
                    f"Prüfungstermin muss zwischen {fruehestes_jahr} und {spaetestes_jahr} liegen, war: {wert.year}"
                )
        self._pruefungstermin = wert

    @property
    def archiviert(self) -> bool:
        return self._archiviert

    @property
    def pruefungsleistung(self) -> Pruefungsleistung | None:
        return self._pruefungsleistung

    @pruefungsleistung.setter
    def pruefungsleistung(self, wert: Pruefungsleistung | None):
        self._pruefungsleistung = wert

    @property
    def lektionen(self) -> list[Lektion]:
        return self._lektionen

    @property
    def status(self) -> Status:
        """Abgeleiteter Status — wird aus den vorhandenen Daten berechnet."""
        if self._pruefungsleistung is not None and self._pruefungsleistung.ist_bestanden():
            return Status.BESTANDEN
        if self._pruefungstermin is not None:
            return Status.AUSSTEHEND
        return Status.LAUFEND

    # -- Methoden --

    def berechne_fortschritt(self) -> float:
        """Gibt den Lernfortschritt als Prozentwert zurück."""
        if not self._lektionen:
            return 0.0
        abgeschlossen = sum(1 for l in self._lektionen if l.abgeschlossen)
        return abgeschlossen / len(self._lektionen) * 100

    def berechne_countdown(self) -> int | None:
        """Gibt die verbleibenden Tage bis zum Prüfungstermin zurück."""
        if self._pruefungstermin is None:
            return None
        delta = self._pruefungstermin - date.today()
        return delta.days

    def ist_bestanden(self) -> bool:
        """Gibt True zurück wenn der Kurs bestanden wurde."""
        if self._pruefungsleistung is None:
            return False
        return self._pruefungsleistung.ist_bestanden()

    def lektion_hinzufuegen(self, name: str):
        """Fügt eine neue Lektion zum Kurs hinzu."""
        self._lektionen.append(Lektion(name))

    def lektionen_anzahl_anpassen(self, neue_anzahl: int):
        """Passt die Anzahl der Lektionen an: fügt bei Bedarf neue hinzu
        oder entfernt überzählige vom Ende der Liste."""
        if neue_anzahl < 0:
            raise ValueError(f"Anzahl Lektionen darf nicht negativ sein, war: {neue_anzahl}")
        if neue_anzahl > 20:
            raise ValueError(f"Anzahl Lektionen darf nicht größer als 20 sein, war: {neue_anzahl}")
        alte_anzahl = len(self._lektionen)
        if neue_anzahl > alte_anzahl:
            for i in range(alte_anzahl + 1, neue_anzahl + 1):
                self.lektion_hinzufuegen(f"Lektion {i}")
        elif neue_anzahl < alte_anzahl:
            self._lektionen = self._lektionen[:neue_anzahl]

    def archivieren(self):
        """Markiert den Kurs als archiviert."""
        self._archiviert = True