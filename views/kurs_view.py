# views/kurs_view.py
"""Kurskachel-Ansicht: stellt einen einzelnen Kurs als Karte dar (Titel,
Status, Fortschrittsbalken, Lektionen-Punkte) und übernimmt außerdem das
Abhaken von Lektionen sowie die Noteneingabe inkl. Retry-Logik nach einer
nicht bestandenen Prüfung."""
import customtkinter as ctk
from datetime import date
from models.kurs import Kurs
from models.pruefungsleistung import Pruefungsleistung
from models.status import Status

# Design-Farbpalette, siehe dashboard_view.py für die gleiche Palette
DUNKEL = "#0d0d14"
KARTEN_BG = "#13111f"
BORDER = "#1e1a2e"
LILA = "#7F77DD"
LILA_HELL = "#AFA9EC"
TEXT = "#eeedf8"
TEXT_MUTED = "#3a3a5a"
PLATZHALTER = "#5b5b7d"
ROT = "#ff6b6b"
ORANGE = "#ffa94d"
GRÜN = "#2ecc71"


class KursView(ctk.CTkFrame):
    """Stellt einen einzelnen Kurs als Kachel dar."""

    def __init__(self, parent, kurs: Kurs, app):
        # Rahmenfarbe wird einmalig beim Erstellen berechnet (nicht bei jedem
        # Hover neu), da sie sich nur ändert, wenn sich der Kurs selbst ändert
        # (und dann wird die Kachel eh komplett neu erzeugt, siehe
        # DashboardView.aktualisieren()).
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
        """Setzt Hover-Effekt für den Rahmen.

        Enter/Leave wird auf ALLE Kind-Widgets rekursiv gebunden, da Tkinter
        beim Überqueren von Kind-Widgets innerhalb des Frames sonst ständig
        Leave- und Enter-Events auf dem äußeren Frame auslöst (jedes Kind-Widget
        ist technisch ein eigenes Fenster) -> ohne das flackert der Rahmen.
        """
        def eintreten(_event):
            self.configure(border_color=self._rahmen_farbe)

        def verlassen(_event):
            self.configure(border_color=BORDER)

        self._hover_binden(self, eintreten, verlassen)

    def _hover_binden(self, widget, eintreten, verlassen):
        """Bindet Enter/Leave rekursiv an ein Widget und alle seine Kinder.
        add='+' sorgt dafür, dass bestehende Bindings des Widgets (z.B. von
        CustomTkinter selbst) nicht überschrieben, sondern ergänzt werden."""
        widget.bind("<Enter>", eintreten, add="+")
        widget.bind("<Leave>", verlassen, add="+")
        for kind in widget.winfo_children():
            self._hover_binden(kind, eintreten, verlassen)

    def _aufbauen(self):
        # nicht_bestanden = es wurde bereits eine Note eingetragen, aber der
        # Kurs wurde NICHT bestanden (Note > 4.0). Wichtig: das ist bewusst
        # unabhängig von kurs.status, weil der Prüfungstermin nach einem
        # Fehlversuch zurückgesetzt wird (siehe _note_eintragen) und status
        # in dem Fall auf LAUFEND fallen würde, obwohl klar eine gescheiterte
        # Prüfungsleistung vorliegt.
        nicht_bestanden = (
            self.kurs.pruefungsleistung is not None
            and not self.kurs.pruefungsleistung.ist_bestanden()
        )

        # -- Kopfzeile: Kursname links, Status rechts --
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(16, 8))

        countdown = self.kurs.berechne_countdown()

        ctk.CTkLabel(
            header,
            text=self.kurs.name,
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=TEXT,
            wraplength=180,
            justify="left"
        ).pack(side="left", anchor="n")

        # Statusanzeige rechts oben: Priorität ist bestanden > nicht bestanden > Countdown
        if self.kurs.status == Status.BESTANDEN:
            ctk.CTkLabel(header, text="Bestanden", text_color=GRÜN, font=ctk.CTkFont(size=12, weight="bold")).pack(side="right", anchor="n")
        elif nicht_bestanden:
            ctk.CTkLabel(header, text="Nicht bestanden", text_color=ROT, font=ctk.CTkFont(size=12, weight="bold")).pack(side="right", anchor="n")
        elif countdown is not None:
            # Farbcodierung nach Dringlichkeit (Ziel 4): rot < 10 Tage, orange < 30 Tage, sonst neutral (violett)
            farbe = ROT if countdown < 10 else ORANGE if countdown < 30 else LILA_HELL
            ctk.CTkLabel(header, text=f"{countdown} Tage", text_color=farbe, font=ctk.CTkFont(size=14, weight="bold")).pack(side="right", anchor="n")

        # -- Fortschrittsbalken (gleiche Farblogik wie der Status oben) --
        if self.kurs.status == Status.BESTANDEN:
            balken_farbe = GRÜN
        elif nicht_bestanden:
            balken_farbe = ROT
        elif countdown is not None and countdown < 10:
            balken_farbe = ROT
        elif countdown is not None and countdown < 30:
            balken_farbe = ORANGE
        else:
            balken_farbe = LILA

        fortschritt = self.kurs.berechne_fortschritt() / 100
        balken = ctk.CTkProgressBar(self, height=4, corner_radius=2, fg_color=BORDER, progress_color=balken_farbe)
        balken.pack(fill="x", padx=20, pady=(0, 4))
        balken.set(fortschritt)

        abgeschlossen = sum(1 for l in self.kurs.lektionen if l.abgeschlossen)
        gesamt = len(self.kurs.lektionen)

        # -- Info-Zeile: Lektionen-Punkte links, Notentext/Lektionenzähler rechts --
        info_zeile = ctk.CTkFrame(self, fg_color="transparent")
        info_zeile.pack(fill="x", padx=20, pady=(4, 12))

        if self.kurs.status == Status.BESTANDEN and self.kurs.pruefungsleistung is not None:
            note_text = f"abgeschlossen — Note {self.kurs.pruefungsleistung.note:.1f}".replace(".", ",")
            ctk.CTkLabel(info_zeile, text=note_text, font=ctk.CTkFont(size=12), text_color=GRÜN).pack(side="right")
            self._korrigieren_button(info_zeile)
        elif nicht_bestanden:
            note_text = f"Note {self.kurs.pruefungsleistung.note:.1f}".replace(".", ",")
            ctk.CTkLabel(info_zeile, text=note_text, font=ctk.CTkFont(size=12), text_color=ROT).pack(side="right")
            self._korrigieren_button(info_zeile)
        else:
            ctk.CTkLabel(info_zeile, text=f"Lektion {abgeschlossen} / {gesamt}", font=ctk.CTkFont(size=12), text_color=TEXT_MUTED).pack(side="right")

        # Ein kleiner runder Button pro Lektion, anklickbar zum Abhaken.
        # Maximal 20 Lektionen pro Kurs (siehe Kurs.lektionen_anzahl_anpassen),
        # daher bewusst in EINER Reihe ohne Umbruch - das Grid im DashboardView
        # (uniform-Gruppe) sorgt trotzdem für gleich breite Kacheln.
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

        # zeigt_noteneingabe entscheidet, ob das Eingabefeld für eine neue
        # Note angezeigt wird: entweder beim allerersten Versuch (noch keine
        # Pruefungsleistung vorhanden) oder bei einem Retry nach einem
        # Fehlversuch (nicht_bestanden), sobald der (neu eingetragene)
        # Prüfungstermin erreicht ist.
        zeigt_noteneingabe = (
            self.kurs.pruefungstermin is not None
            and date.today() >= self.kurs.pruefungstermin
            and (self.kurs.pruefungsleistung is None or nicht_bestanden)
        )

        # Hinweistext nur zeigen, wenn das Eingabefeld NICHT sowieso schon da
        # ist (sonst wäre die Meldung redundant/verwirrend neben dem Feld).
        if nicht_bestanden and not zeigt_noteneingabe:
            hinweis = ctk.CTkFrame(self, fg_color="transparent")
            hinweis.pack(fill="x", padx=20, pady=(0, 16))
            if self.kurs.pruefungstermin is None:
                # Fehlversuch, aber noch kein neuer Termin für den nächsten Versuch gesetzt
                text = "Nicht bestanden — kein Problem! Trag im Profil einen neuen Prüfungstermin für deinen nächsten Versuch ein."
                farbe = ROT
            else:
                # Neuer Termin ist schon gesetzt, liegt aber noch in der Zukunft
                text = f"Nächster Versuch geplant am {self.kurs.pruefungstermin.strftime('%d.%m.%Y')}. Viel Erfolg!"
                farbe = LILA_HELL
            ctk.CTkLabel(
                hinweis, text=text, font=ctk.CTkFont(size=11),
                text_color=farbe, wraplength=380, justify="left"
            ).pack(anchor="w")

        if zeigt_noteneingabe:
            self._note_eingabe_anzeigen()

    def _lektion_abhaken(self, lektion):
        """Markiert eine Lektion (und alle davor) als abgeschlossen, bzw.
        macht das rückgängig (und alle danach), wenn sie schon abgeschlossen
        war. Die Lektionen bauen also aufeinander auf: man kann nicht
        Lektion 5 abhaken, ohne dass 1-4 automatisch mit abgehakt werden -
        und umgekehrt reißt das Abwählen einer Lektion alle späteren mit."""
        geklickte_index = self.kurs.lektionen.index(lektion)
        if lektion.abgeschlossen:
            for i in range(geklickte_index, len(self.kurs.lektionen)):
                self.kurs.lektionen[i].abgeschlossen = False
        else:
            for i in range(0, geklickte_index + 1):
                self.kurs.lektionen[i].abgeschlossen = True
        self.app.daten_speichern()
        self.app.ansicht_wechseln("dashboard")  # baut die Ansicht neu auf, damit der Fortschrittsbalken sofort aktualisiert wird

    def _note_eingabe_anzeigen(self):
        """Baut das Eingabefeld + Button zum Eintragen einer Note auf.
        Wird nur aufgerufen, wenn zeigt_noteneingabe (siehe _aufbauen) True ist."""
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(fill="x", padx=20, pady=(0, 16))

        zeile = ctk.CTkFrame(frame, fg_color="transparent")
        zeile.pack(fill="x")

        ctk.CTkLabel(zeile, text="Note:", font=ctk.CTkFont(size=12), text_color=TEXT_MUTED).pack(side="left")

        self.note_eingabe = ctk.CTkEntry(
            zeile, width=60,
            placeholder_text="z.B. 1,7",
            placeholder_text_color=PLATZHALTER,
            fg_color=DUNKEL,
            border_color=BORDER,
            text_color=TEXT
        )
        self.note_eingabe.pack(side="left", padx=8)

        ctk.CTkButton(
            zeile,
            text="Eintragen",
            width=90,
            fg_color=LILA,
            hover_color="#6a62cc",
            text_color=TEXT,
            font=ctk.CTkFont(size=12, weight="bold"),
            corner_radius=20,
            command=self._note_eintragen
        ).pack(side="left")

        self.note_fehler_label = ctk.CTkLabel(frame, text="", text_color=ROT, font=ctk.CTkFont(size=11))
        self.note_fehler_label.pack(anchor="w", pady=(4, 0))

    def _note_eintragen(self):
        """Validiert die eingegebene Note und trägt sie ein.

        Reihenfolge wichtig: erst die Zahl parsen, dann die Note validieren
        (1.0-5.0 über Pruefungsleistung.note), und erst wenn BEIDES gültig
        ist, die Änderungen am Kurs vornehmen - so bleibt der Kurs bei einer
        ungültigen Eingabe unverändert (kein Partial-Save).
        """
        eingabe = self.note_eingabe.get().strip().replace(",", ".")  # deutsches Komma als Dezimaltrennzeichen erlauben
        try:
            note = float(eingabe)
        except ValueError:
            self.note_fehler_label.configure(text="Bitte eine Zahl eingeben (z.B. 1,7).")
            return
        try:
            pl = Pruefungsleistung()
            pl.note = note
        except ValueError as e:
            self.note_fehler_label.configure(text=str(e))
            return
        self.kurs.pruefungsleistung = pl
        # Bei einer (neu) eingetragenen Note gilt der Kurs als fertig bearbeitet -
        # alle Lektionen werden automatisch als abgeschlossen markiert.
        for lektion in self.kurs.lektionen:
            lektion.abgeschlossen = True
        if not pl.ist_bestanden():
            # Der jetzt "verbrauchte" Prüfungstermin wird zurückgesetzt, damit die
            # Noteneingabe nicht direkt wieder erscheint - erst wenn im Profil
            # explizit ein neuer Termin für den nächsten Versuch eingetragen wird.
            self.kurs.pruefungstermin = None
        self.app.daten_speichern()
        self.app.ansicht_wechseln("dashboard")

    def _korrigieren_button(self, parent):
        """Kleiner, unauffälliger Link neben der Note, um eine versehentlich
        falsch eingetragene Note zu korrigieren (z.B. Tippfehler wie 5,0
        statt 2,0). Nutzt Pruefungsleistung.pruefung_entfernen()."""
        ctk.CTkButton(
            parent, text="Korrigieren", width=0,
            fg_color="transparent", hover_color=DUNKEL,
            text_color=TEXT_MUTED, font=ctk.CTkFont(size=11, underline=True),
            corner_radius=6,
            command=self._note_korrigieren
        ).pack(side="right", padx=(0, 8))

    def _note_korrigieren(self):
        """Löscht eine versehentlich falsch eingetragene Note wieder, damit
        sie neu eingegeben werden kann.

        Ruft bewusst Pruefungsleistung.pruefung_entfernen() auf (statt die
        Note direkt zu überschreiben), um die vorhandene, dafür vorgesehene
        Methode zu nutzen. Da eine 'leere' Pruefungsleistung inhaltlich
        aber nichts mehr aussagt, wird sie danach zusätzlich ganz vom Kurs
        entfernt (pruefungsleistung = None) - dadurch erscheint das Kurs
        wieder genau wie vor der ersten Noteneingabe.
        """
        if self.kurs.pruefungsleistung is not None:
            self.kurs.pruefungsleistung.pruefung_entfernen()
            self.kurs.pruefungsleistung = None
        self.app.daten_speichern()
        self.app.ansicht_wechseln("dashboard")