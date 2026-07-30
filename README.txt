# StudyBoard

Ein Studien-Dashboard zur Verwaltung von Kursen, Lernfortschritt und Prüfungsterminen, entwickelt mit Python und CustomTkinter im Rahmen des Moduls "Object-Oriented Programming with Python" an der IU Internationale Hochschule.

**GitHub-Repository:** [Link hier einfügen]

## Voraussetzungen

- Python 3.10 oder höher
- Betriebssystem: Windows, macOS oder Linux

## Installation

1. Repository klonen oder als ZIP herunterladen und entpacken:
   ```
   git clone [Link hier einfügen]
   ```

2. In den Projektordner wechseln:
   ```
   cd Mein_Dashboard
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

Die Anwendung startet automatisch mit einem leeren Profil, falls noch keine Daten unter `data/profil.json` vorhanden sind.

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
└── data/                  Gespeicherte Profildaten (profil.json)
```