from models.enums import KursStatusEnum

class Kurs:
    """Repräsentiert einen Kurs innerhalb des Studien-Dashboards.

    Ein Kurs besitzt ECTS, einen Status und optional Voraussetzungen.
    """

    def __init__(self, kursname, ects, semester, status=KursStatusEnum.OFFEN, voraussetzungen=None):
        self.kursname = kursname
        self.ects = ects
        self.semester = semester
        self.status = status
        self.voraussetzungen = voraussetzungen or []

    def aktualisiere_status(self, neuer_status):
        """Aktualisiert den Status des Kurses."""
        self.status = neuer_status
