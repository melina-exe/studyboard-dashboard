# models/status.py
from enum import Enum

class Status(Enum):
    """Mögliche Zustände eines Kurses."""
    LAUFEND = "laufend"
    AUSSTEHEND = "ausstehend"
    BESTANDEN = "bestanden"