from abc import ABC, abstractmethod

from models.enums import ZielStatusEnum


class Ziel(ABC):
    """Abstrakte Basisklasse für alle Zielarten.

    Jede konkrete Zielart muss selbst festlegen, wann sie erreicht ist.
    """

    def __init__(self, beschreibung, status=ZielStatusEnum.IN_BEARBEITUNG):
        self.beschreibung = beschreibung
        self.status = status

    @abstractmethod
    def pruefe_zielerreichung(self):
        """Muss von jeder konkreten Zielklasse umgesetzt werden."""
        pass


class Abschlussziel(Ziel):
    """Ziel zur Überprüfung eines geplanten Abschlussdatums."""

    def __init__(self, beschreibung, ziel_datum, status=ZielStatusEnum.IN_BEARBEITUNG):
        super().__init__(beschreibung, status)
        self.ziel_datum = ziel_datum

    def pruefe_zielerreichung(self):
        """Prüft, ob das Abschlussziel als erreicht markiert wurde."""
        return self.status == ZielStatusEnum.ERREICHT


class Notenziel(Ziel):
    """Ziel zur Überprüfung eines gewünschten Notendurchschnitts."""

    def __init__(self, beschreibung, ziel_note, aktuelle_note, status=ZielStatusEnum.IN_BEARBEITUNG):
        super().__init__(beschreibung, status)
        self.ziel_note = ziel_note
        self.aktuelle_note = aktuelle_note

    def pruefe_zielerreichung(self):
        """Prüft, ob der aktuelle Durchschnitt höchstens der Zielnote entspricht."""
        return self.aktuelle_note <= self.ziel_note


class LernzeitZiel(Ziel):
    """Ziel zur Überprüfung der durchschnittlichen Lernzeit."""

    def __init__(self, beschreibung, ziel_stunden, lernzeiten, status=ZielStatusEnum.IN_BEARBEITUNG):
        super().__init__(beschreibung, status)
        self.ziel_stunden = ziel_stunden
        self.lernzeiten = lernzeiten

    def berechne_durchschnitt(self):
        """Berechnet den Durchschnitt aller gespeicherten Lernzeiten."""
        if len(self.lernzeiten) == 0:
            return 0

        gesamt = 0

        for lernzeit in self.lernzeiten:
            gesamt += lernzeit.ist_stunden

        return gesamt / len(self.lernzeiten)

    def pruefe_zielerreichung(self):
        """Prüft, ob die durchschnittliche Lernzeit den Zielwert erreicht."""
        return self.berechne_durchschnitt() >= self.ziel_stunden
