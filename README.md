# StudyBoard

Ein Studien-Dashboard zur Verwaltung von Kursen, Lernfortschritt und Prüfungsterminen, entwickelt mit Python und CustomTkinter im Rahmen des Moduls "Objektorientierte und funktionale Programmierung mit Python" an der IU Internationale Hochschule.

**GitHub-Repository:** https://github.com/melina-exe/studyboard-dashboard

## Was macht StudyBoard?

StudyBoard zeigt den eigenen Studienfortschritt in einer Übersicht. Jeder selbst eingetragene Kurs erscheint als Kachel mit Status: läuft er noch, steht die Prüfung noch aus, oder ist er schon bestanden. Kurse lassen sich in einzelne Lektionen aufteilen und einzeln abhaken; ein Fortschrittsbalken zeigt den Stand.

Sobald ein Prüfungstermin feststeht, rechnet die App die verbleibende Zeit aus und färbt die Karte danach ein: Rot unter 10 Tagen, Orange unter 30, Violett bei ausreichend Zeit, Grün nach bestandener Prüfung. Bestandene Kurse bleiben noch drei Tage sichtbar, verschwinden dann aus der Übersicht, zählen aber weiter bei ECTS und Notendurchschnitt mit. Im Profil lassen sie sich jederzeit wieder aufrufen.

Oben im Dashboard stehen drei Kennzahlen: erreichte ECTS im Verhältnis zum Studiengang, gewichteter Notendurchschnitt, Anzahl bestandener Kurse. Geht eine Prüfung mal schief, zeigt die Karte das direkt an und lässt sich mit einem neuen Prüfungstermin für den nächsten Versuch bearbeiten.

## Voraussetzungen

- Python 3.10 oder höher
- Betriebssystem: Windows, macOS oder Linux

## Installation

1. Repository klonen oder als ZIP herunterladen und entpacken:
   ```
   git clone https://github.com/melina-exe/studyboard-dashboard.git
   ```

2. In den Projektordner wechseln:
   ```
   cd studyboard-dashboard
   ```

3. Abhängigkeiten installieren:
   ```
   pip install -r requirements.txt
   ```
   *(Unter Windows ggf. `py -m pip install -r requirements.txt`, falls `pip` nicht direkt gefunden wird.)*

## Starten

```
python main.py
```

*(Unter Windows: `py main.py`)*

## Profildaten: leer oder mit Beispieldaten starten

Im Ordner `data/` liegen drei JSON-Dateien:

| Datei | Zweck |
|---|---|
| `profil.json` | Wird tatsächlich von der Anwendung geladen. **Standardmäßig leer.** |
| `profil_leer.json` | Vorlage für ein leeres Profil (identisch mit dem Auslieferungszustand von `profil.json`). |
| `profil_beispiel.json` | Vorlage mit Beispieldaten: 5 Demo-Kurse, die alle vier Status-Farben zeigen (bestanden, laufend, Prüfung bald/etwas später fällig, nicht bestanden mit geplantem neuen Versuch). |

**Standardmäßig startet die App leer** (`profil.json` enthält kein Profil und keine Kurse). Um stattdessen die Beispieldaten zu sehen, einmalig **vor dem Start** die gewünschte Vorlage über `profil.json` kopieren:

```
# Beispieldaten laden (Windows PowerShell):
copy data\profil_beispiel.json data\profil.json

# Beispieldaten laden (macOS/Linux):
cp data/profil_beispiel.json data/profil.json
```

Um wieder zum leeren Zustand zurückzukehren, einfach `profil_leer.json` genauso über `profil.json` kopieren. Über die Oberfläche selbst lassen sich außerdem jederzeit eigene Kurse im Profil-Bereich hinzufügen, bearbeiten und löschen - die Beispieldaten sind nur ein schneller Einstieg, kein fester Bestandteil der Anwendung.

## Projektstruktur

```
Mein Dashboard/
├── main.py              Einstiegspunkt der Anwendung
├── app.py                Hauptklasse DashboardApp
├── models/                Fachklassen (Kurs, Profil, Studiengang, ...)
├── services/             Berechnungs- und Archivierungslogik
├── repository/            Speichern/Laden der Profildaten (JSON)
├── views/                 CustomTkinter-Ansichten (Dashboard, Profil)
├── assets/                Icons und Bilder
└── data/                  Profildaten (profil.json, profil_leer.json, profil_beispiel.json)
```