# services/archiv_service.py
from datetime import date
from models.kurs import Kurs


class ArchivService:
    """Prüft regelmäßig welche Kurse archiviert werden sollen."""

    ANZEIGE_TAGE = 3  # Wie viele Tage ein bestandener Kurs noch sichtbar bleibt

    def pruefe_archivierung(self, kurse: list[Kurs]):
        """Archiviert Kurse die lange genug bestanden sind."""
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