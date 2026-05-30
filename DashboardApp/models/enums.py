from enum import Enum


class KursStatusEnum(Enum):
    """Definiert die erlaubten Statuswerte eines Kurses.

    Enums verhindern, dass im Code beliebige freie Textwerte verwendet werden.
    """

    OFFEN = "Offen"
    IN_BEARBEITUNG = "In Bearbeitung"
    KRITISCH = "Kritisch"
    ABGESCHLOSSEN = "Abgeschlossen"
    ANGERECHNET = "Angerechnet"


class PruefungsartEnum(Enum):
    """Definiert die möglichen Prüfungsarten."""

    ONLINE_KLAUSUR = "Online Klausur"
    PRAESENZKLAUSUR = "Präsenzklausur"
    MUENDLICH = "Mündlich"
    SCHRIFTLICH = "Schriftlich"
    PORTFOLIO = "Portfolio"


class ZielStatusEnum(Enum):
    """Definiert die möglichen Statuswerte eines Zieles."""

    OFFEN = "Offen"
    IN_BEARBEITUNG = "In Bearbeitung"
    ERREICHT = "Erreicht"
    VERFEHLT = "Verfehlt"
    
