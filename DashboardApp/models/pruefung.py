from models.enums import PruefungsartEnum


class Pruefung:
    """Repräsentiert eine Prüfung, die zu einem Kurs gehört.

    Die Note wird hier gespeichert. Angerechnete Kurse besitzen dagegen keine Prüfung.
    """

    def __init__(self, datum, pruefungsart, note=None, bestanden=False):
        self.datum = datum
        self.pruefungsart = pruefungsart
        self.note = note
        self.bestanden = bestanden

    def pruefung_abschliessen(self):
        """Prüft anhand der Note, ob die Prüfung bestanden wurde."""
        if self.note is None:
            return False

        self.bestanden = self.note <= 4
        return self.bestanden
