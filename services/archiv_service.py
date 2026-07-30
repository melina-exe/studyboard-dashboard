# services/archiv_service.py
"""Service-Klasse, die dafür sorgt, dass bestandene Kurse nach einer
Anzeigefrist automatisch aus der Dashboard-Übersicht verschwinden (aber
weiterhin in die ECTS-/Notenberechnung einfließen). Wird beim Start der
App einmal aufgerufen (siehe DashboardApp.daten_laden())."""
from datetime import date
from models.kurs import Kurs


class ArchivService:
    """Prüft regelmäßig welche Kurse archiviert werden sollen."""

    ANZEIGE_TAGE = 3  # Wie viele Tage ein bestandener Kurs noch sichtbar bleibt

    def pruefe_archivierung(self, kurse: list[Kurs]):
        """Archiviert Kurse, die lange genug bestanden sind.

        Nutzt Pruefungsleistung.eintragungsdatum als Referenzpunkt, wichtig:
        dieses Datum muss beim Laden aus der JSON-Datei korrekt wiederhergestellt
        werden (siehe ProfilRepository.laden()), sonst würde die Frist bei
        jedem Neustart der App wieder von vorne beginnen.
        """
        for kurs in kurse:
            if kurs.archiviert:
                continue
            if not kurs.ist_bestanden():
                continue
            if kurs.pruefungsleistung is None:
                continue

            tage_bestanden = (date.today() - kurs.pruefungsleistung.eintragungsdatum).days
            if tage_bestanden >= self.ANZEIGE_TAGE:
                kurs.archivieren()