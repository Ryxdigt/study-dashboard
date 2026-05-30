class Lernzeit:
    """Speichert Soll- und Ist-Lernzeit zu einem Kurs."""

    def __init__(self, datum, soll_stunden, ist_stunden):
        self.datum = datum
        self.soll_stunden = soll_stunden
        self.ist_stunden = ist_stunden

    def berechne_abweichung(self):
        """Berechnet die Abweichung zwischen Ist- und Soll-Stunden."""
        return self.ist_stunden - self.soll_stunden
