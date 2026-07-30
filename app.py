# app.py
"""Hauptmodul der Anwendung: DashboardApp ist das Tk-Hauptfenster und
gleichzeitig die zentrale Koordinationsstelle - sie hält Profil und
Studiengang im Speicher, verwaltet Repository/Services und schaltet
zwischen den beiden Ansichten (Dashboard, Profil) um."""
import customtkinter as ctk
from models.profil import Profil
from models.studiengang import Studiengang
from services.studiengang_service import StudiengangService
from services.archiv_service import ArchivService
from repository.profil_repository import ProfilRepository


# Globale CustomTkinter-Einstellungen, gelten für die gesamte Anwendung
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
ctk.set_widget_scaling(1.0)


class DashboardApp(ctk.CTk):
    """Einstiegspunkt der Anwendung, koordiniert alle Views."""

    def __init__(self):
        super().__init__()
        self.title("StudyBoard")
        self.geometry("1000x700")
        self.minsize(800, 600)

        # Repository und Services
        self.repo = ProfilRepository()
        self.archiv_service = ArchivService()

        # Profil und Studiengang laden oder neu anlegen
        self.daten_laden()

        self.studiengang_service = StudiengangService(self.studiengang)

        # Archivierung prüfen, läuft einmal beim Start, damit bestandene
        # Kurse, deren Anzeigefrist abgelaufen ist, aus dem Dashboard
        # verschwinden (siehe ArchivService für Details).
        self.archiv_service.pruefe_archivierung(self.profil.kurse)

        # Views werden erst HIER importiert (nicht ganz oben in der Datei),
        # weil dashboard_view.py und profil_view.py ihrerseits Typen aus
        # diesem Modul referenzieren könnten - so werden zirkuläre Imports
        # vermieden.
        from views.dashboard_view import DashboardView
        from views.profil_view import ProfilView

        self.dashboard_view = DashboardView(self)
        self.profil_view = ProfilView(self)

        # Beim Schließen des Fensters (Klick auf X) automatisch speichern
        self.protocol("WM_DELETE_WINDOW", self.beenden)

    def starten(self):
        """Zeigt die Startansicht (Dashboard) und startet die Ereignisschleife.
        Wird von main.py aufgerufen, nachdem die App erstellt wurde."""
        self.ansicht_wechseln("dashboard")
        self.mainloop()

    def daten_laden(self):
        """Lädt Profil und Studiengang aus dem Repository, oder legt bei
        Bedarf ein leeres Profil an (z.B. beim allerersten Start, wenn noch
        keine data/profil.json existiert)."""
        ergebnis = self.repo.laden()
        if ergebnis:
            self.profil, self.studiengang = ergebnis
        else:
            self.profil = Profil("", "")
            self.studiengang = Studiengang("", 180)

    def ansicht_wechseln(self, ansicht: str):
        """Wechselt zwischen Dashboard und Profil.

        Beide Views existieren die ganze Zeit über (werden im Konstruktor
        einmal erstellt); hier wird nur die jeweils andere ausgeblendet
        (pack_forget) und die gewünschte neu aufgebaut und eingeblendet,
        damit sie immer den aktuellen Datenstand zeigt.
        """
        self.dashboard_view.pack_forget()
        self.profil_view.pack_forget()

        if ansicht == "dashboard":
            self.dashboard_view.aktualisieren()
            self.dashboard_view.pack(fill="both", expand=True)
        elif ansicht == "profil":
            self.profil_view.anzeigen()
            self.profil_view.pack(fill="both", expand=True)

    def daten_speichern(self):
        """Speichert Profil und Studiengang über das Repository. Wird nach
        jeder Änderung (Kurs hinzufügen/bearbeiten/löschen, Note eintragen,
        Lektion abhaken, ...) von den Views aufgerufen."""
        self.repo.speichern(self.profil, self.studiengang)

    def beenden(self):
        """Speichert und beendet die Anwendung (an das Schließen-Ereignis
        des Fensters gebunden, siehe __init__)."""
        self.daten_speichern()
        self.destroy()