# views/profil_view.py
import customtkinter as ctk
from models.kurs import Kurs

DUNKEL = "#0d0d14"
KARTEN_BG = "#13111f"
BORDER = "#1e1a2e"
LILA = "#7F77DD"
LILA_HELL = "#AFA9EC"
TEXT = "#eeedf8"
TEXT_MUTED = "#3a3a5a"
ORANGE = "#ffa94d"
ROT_BG = "#2a1a1a"
ROT_TEXT = "#cc4444"


class ProfilView(ctk.CTkFrame):
    """Formularansicht zum Verwalten von Profil, Studiengang und Kursen."""

    def __init__(self, app):
        super().__init__(app, fg_color=DUNKEL)
        self.app = app
        self._aufbauen()

    @property
    def profil(self):
        """Das aktuell verwaltete Profil (delegiert an die App)."""
        return self.app.profil

    def _aufbauen(self):
        header = ctk.CTkFrame(self, fg_color=DUNKEL, border_width=1, border_color=BORDER, corner_radius=0)
        header.pack(fill="x", ipady=6)

        ctk.CTkLabel(header, text="Profil", font=ctk.CTkFont(family="Georgia", size=22, weight="bold"), text_color=TEXT).pack(side="left", padx=24, pady=12)

        ctk.CTkButton(
            header, text="Zurück", width=90,
            fg_color="transparent", hover_color=KARTEN_BG,
            border_width=1, border_color=LILA,
            text_color=LILA_HELL, corner_radius=20,
            font=ctk.CTkFont(size=15),
            command=lambda: self.app.ansicht_wechseln("dashboard")
        ).pack(side="right", padx=24, pady=10)

        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent", scrollbar_button_color=BORDER)
        self.scroll.pack(fill="both", expand=True, padx=24, pady=20)

    def anzeigen(self):
        for widget in self.scroll.winfo_children():
            widget.destroy()
        self._akkordeon("Profildaten", self._profildaten_inhalt, offen=False)
        self._akkordeon("Kurs hinzufügen", self._kurs_hinzufuegen_inhalt, offen=True)
        self._kurse_akkordeons()
        self.archivierte_anzeigen()

    def _profildaten_inhalt(self, parent):
        self.e_name = self._feld(parent, "Name", wert=self.app.profil.name)
        self.e_sg_name = self._feld(parent, "Studiengang", wert=self.app.studiengang.name)
        self.e_sg_ects = self._feld(parent, "Gesamt-ECTS", wert=str(self.app.studiengang.gesamt_ects))
        self._speichern_btn(parent, self._profildaten_speichern)

    def _akkordeon(self, titel, inhalt_fn, offen=True):
        container = ctk.CTkFrame(self.scroll, fg_color=KARTEN_BG, corner_radius=16)
        container.pack(fill="x", pady=5)

        header = ctk.CTkFrame(container, fg_color="transparent", cursor="hand2")
        header.pack(fill="x")

        ctk.CTkLabel(header, text=titel.upper(), font=ctk.CTkFont(size=15, weight="bold"), text_color=LILA_HELL).pack(side="left", padx=20, pady=14)

        from PIL import Image
        icon_unten = ctk.CTkImage(Image.open("assets/pfeil_unten.png"), size=(16, 16))
        icon_rechts = ctk.CTkImage(Image.open("assets/pfeil_rechts.png"), size=(16, 16))

        pfeil = ctk.CTkLabel(header, text="", image=icon_unten if offen else icon_rechts, width=24, height=24, fg_color="transparent")
        pfeil.pack(side="right", padx=20)

        body = ctk.CTkFrame(container, fg_color="transparent")
        if offen:
            body.pack(fill="x", padx=20, pady=(0, 16))

        def toggle(e=None):
            if body.winfo_ismapped():
                body.pack_forget()
                pfeil.configure(image=icon_rechts)
            else:
                body.pack(fill="x", padx=20, pady=(0, 16))
                pfeil.configure(image=icon_unten)

        header.bind("<Button-1>", toggle)
        for widget in header.winfo_children():
            widget.bind("<Button-1>", toggle)

        inhalt_fn(body)

    def _kurse_akkordeons(self):
        aktive_kurse = [k for k in self.app.profil.kurse if not k.archiviert]

        if not aktive_kurse:
            leer = ctk.CTkFrame(self.scroll, fg_color=KARTEN_BG, corner_radius=16)
            leer.pack(fill="x", pady=5)
            ctk.CTkLabel(leer, text="Noch keine Kurse vorhanden.", text_color=TEXT_MUTED, font=ctk.CTkFont(size=13)).pack(padx=20, pady=16)
            return

        semester_dict: dict[int, list[Kurs]] = {}
        for kurs in aktive_kurse:
            semester_dict.setdefault(kurs.semester, []).append(kurs)

        for semester_nr in sorted(semester_dict.keys()):
            kurse = semester_dict[semester_nr]
            self._akkordeon(
                f"Semester {semester_nr}",
                lambda body, k=kurse: self._semester_inhalt(body, k),
                offen=True
            )

    def archivierte_anzeigen(self):
        """Zeigt archivierte Kurse (aus abgeschlossenen Semestern) in einem eigenen,
        eingeklappten Bereich an. Archivierte Kurse können hier weiterhin gelöscht,
        aber nicht mehr bearbeitet werden."""
        archivierte_kurse = [k for k in self.app.profil.kurse if k.archiviert]
        if not archivierte_kurse:
            return

        self._akkordeon(
            f"Archivierte Kurse ({len(archivierte_kurse)})",
            lambda body, k=archivierte_kurse: self._archiviert_inhalt(body, k),
            offen=False
        )

    def _archiviert_inhalt(self, parent, kurse):
        for kurs in kurse:
            zeile = ctk.CTkFrame(parent, fg_color="transparent")
            zeile.pack(fill="x")

            ctk.CTkLabel(zeile, text=kurs.name, font=ctk.CTkFont(size=13), text_color=TEXT_MUTED, anchor="w").pack(side="left", pady=8)
            ctk.CTkLabel(zeile, text=f"{kurs.ects} ECTS", font=ctk.CTkFont(size=11), text_color=TEXT_MUTED).pack(side="left", padx=8)

            if kurs.pruefungsleistung is not None:
                note_text = f"Note {kurs.pruefungsleistung.note:.1f}".replace(".", ",")
                ctk.CTkLabel(zeile, text=note_text, font=ctk.CTkFont(size=11), text_color=TEXT_MUTED).pack(side="left", padx=8)

            ctk.CTkButton(
                zeile, text="Löschen", width=75,
                fg_color=ROT_BG, hover_color="#4a2a2a",
                text_color=ROT_TEXT, corner_radius=12,
                font=ctk.CTkFont(size=11),
                command=lambda k=kurs: self._kurs_loeschen(k)
            ).pack(side="right", padx=(4, 0), pady=6)

            ctk.CTkFrame(parent, fg_color=BORDER, height=1).pack(fill="x", pady=2)

    def _feld(self, parent, label, placeholder="", wert=""):
        zeile = ctk.CTkFrame(parent, fg_color="transparent")
        zeile.pack(fill="x", pady=4)
        ctk.CTkLabel(zeile, text=label, width=140, anchor="w", font=ctk.CTkFont(size=12), text_color=TEXT_MUTED).pack(side="left")
        entry = ctk.CTkEntry(zeile, placeholder_text=placeholder, fg_color=DUNKEL, border_color=BORDER, text_color=TEXT, width=260)
        if wert:
            entry.insert(0, wert)
        entry.pack(side="left")
        return entry

    def _studiengang_inhalt(self, parent):
        self.e_sg_name = self._feld(parent, "Name", wert=self.app.studiengang.name)
        self.e_sg_ects = self._feld(parent, "Gesamt-ECTS", wert=str(self.app.studiengang.gesamt_ects))
        self._speichern_btn(parent, self._studiengang_speichern)

    def _profil_inhalt(self, parent):
        self.e_name = self._feld(parent, "Name", wert=self.app.profil.name)
        self.e_matr = self._feld(parent, "Matrikelnummer", wert=self.app.profil.matrikelnummer)
        self._speichern_btn(parent, self._profil_speichern)

    def _kurs_hinzufuegen_inhalt(self, parent):
        self.e_kursname = self._feld(parent, "Kursname", placeholder="z.B. Analysis")
        self.e_kurs_ects = self._feld(parent, "ECTS", placeholder="5")
        self.e_semester = self._feld(parent, "Semester", placeholder="1")

        datum_zeile = ctk.CTkFrame(parent, fg_color="transparent")
        datum_zeile.pack(fill="x", pady=4)
        ctk.CTkLabel(datum_zeile, text="Prüfungstermin", width=140, anchor="w", font=ctk.CTkFont(size=12), text_color=TEXT_MUTED).pack(side="left")
        self.e_tag = ctk.CTkEntry(datum_zeile, width=52, placeholder_text="TT", fg_color=DUNKEL, border_color=BORDER, text_color=TEXT)
        self.e_tag.pack(side="left")
        ctk.CTkLabel(datum_zeile, text=".", text_color=TEXT_MUTED).pack(side="left", padx=2)
        self.e_monat = ctk.CTkEntry(datum_zeile, width=52, placeholder_text="MM", fg_color=DUNKEL, border_color=BORDER, text_color=TEXT)
        self.e_monat.pack(side="left")
        ctk.CTkLabel(datum_zeile, text=".", text_color=TEXT_MUTED).pack(side="left", padx=2)
        self.e_jahr = ctk.CTkEntry(datum_zeile, width=72, placeholder_text="JJJJ", fg_color=DUNKEL, border_color=BORDER, text_color=TEXT)
        self.e_jahr.pack(side="left")
        ctk.CTkLabel(datum_zeile, text="optional", font=ctk.CTkFont(size=11), text_color=TEXT_MUTED).pack(side="left", padx=8)

        self.e_lektionen = self._feld(parent, "Anzahl Lektionen", placeholder="z.B. 8")

        self.fehler_label = ctk.CTkLabel(parent, text="", text_color="red", font=ctk.CTkFont(size=11))
        self.fehler_label.pack(anchor="w", pady=2)

        ctk.CTkButton(
            parent, text="Kurs hinzufügen",
            fg_color=LILA, hover_color="#6a62cc",
            text_color=TEXT, font=ctk.CTkFont(size=12, weight="bold"),
            corner_radius=20, command=self._kurs_hinzufuegen
        ).pack(anchor="e", pady=8)

    def _semester_inhalt(self, parent, kurse):
        for kurs in kurse:
            kurs_container = ctk.CTkFrame(parent, fg_color="transparent")
            kurs_container.pack(fill="x")

            zeile = ctk.CTkFrame(kurs_container, fg_color="transparent")
            zeile.pack(fill="x")

            status_farbe = {"laufend": LILA, "ausstehend": ORANGE, "bestanden": LILA_HELL}.get(kurs.status.value, TEXT_MUTED)
            ctk.CTkLabel(zeile, text=kurs.name, font=ctk.CTkFont(size=13), text_color=TEXT, anchor="w").pack(side="left", pady=8)
            ctk.CTkLabel(zeile, text=f"{kurs.ects} ECTS", font=ctk.CTkFont(size=11), text_color=TEXT_MUTED).pack(side="left", padx=8)

            ctk.CTkButton(
                zeile, text="Löschen", width=75,
                fg_color=ROT_BG, hover_color="#4a2a2a",
                text_color=ROT_TEXT, corner_radius=12,
                font=ctk.CTkFont(size=11),
                command=lambda k=kurs: self._kurs_loeschen(k)
            ).pack(side="right", padx=(4, 0), pady=6)

            ctk.CTkButton(
                zeile, text="Bearbeiten", width=85,
                fg_color="transparent", hover_color=DUNKEL,
                border_width=1, border_color=BORDER,
                text_color=LILA_HELL, corner_radius=12,
                font=ctk.CTkFont(size=11),
                command=lambda k=kurs, c=kurs_container: self._bearbeiten_aufklappen(k, c)
            ).pack(side="right", pady=6)

            ctk.CTkFrame(parent, fg_color=BORDER, height=1).pack(fill="x", pady=2)

    def _bearbeiten_aufklappen(self, kurs: Kurs, container: ctk.CTkFrame):
        for widget in container.winfo_children():
            if hasattr(widget, "_ist_bearbeitungsformular"):
                widget.destroy()
                return

        formular = ctk.CTkFrame(container, fg_color=DUNKEL, corner_radius=8)
        formular._ist_bearbeitungsformular = True
        formular.pack(fill="x", pady=6)

        def feld(label, placeholder="", wert=""):
            zeile = ctk.CTkFrame(formular, fg_color="transparent")
            zeile.pack(fill="x", pady=3)
            ctk.CTkLabel(zeile, text=label, width=140, anchor="w", font=ctk.CTkFont(size=12), text_color=TEXT_MUTED).pack(side="left")
            e = ctk.CTkEntry(zeile, placeholder_text=placeholder, fg_color=DUNKEL, border_color=BORDER, text_color=TEXT, width=220)
            if wert:
                e.insert(0, wert)
            e.pack(side="left")
            return e

        datum_zeile = ctk.CTkFrame(formular, fg_color="transparent")
        datum_zeile.pack(fill="x", pady=3)
        ctk.CTkLabel(datum_zeile, text="Prüfungstermin", width=140, anchor="w", font=ctk.CTkFont(size=12), text_color=TEXT_MUTED).pack(side="left")
        e_tag = ctk.CTkEntry(datum_zeile, width=52, placeholder_text="TT", fg_color=DUNKEL, border_color=BORDER, text_color=TEXT)
        e_tag.pack(side="left")
        ctk.CTkLabel(datum_zeile, text=".", text_color=TEXT_MUTED).pack(side="left", padx=2)
        e_monat = ctk.CTkEntry(datum_zeile, width=52, placeholder_text="MM", fg_color=DUNKEL, border_color=BORDER, text_color=TEXT)
        e_monat.pack(side="left")
        ctk.CTkLabel(datum_zeile, text=".", text_color=TEXT_MUTED).pack(side="left", padx=2)
        e_jahr = ctk.CTkEntry(datum_zeile, width=72, placeholder_text="JJJJ", fg_color=DUNKEL, border_color=BORDER, text_color=TEXT)
        e_jahr.pack(side="left")

        if kurs.pruefungstermin:
            e_tag.insert(0, str(kurs.pruefungstermin.day))
            e_monat.insert(0, str(kurs.pruefungstermin.month))
            e_jahr.insert(0, str(kurs.pruefungstermin.year))

        e_lektionen = feld("Anzahl Lektionen", placeholder="z.B. 8", wert=str(len(kurs.lektionen)) if kurs.lektionen else "")
        e_ects = feld("ECTS", wert=str(kurs.ects))
        e_semester = feld("Semester", wert=str(kurs.semester))

        fehler = ctk.CTkLabel(formular, text="", text_color="red", font=ctk.CTkFont(size=11))
        fehler.pack(anchor="w")

        def speichern():
            from datetime import date

            # -- 1. Alle Eingaben validieren, ohne den Kurs zu verändern --
            tag = e_tag.get().strip()
            monat = e_monat.get().strip()
            jahr = e_jahr.get().strip()
            neuer_termin = kurs.pruefungstermin
            if tag or monat or jahr:
                try:
                    neuer_termin = date(int(jahr), int(monat), int(tag))
                except ValueError:
                    fehler.configure(text="Bitte gültiges Datum eingeben.")
                    return
            else:
                neuer_termin = None

            try:
                neue_ects = int(e_ects.get())
                neues_semester = int(e_semester.get())
            except ValueError:
                fehler.configure(text="ECTS und Semester müssen Zahlen sein.")
                return

            anzahl = e_lektionen.get().strip()
            neue_lektionen_anzahl = None
            if anzahl:
                try:
                    neue_lektionen_anzahl = int(anzahl)
                except ValueError:
                    fehler.configure(text="Anzahl muss eine Zahl sein.")
                    return

            # -- 2. Erst jetzt, wenn alles gültig ist, die Änderungen anwenden --
            try:
                kurs.ects = neue_ects
                kurs.semester = neues_semester
            except ValueError as e:
                fehler.configure(text=str(e))
                return

            kurs.pruefungstermin = neuer_termin

            if neue_lektionen_anzahl is not None:
                kurs.lektionen_anzahl_anpassen(neue_lektionen_anzahl)

            self.app.daten_speichern()
            self.anzeigen()

        ctk.CTkButton(
            formular, text="Speichern",
            fg_color=LILA, hover_color="#6a62cc",
            text_color=TEXT, font=ctk.CTkFont(size=12, weight="bold"),
            corner_radius=20, command=speichern
        ).pack(anchor="e", pady=8)

    def _speichern_btn(self, parent, command):
        ctk.CTkButton(
            parent, text="Speichern",
            fg_color="transparent", hover_color=DUNKEL,
            border_width=1, border_color=LILA,
            text_color=LILA_HELL, corner_radius=20,
            font=ctk.CTkFont(size=12),
            command=command
        ).pack(anchor="e", pady=8)

    
    def _profildaten_speichern(self):
        self.app.profil._name = self.e_name.get()
        self.app.studiengang.name = self.e_sg_name.get()
        try:
            self.app.studiengang.gesamt_ects = int(self.e_sg_ects.get())
        except ValueError:
            pass
        self.app.daten_speichern()

    def _kurs_hinzufuegen(self):
        name = self.e_kursname.get().strip()
        if not name:
            self.fehler_label.configure(text="Kursname darf nicht leer sein.")
            return
        try:
            ects = int(self.e_kurs_ects.get())
            semester = int(self.e_semester.get())
        except ValueError:
            self.fehler_label.configure(text="ECTS und Semester müssen Zahlen sein.")
            return
        try:
            kurs = Kurs(name, ects, semester)
        except ValueError as e:
            self.fehler_label.configure(text=str(e))
            return
        tag = self.e_tag.get().strip()
        monat = self.e_monat.get().strip()
        jahr = self.e_jahr.get().strip()
        if tag or monat or jahr:
            try:
                from datetime import date
                kurs.pruefungstermin = date(int(jahr), int(monat), int(tag))
            except ValueError:
                self.fehler_label.configure(text="Bitte gültiges Datum eingeben.")
                return
        anzahl = self.e_lektionen.get().strip()
        if anzahl:
            try:
                for i in range(1, int(anzahl) + 1):
                    kurs.lektion_hinzufuegen(f"Lektion {i}")
            except ValueError:
                self.fehler_label.configure(text="Anzahl Lektionen muss eine Zahl sein.")
                return
        self.app.profil.kurs_hinzufuegen(kurs)
        self.app.daten_speichern()
        self.anzeigen()

    def _kurs_loeschen(self, kurs):
        self.app.profil.kurs_entfernen(kurs)
        self.app.daten_speichern()
        self.anzeigen()