# models/status.py
"""Enum für den abgeleiteten Status eines Kurses (siehe Kurs.status)."""
from enum import Enum

class Status(Enum):
    """Mögliche Zustände eines Kurses."""
    LAUFEND = "laufend"       # Kurs läuft, noch kein Prüfungstermin gesetzt
    AUSSTEHEND = "ausstehend"  # Prüfungstermin gesetzt, aber noch keine Note eingetragen
    BESTANDEN = "bestanden"    # Note eingetragen und bestanden (Note <= 4.0)