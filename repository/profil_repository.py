# repository/profil_repository.py
"""Repository-Klasse für die Persistierung: kapselt das Lesen/Schreiben der
Profildaten als JSON-Datei, damit der Rest der Anwendung (Views, Services)
nichts vom Speicherformat wissen muss."""
import json
from datetime import date
from models.profil import Profil
from models.studiengang import Studiengang
from models.kurs import Kurs
from models.lektion import Lektion
from models.pruefungsleistung import Pruefungsleistung


class ProfilRepository:
    """Kümmert sich um das Speichern und Laden des Profils als JSON-Datei."""

    def __init__(self, dateipfad: str = "data/profil.json"):
        self._dateipfad = dateipfad

    def speichern(self, profil: Profil, studiengang: Studiengang):
        """Serialisiert Profil, Studiengang und alle Kurse (inkl. Lektionen
        und Prüfungsleistung) als JSON-Datei. Überschreibt die Datei komplett
        bei jedem Aufruf (kein inkrementelles Update)."""
        daten = {
            "profil": {
                "name": profil.name,
                "matrikelnummer": profil.matrikelnummer,
            },
            "studiengang": {
                "name": studiengang.name,
                "gesamt_ects": studiengang.gesamt_ects,
            },
            "kurse": []
        }

        for kurs in profil.kurse:
            kurs_daten = {
                "name": kurs.name,
                "ects": kurs.ects,
                "semester": kurs.semester,
                "pruefungstermin": kurs.pruefungstermin.isoformat() if kurs.pruefungstermin else None,
                "archiviert": kurs.archiviert,
                "lektionen": [
                    {"name": l.name, "abgeschlossen": l.abgeschlossen}
                    for l in kurs.lektionen
                ],
                # eintragungsdatum wird mitgespeichert, damit der ArchivService
                # beim nächsten Laden korrekt weiterzählen kann (siehe laden()
                # unten und die ausführliche Erklärung im ArchivService).
                "pruefungsleistung": {
                    "note": kurs.pruefungsleistung.note,
                    "eintragungsdatum": kurs.pruefungsleistung.eintragungsdatum.isoformat()
                } if kurs.pruefungsleistung else None
            }
            daten["kurse"].append(kurs_daten)

        with open(self._dateipfad, "w", encoding="utf-8") as f:
            json.dump(daten, f, ensure_ascii=False, indent=2)

    def laden(self) -> tuple[Profil, Studiengang] | None:
        """Lädt Profil und Studiengang aus der JSON-Datei.

        Gibt None zurück, wenn noch keine Datei existiert (z.B. beim allerersten
        Start der App), DashboardApp.daten_laden() legt in diesem Fall ein
        leeres Profil an.
        """
        try:
            with open(self._dateipfad, "r", encoding="utf-8") as f:
                daten = json.load(f)
        except FileNotFoundError:
            return None

        profil = Profil(
            name=daten["profil"]["name"],
            matrikelnummer=daten["profil"]["matrikelnummer"]
        )

        studiengang = Studiengang(
            name=daten["studiengang"]["name"],
            gesamt_ects=daten["studiengang"]["gesamt_ects"]
        )

        for k in daten["kurse"]:
            kurs = Kurs(
                name=k["name"],
                ects=k["ects"],
                semester=k.get("semester", 1)  # get() für Abwärtskompatibilität mit älteren Datenständen ohne "semester"
            )

            if k["pruefungstermin"]:
                kurs.pruefungstermin = date.fromisoformat(k["pruefungstermin"])

            if k["archiviert"]:
                kurs.archivieren()

            for l in k["lektionen"]:
                kurs.lektion_hinzufuegen(l["name"])
                if l["abgeschlossen"]:
                    kurs.lektionen[-1].abgeschlossen = True

            if k["pruefungsleistung"]:
                pl = Pruefungsleistung()
                pl.note = k["pruefungsleistung"]["note"]
                # Wichtig: das gespeicherte Eintragungsdatum wiederherstellen,
                # statt es (wie im Pruefungsleistung-Konstruktor) automatisch
                # auf "heute" zu setzen, sonst würde die Archivierungs-Frist
                # bei jedem Laden neu beginnen.
                pl.eintragungsdatum = date.fromisoformat(k["pruefungsleistung"]["eintragungsdatum"])
                profil.kurs_hinzufuegen(kurs)
                kurs.pruefungsleistung = pl

            else:
                profil.kurs_hinzufuegen(kurs)

        return profil, studiengang