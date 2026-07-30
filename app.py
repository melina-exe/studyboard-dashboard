# app.py
import customtkinter as ctk
from models.profil import Profil
from models.studiengang import Studiengang
from services.studiengang_service import StudiengangService
from services.archiv_service import ArchivService
from repository.profil_repository import ProfilRepository


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

        # Archivierung prüfen
        self.archiv_service.pruefe_archivierung(self.profil.kurse)

        # Views importieren hier (verhindert zirkuläre Imports)
        from views.dashboard_view import DashboardView
        from views.profil_view import ProfilView

        self.dashboard_view = DashboardView(self)
        self.profil_view = ProfilView(self)

        # Beim Schließen speichern
        self.protocol("WM_DELETE_WINDOW", self.beenden)

    def starten(self):
        """Zeigt die Startansicht (Dashboard) und startet die Ereignisschleife."""
        self.ansicht_wechseln("dashboard")
        self.mainloop()

    def daten_laden(self):
        """Lädt Profil und Studiengang aus dem Repository, oder legt bei Bedarf ein leeres Profil an."""
        ergebnis = self.repo.laden()
        if ergebnis:
            self.profil, self.studiengang = ergebnis
        else:
            self.profil = Profil("", "")
            self.studiengang = Studiengang("", 180)

    def ansicht_wechseln(self, ansicht: str):
        """Wechselt zwischen Dashboard und Profil."""
        self.dashboard_view.pack_forget()
        self.profil_view.pack_forget()

        if ansicht == "dashboard":
            self.dashboard_view.aktualisieren()
            self.dashboard_view.pack(fill="both", expand=True)
        elif ansicht == "profil":
            self.profil_view.anzeigen()
            self.profil_view.pack(fill="both", expand=True)

    def daten_speichern(self):
        """Speichert Profil und Studiengang."""
        self.repo.speichern(self.profil, self.studiengang)

    def beenden(self):
        """Speichert und beendet die Anwendung."""
        self.daten_speichern()
        self.destroy()