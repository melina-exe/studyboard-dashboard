# models/kurs.py
"""Datenmodell für einen einzelnen Kurs im Studium. Die zentrale Klasse
des Fachmodells. Ein Kurs verwaltet seine eigenen Lektionen (Lernfortschritt)
und seine Pruefungsleistung (Note), berechnet daraus seinen Status und weiß,
wie lange es noch bis zur Prüfung ist."""
from datetime import date
from models.lektion import Lektion
from models.pruefungsleistung import Pruefungsleistung
from models.status import Status


class Kurs:
    """Repräsentiert einen einzelnen Kurs im Studium."""

    def __init__(self, name: str, ects: int, semester: int = 1):
        self._name = name
        # ects/semester werden bewusst über die Properties unten gesetzt
        # (nicht direkt zugewiesen), damit die Validierung auch beim
        # Erstellen eines neuen Kurses greift, nicht nur bei nachträglicher
        # Bearbeitung.
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
        """Datum der (nächsten) Prüfung, oder None wenn noch keiner feststeht
        bzw. nach einer nicht bestandenen Prüfung noch kein neuer Termin
        für den nächsten Versuch eingetragen wurde."""
        return self._pruefungstermin

    @pruefungstermin.setter
    def pruefungstermin(self, wert: date | None):
        # Realistischer Jahresbereich, damit keine Tippfehler wie "2090"
        # durchrutschen (siehe Bug-Report vom 30.07.).
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
        """True, sobald der ArchivService den Kurs archiviert hat (siehe
        archivieren()). Archivierte Kurse verschwinden aus der Dashboard-
        Übersicht, fließen aber weiterhin in die ECTS-/Notenberechnung ein."""
        return self._archiviert

    @property
    def pruefungsleistung(self) -> Pruefungsleistung | None:
        """Die zuletzt eingetragene Prüfungsleistung (Note), oder None wenn
        noch keine Note eingetragen wurde."""
        return self._pruefungsleistung

    @pruefungsleistung.setter
    def pruefungsleistung(self, wert: Pruefungsleistung | None):
        self._pruefungsleistung = wert

    @property
    def lektionen(self) -> list[Lektion]:
        """Alle Lektionen des Kurses, die nicht über lektion_entfernen()
        gelöscht wurden."""
        return [l for l in self._lektionen if not l.geloescht]

    @property
    def status(self) -> Status:
        """Abgeleiteter Status — wird aus den vorhandenen Daten berechnet,
        nicht separat gespeichert (daher '/ status' im Klassendiagramm)."""
        if self._pruefungsleistung is not None and self._pruefungsleistung.ist_bestanden():
            return Status.BESTANDEN
        if self._pruefungstermin is not None:
            return Status.AUSSTEHEND
        return Status.LAUFEND

    # -- Methoden --

    def berechne_fortschritt(self) -> float:
        """Gibt den Lernfortschritt als Prozentwert (0-100) zurück, basierend
        auf dem Anteil abgeschlossener Lektionen."""
        sichtbare = self.lektionen
        if not sichtbare:
            return 0.0
        abgeschlossen = sum(1 for l in sichtbare if l.abgeschlossen)
        return abgeschlossen / len(sichtbare) * 100

    def berechne_countdown(self) -> int | None:
        """Gibt die verbleibenden Tage bis zum Prüfungstermin zurück
        (negativ, falls der Termin bereits verstrichen ist), oder None,
        wenn (noch) kein Prüfungstermin gesetzt ist."""
        if self._pruefungstermin is None:
            return None
        delta = self._pruefungstermin - date.today()
        return delta.days

    def ist_bestanden(self) -> bool:
        """Gibt True zurück, wenn eine Prüfungsleistung existiert und diese
        bestanden ist (Note <= 4.0)."""
        if self._pruefungsleistung is None:
            return False
        return self._pruefungsleistung.ist_bestanden()

    def lektion_hinzufuegen(self, name: str):
        """Fügt eine neue Lektion zum Kurs hinzu."""
        self._lektionen.append(Lektion(name))

    def lektionen_anzahl_anpassen(self, neue_anzahl: int):
        """Passt die Anzahl der Lektionen an: fügt bei Bedarf neue hinzu
        (nummeriert fortlaufend als 'Lektion N') oder löscht überzählige
        vom Ende der Liste über lektion_entfernen(). Wird sowohl beim
        Neuanlegen als auch beim Bearbeiten eines Kurses verwendet, damit
        die Validierung nur an einer Stelle im Code gepflegt werden muss."""
        if neue_anzahl < 0:
            raise ValueError(f"Anzahl Lektionen darf nicht negativ sein, war: {neue_anzahl}")
        if neue_anzahl > 20:
            raise ValueError(f"Anzahl Lektionen darf nicht größer als 20 sein, war: {neue_anzahl}")
        sichtbare = self.lektionen
        alte_anzahl = len(sichtbare)
        if neue_anzahl > alte_anzahl:
            for i in range(alte_anzahl + 1, neue_anzahl + 1):
                self.lektion_hinzufuegen(f"Lektion {i}")
        elif neue_anzahl < alte_anzahl:
            for lektion in sichtbare[neue_anzahl:]:
                lektion.lektion_entfernen()

    def archivieren(self):
        """Markiert den Kurs als archiviert. Wird vom ArchivService
        aufgerufen, nachdem ein bestandener Kurs lange genug sichtbar war."""
        self._archiviert = True