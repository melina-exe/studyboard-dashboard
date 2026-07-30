# views/kurs_view.py
import customtkinter as ctk
from datetime import date
from models.kurs import Kurs
from models.pruefungsleistung import Pruefungsleistung
from models.status import Status

DUNKEL = "#0d0d14"
KARTEN_BG = "#13111f"
BORDER = "#1e1a2e"
LILA = "#7F77DD"
LILA_HELL = "#AFA9EC"
TEXT = "#eeedf8"
TEXT_MUTED = "#3a3a5a"
ROT = "#ff6b6b"
ORANGE = "#ffa94d"
GRÜN = "#2ecc71"


class KursView(ctk.CTkFrame):
    """Stellt einen einzelnen Kurs als Kachel dar."""

    def __init__(self, parent, kurs: Kurs, app):
        countdown = kurs.berechne_countdown()
        if kurs.status == Status.BESTANDEN:
            self._rahmen_farbe = GRÜN
        elif countdown is not None and countdown < 10:
            self._rahmen_farbe = ROT
        elif countdown is not None and countdown < 30:
            self._rahmen_farbe = ORANGE
        else:
            self._rahmen_farbe = BORDER

        super().__init__(parent, fg_color=KARTEN_BG, corner_radius=16, border_width=1, border_color=BORDER)
        self.kurs = kurs
        self.app = app
        self._aufbauen()
        self._hover_setup()

    def _hover_setup(self):
        """Setzt Hover-Effekt für den Rahmen."""
        self.bind("<Enter>", lambda e: self.configure(border_color=self._rahmen_farbe))
        self.bind("<Leave>", lambda e: self.configure(border_color=BORDER))

    def _aufbauen(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=16, pady=(16, 8))

        countdown = self.kurs.berechne_countdown()

        ctk.CTkLabel(
            header,
            text=self.kurs.name,
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=TEXT,
            wraplength=180,
            justify="left"
        ).pack(side="left", anchor="n")

        if self.kurs.status == Status.BESTANDEN:
            ctk.CTkLabel(header, text="Bestanden", text_color=GRÜN, font=ctk.CTkFont(size=12, weight="bold")).pack(side="right", anchor="n")
        elif countdown is not None:
            farbe = ROT if countdown < 10 else ORANGE if countdown < 30 else LILA_HELL
            ctk.CTkLabel(header, text=f"{countdown} Tage", text_color=farbe, font=ctk.CTkFont(size=14, weight="bold")).pack(side="right", anchor="n")

        if self.kurs.status == Status.BESTANDEN:
            balken_farbe = GRÜN
        elif countdown is not None and countdown < 10:
            balken_farbe = ROT
        elif countdown is not None and countdown < 30:
            balken_farbe = ORANGE
        else:
            balken_farbe = LILA

        fortschritt = self.kurs.berechne_fortschritt() / 100
        balken = ctk.CTkProgressBar(self, height=4, corner_radius=2, fg_color=BORDER, progress_color=balken_farbe)
        balken.pack(fill="x", padx=16, pady=(0, 4))
        balken.set(fortschritt)

        abgeschlossen = sum(1 for l in self.kurs.lektionen if l.abgeschlossen)
        gesamt = len(self.kurs.lektionen)

        info_zeile = ctk.CTkFrame(self, fg_color="transparent")
        info_zeile.pack(fill="x", padx=16, pady=(4, 12))

        if self.kurs.status == Status.BESTANDEN and self.kurs.pruefungsleistung is not None:
            note_text = f"abgeschlossen — Note {self.kurs.pruefungsleistung.note:.1f}".replace(".", ",")
            ctk.CTkLabel(info_zeile, text=note_text, font=ctk.CTkFont(size=12), text_color=GRÜN).pack(side="right")
        else:
            ctk.CTkLabel(info_zeile, text=f"Lektion {abgeschlossen} / {gesamt}", font=ctk.CTkFont(size=12), text_color=TEXT_MUTED).pack(side="right")

        if self.kurs.lektionen:
            for lektion in self.kurs.lektionen:
                farbe = balken_farbe if lektion.abgeschlossen else DUNKEL
                rand = balken_farbe if lektion.abgeschlossen else BORDER
                btn = ctk.CTkButton(
                    info_zeile,
                    text="",
                    width=14, height=14,
                    corner_radius=7,
                    fg_color=farbe,
                    hover_color=LILA,
                    border_width=1,
                    border_color=rand,
                    command=lambda l=lektion: self._lektion_abhaken(l)
                )
                btn.pack(side="left", padx=1)

        if (self.kurs.pruefungstermin is not None
                and date.today() >= self.kurs.pruefungstermin
                and self.kurs.pruefungsleistung is None):
            self._note_eingabe_anzeigen()

    def _lektion_abhaken(self, lektion):
        geklickte_index = self.kurs.lektionen.index(lektion)
        if lektion.abgeschlossen:
            for i in range(geklickte_index, len(self.kurs.lektionen)):
                self.kurs.lektionen[i].abgeschlossen = False
        else:
            for i in range(0, geklickte_index + 1):
                self.kurs.lektionen[i].abgeschlossen = True
        self.app.daten_speichern()
        self.app.ansicht_wechseln("dashboard")

    def _note_eingabe_anzeigen(self):
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(fill="x", padx=16, pady=(0, 16))

        ctk.CTkLabel(frame, text="Note:", font=ctk.CTkFont(size=12), text_color=TEXT_MUTED).pack(side="left")

        self.note_eingabe = ctk.CTkEntry(
            frame, width=60,
            placeholder_text="1.0",
            fg_color=DUNKEL,
            border_color=BORDER,
            text_color=TEXT
        )
        self.note_eingabe.pack(side="left", padx=8)

        ctk.CTkButton(
            frame,
            text="Eintragen",
            width=90,
            fg_color=LILA,
            hover_color="#6a62cc",
            text_color=TEXT,
            font=ctk.CTkFont(size=12, weight="bold"),
            corner_radius=20,
            command=self._note_eintragen
        ).pack(side="left")

    def _note_eintragen(self):
        try:
            note = float(self.note_eingabe.get().replace(",", "."))
            pl = Pruefungsleistung()
            pl.note = note
            self.kurs.pruefungsleistung = pl
            for lektion in self.kurs.lektionen:
                lektion.abgeschlossen = True
            self.app.daten_speichern()
            self.app.ansicht_wechseln("dashboard")
        except (ValueError, AttributeError):
            self.note_eingabe.configure(placeholder_text="1.0 - 5.0")