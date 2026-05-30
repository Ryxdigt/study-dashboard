from models.enums import KursStatusEnum


class KursService:
    """Enthält Fachlogik rund um Kurse.

    Diese Klasse entscheidet zum Beispiel, ob ein Kurs gestartet werden darf,
    ob ECTS erreicht wurden und wie der Studienfortschritt berechnet wird.
    """

    def __init__(self, kurs_repository):
        self.repository = kurs_repository

    def lade_offene_kurse(self, kurse):
        """Filtert alle Kurse, die noch offen sind."""
        return [
            kurs for kurs in kurse
            if kurs.status == KursStatusEnum.OFFEN
        ]

    def lade_kurse(self):
        """Lädt Kurse über das Repository."""
        return self.repository.lade_kurse()

    def kurs_speichern(self, kurs):
        """Speichert einen Kurs über das Repository."""
        return self.repository.kurs_speichern(kurs)

    def aktiviere_kurs(self, kurs):
        """Setzt einen Kurs auf 'In Bearbeitung'."""
        kurs.aktualisiere_status(KursStatusEnum.IN_BEARBEITUNG)

        self.repository.aktualisiere_kurs_status(kurs.kursname, KursStatusEnum.IN_BEARBEITUNG)

    def pruefe_voraussetzungen(self, kurs, kurse):
        """Prüft, ob alle Voraussetzungen eines Kurses erfüllt sind."""
        bestandene_kursnamen = [
            vorhandener_kurs.kursname
            for vorhandener_kurs in kurse
            if vorhandener_kurs.status in [
                KursStatusEnum.ABGESCHLOSSEN,
                KursStatusEnum.ANGERECHNET
            ]
        ]

        return [
            voraussetzung
            for voraussetzung in kurs.voraussetzungen
            if voraussetzung not in bestandene_kursnamen
        ]

    def schliesse_kurs_ab(self, kurs):
        """Setzt einen bestandenen Kurs auf 'Abgeschlossen'."""
        kurs.aktualisiere_status(KursStatusEnum.ABGESCHLOSSEN)
        self.repository.aktualisiere_kurs_status(kurs.kursname, KursStatusEnum.ABGESCHLOSSEN)

    def rechne_kurs_an(self, kurs):
        """Markiert einen Kurs als angerechnet, ohne eine Note zu speichern."""
        kurs.aktualisiere_status(KursStatusEnum.ANGERECHNET)
        self.repository.aktualisiere_kurs_status(kurs.kursname, KursStatusEnum.ANGERECHNET)

    def setze_kurs_zurueck(self, kurs):
        """Setzt einen Kurs zurück auf 'Offen'."""
        kurs.aktualisiere_status(KursStatusEnum.OFFEN)
        self.repository.aktualisiere_kurs_status(kurs.kursname, KursStatusEnum.OFFEN)

    def berechne_erreichte_ects(self, kurse):
        """Summiert ECTS aus abgeschlossenen und angerechneten Kursen."""
        return sum(
            kurs.ects
            for kurs in kurse
            if kurs.status in [
                KursStatusEnum.ABGESCHLOSSEN,
                KursStatusEnum.ANGERECHNET
            ]
        )

    def berechne_studienfortschritt(self, kurse):
        """Berechnet den prozentualen Fortschritt bezogen auf alle Kurse."""
        if len(kurse) == 0:
            return 0

        abgeschlossene_kurse = [
            kurs for kurs in kurse
            if kurs.status in [
                KursStatusEnum.ABGESCHLOSSEN,
                KursStatusEnum.ANGERECHNET
            ]
        ]

        return (len(abgeschlossene_kurse) / len(kurse)) * 100
