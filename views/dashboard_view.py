# views/dashboard_view.py
import customtkinter as ctk
from PIL import Image

DUNKEL = "#0d0d14"
KARTEN_BG = "#13111f"
BORDER = "#1e1a2e"
LILA = "#7F77DD"
LILA_HELL = "#AFA9EC"
TEXT = "#eeedf8"
TEXT_MUTED = "#3a3a5a"
ROT = "#ff6b6b"
ORANGE = "#ffa94d"


class DashboardView(ctk.CTkFrame):
    """Hauptansicht des Dashboards."""

    def __init__(self, app):
        super().__init__(app, fg_color=DUNKEL)
        self.app = app
        self._aufbauen()

    def _aufbauen(self):
        # -- Header --
        header = ctk.CTkFrame(self, fg_color=DUNKEL, border_width=1, border_color=BORDER, corner_radius=0)
        header.pack(fill="x", ipady=6)

        ctk.CTkLabel(header, text="StudyBoard", font=ctk.CTkFont(size=24, weight="bold", family="Georgia"), text_color=TEXT).pack(side="left", padx=24, pady=12)

        rechts = ctk.CTkFrame(header, fg_color="transparent", cursor="hand2")
        rechts.pack(side="right", padx=24, pady=8)
        rechts.bind("<Button-1>", lambda e: self.app.ansicht_wechseln("profil"))

        nutzer_frame = ctk.CTkFrame(rechts, fg_color="transparent")
        nutzer_frame.pack(side="left", padx=(0, 10))

        self.label_nutzer_name = ctk.CTkLabel(nutzer_frame, text="", font=ctk.CTkFont(family="Georgia", size=20, weight="bold"), text_color=TEXT)
        self.label_nutzer_name.pack(side="left")
        self.label_nutzer_name.bind("<Button-1>", lambda e: self.app.ansicht_wechseln("profil"))

        ctk.CTkLabel(nutzer_frame, text=" — ", font=ctk.CTkFont(size=11), text_color=TEXT_MUTED).pack(side="left")

        self.label_nutzer_sub = ctk.CTkLabel(nutzer_frame, text="", font=ctk.CTkFont(size=18), text_color=LILA_HELL)
        self.label_nutzer_sub.pack(side="left")
        self.label_nutzer_sub.bind("<Button-1>", lambda e: self.app.ansicht_wechseln("profil"))

        icon_bild = ctk.CTkImage(Image.open("assets/benutzer.png"), size=(53, 53))
        self.avatar_label = ctk.CTkLabel(rechts, text="", image=icon_bild, width=48, height=48, corner_radius=24, fg_color=DUNKEL, cursor="hand2")

        self.avatar_label.pack(side="left")
        self.avatar_label.bind("<Button-1>", lambda e: self.app.ansicht_wechseln("profil"))

        # -- Kennzahlen --
        kenn_frame = ctk.CTkFrame(self, fg_color="transparent")
        kenn_frame.pack(fill="x", padx=24, pady=14)
        kenn_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.kenn_ects = self._kennzahl_karte(kenn_frame, "ECTS erreicht", "--", "--")
        self.kenn_ects.grid(row=0, column=0, padx=(0, 8), sticky="nsew")

        self.kenn_schnitt = self._kennzahl_karte(kenn_frame, "Notendurchschnitt", "--", "gewichtet")
        self.kenn_schnitt.grid(row=0, column=1, padx=8, sticky="nsew")

        self.kenn_bestanden = self._kennzahl_karte(kenn_frame, "Kurse bestanden", "--", "--")
        self.kenn_bestanden.grid(row=0, column=2, padx=(8, 0), sticky="nsew")

        # -- Alle Kurse --
        ctk.CTkLabel(self, text="ALLE KURSE", font=ctk.CTkFont(size=15, weight="bold"), text_color=TEXT_MUTED).pack(anchor="w", padx=24)

        self.kurs_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent",scrollbar_button_color=BORDER,height=260)
        self.kurs_scroll.pack(fill="both", expand=True, padx=24, pady=(8, 0))

        # -- Countdown --
        self.countdown_frame = ctk.CTkFrame(self, fg_color=KARTEN_BG, corner_radius=16)
        self.countdown_frame.pack(fill="x", padx=24, pady=(0, 20), side="bottom")

        self.countdown_label = ctk.CTkLabel(self, text="PRÜFUNGS-COUNTDOWN", font=ctk.CTkFont(size=15, weight="bold"), text_color=TEXT_MUTED)
        self.countdown_label.pack(anchor="w", padx=24, pady=(14, 4), side="bottom")

    def _kennzahl_karte(self, parent, label, wert, sub):
        karte = ctk.CTkFrame(parent, fg_color=KARTEN_BG, corner_radius=16)
        ctk.CTkLabel(karte, text=label, font=ctk.CTkFont(size=15), text_color=LILA_HELL).pack(anchor="w", padx=20, pady=(16, 2))
        lbl_wert = ctk.CTkLabel(karte, text=wert, font=ctk.CTkFont(size=20, weight="bold"), text_color=TEXT)
        lbl_wert.pack(anchor="w", padx=20)
        lbl_sub = ctk.CTkLabel(karte, text=sub, font=ctk.CTkFont(size=15), text_color=TEXT_MUTED)
        lbl_sub.pack(anchor="w", padx=20, pady=(2, 16))
        karte._lbl_wert = lbl_wert
        karte._lbl_sub = lbl_sub
        return karte

    def aktualisieren(self):
        kurse = self.app.profil.kurse
        service = self.app.studiengang_service

        name = self.app.profil.name
        self.label_nutzer_name.configure(text=name)
        self.label_nutzer_sub.configure(text=self.app.studiengang.name)

        ects = service.berechne_bestandene_ects(kurse)
        gesamt = self.app.studiengang.gesamt_ects
        prozent = service.berechne_ects_prozent(kurse)
        schnitt = service.berechne_durchschnitt(kurse)
        bestanden = service.berechne_bestandene_kurse(kurse)

        self.kenn_ects._lbl_wert.configure(text=f"{ects} / {gesamt}")
        self.kenn_ects._lbl_sub.configure(text=f"{prozent:.0f} % abgeschlossen")
        self.kenn_schnitt._lbl_wert.configure(text=f"{schnitt:.2f}" if schnitt > 0 else "--")
        self.kenn_bestanden._lbl_wert.configure(text=f"{bestanden} / {len(kurse)}")
        self.kenn_bestanden._lbl_sub.configure(text=f"{bestanden} bestanden")

        for widget in self.kurs_scroll.winfo_children():
            widget.destroy()

        from views.kurs_view import KursView
        aktive_kurse = [k for k in kurse if not k.archiviert]

        if not aktive_kurse:
            ctk.CTkLabel(self.kurs_scroll, text="Keine aktiven Kurse. Füge Kurse im Profil hinzu.", text_color=TEXT_MUTED).pack(pady=40)
        else:
            for i, kurs in enumerate(aktive_kurse):
                kachel = KursView(self.kurs_scroll, kurs, self.app)
                kachel.grid(row=i // 2, column=i % 2, padx=6, pady=6, sticky="nsew")
            self.kurs_scroll.grid_columnconfigure(0, weight=1)
            self.kurs_scroll.grid_columnconfigure(1, weight=1)

        for widget in self.countdown_frame.winfo_children():
            widget.destroy()

        aktive_mit_termin = [k for k in kurse if not k.archiviert and k.pruefungstermin and not k.ist_bestanden()]
        if not aktive_mit_termin:
            ctk.CTkLabel(self.countdown_frame, text="Keine anstehenden Prüfungen.", text_color=TEXT_MUTED, font=ctk.CTkFont(size=12)).pack(padx=20, pady=12)
        else:
            for i, kurs in enumerate(aktive_mit_termin):
                cd = kurs.berechne_countdown()
                farbe = ROT if cd < 10 else ORANGE if cd < 30 else LILA_HELL
                if i > 0:
                    ctk.CTkFrame(self.countdown_frame, fg_color=BORDER, height=1).pack(fill="x", padx=20)
                zeile = ctk.CTkFrame(self.countdown_frame, fg_color="transparent")
                zeile.pack(fill="x", padx=20)
                ctk.CTkLabel(zeile, text=kurs.name, font=ctk.CTkFont(size=13), text_color=TEXT).pack(side="left", pady=10)
                ctk.CTkLabel(zeile, text=f"{cd} Tage", font=ctk.CTkFont(size=12, weight="bold"), text_color=farbe).pack(side="right", pady=10)