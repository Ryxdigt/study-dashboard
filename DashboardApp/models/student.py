class Student:
    """Repräsentiert den Studierenden und bündelt Studiendaten."""

    def __init__(self, name, matrikelnummer, studiengang):
        self.name = name
        self.matrikelnummer = matrikelnummer
        self.studiengang = studiengang
        self.kurse = []
        self.ziele = []

    def kurs_hinzufuegen(self, kurs):
        """Fügt dem Studenten einen Kurs hinzu."""
        self.kurse.append(kurs)

    def ziel_hinzufuegen(self, ziel):
        """Fügt dem Studenten ein persönliches Ziel hinzu."""
        self.ziele.append(ziel)

    def berechne_fortschritt(self):
        """Berechnet den Anteil abgeschlossener Kurse."""
        if len(self.kurse) == 0:
            return 0

        abgeschlossen = len([
            kurs for kurs in self.kurse
            if kurs.status.value == "Abgeschlossen"
        ])

        return (abgeschlossen/len(self.kurse)) * 100
