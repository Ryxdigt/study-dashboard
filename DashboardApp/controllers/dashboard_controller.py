from data.studiengaenge import STUDIENGAENGE

from models.student import Student
from models.kurs import Kurs
from models.pruefung import Pruefung
from models.enums import KursStatusEnum, PruefungsartEnum

from repositories.database import Database
from repositories.student_repository import StudentRepository
from repositories.kurs_repository import KursRepository
from repositories.lernzeit_repository import LernzeitRepository
from repositories.pruefung_repository import PruefungRepository
from repositories.ziel_repository import ZielRepository

from services.kurs_service import KursService
from services.lernzeit_service import LernzeitService
from services.ziel_service import ZielService


class DashboardController:
    """Koordiniert Benutzeraktionen zwischen Oberfläche, Fachlogik und Datenbank.

    Die Streamlit-Oberfläche ruft diese Klasse auf. Der Controller entscheidet
    dann, welcher Service oder welches Repository für die jeweilige Aktion
    zuständig ist. Dadurch bleibt die Oberfläche möglichst frei von Fachlogik.
    """

    def __init__(self):
        # Die Datenbank wird nur einmal erzeugt und an die Repositories weitergegeben.
        self.database = Database()

        # Repositories kapseln alle direkten Datenbankzugriffe.
        self.student_repository = StudentRepository(self.database)
        self.kurs_repository = KursRepository(self.database)
        self.lernzeit_repository = LernzeitRepository(self.database)
        self.pruefung_repository = PruefungRepository(self.database)
        self.ziel_repository = ZielRepository(self.database)

        # Services enthalten die fachlichen Berechnungen und Regeln.
        self.kurs_service = KursService(self.kurs_repository)
        self.lernzeit_service = LernzeitService()
        self.ziel_service = ZielService()

    def lade_student(self):
        """Lädt den gespeicherten Studenten aus der Datenbank."""
        return self.student_repository.lade_student()

    def student_anlegen(self, name, matrikelnummer, studiengang):
        """Speichert den Studenten und initialisiert die Kurse des Studiengangs."""
        student = Student(name, matrikelnummer, studiengang)

        self.student_repository.student_speichern(student)
        self.initialisiere_kurse_fuer_studiengang(studiengang)

    def lade_kurse(self):
        """Lädt alle Kurse und ergänzt fehlende Voraussetzungen aus der Vorlage."""
        kurse = self.kurs_repository.lade_kurse()

        # Ältere Datenbankeinträge können noch ohne Voraussetzungen gespeichert sein.
        # Deshalb werden sie beim Laden aus der Studiengangsvorlage ergänzt.
        for kurs in kurse:
            if len(kurs.voraussetzungen) == 0:
                kurs.voraussetzungen = self.voraussetzungen_aus_vorlage(kurs.kursname)

        return kurse

    def voraussetzungen_aus_vorlage(self, kursname):
        """Sucht die Voraussetzungen eines Kurses in der Studiengangsvorlage."""
        for kurse_vorlage in STUDIENGAENGE.values():
            for kurs_daten in kurse_vorlage:
                if kurs_daten["kursname"] == kursname:
                    return kurs_daten.get(
                        "voraussetzungen",
                        kurs_daten.get("voraussetzung", [])
                    )

        return []

    def offene_kurse_laden(self):
        """Lädt alle offenen Kurse."""
        kurse = self.lade_kurse()
        return self.kurs_service.lade_offene_kurse(kurse)
    
    def initialisiere_kurse_fuer_studiengang(self, studiengang):
        kurse_vorlage = STUDIENGAENGE.get(studiengang, [])

        for kurs_daten in kurse_vorlage:
            kurs = Kurs(
                kursname=kurs_daten["kursname"],
                ects=kurs_daten["ects"],
                semester=kurs_daten["semester"],
                status=KursStatusEnum.OFFEN,
                voraussetzungen=kurs_daten.get(
                    "voraussetzungen",
                    kurs_daten.get("voraussetzung", [])
                )
            )

            self.kurs_repository.kurs_speichern(kurs)

    def kurs_aktivieren(self, kurs):
        self.kurs_service.aktiviere_kurs(kurs)

    def fehlende_voraussetzungen(self, kurs):
        """Gibt zurück, welche Voraussetzungen für einen Kurs noch fehlen."""
        return self.kurs_service.pruefe_voraussetzungen(kurs, self.lade_kurse())

    def kurs_anrechnen(self, kurs):
        """Markiert einen offenen Kurs als angerechnet."""
        self.kurs_service.rechne_kurs_an(kurs)

    def kurs_zuruecksetzen(self, kurs):
        """Setzt einen Kurs zurück und entfernt versehentlich gespeicherte Prüfungen."""
        self.kurs_service.setze_kurs_zurueck(kurs)
        self.pruefung_repository.loesche_pruefungen(kurs.kursname)

    def lernzeit_hinzufuegen(self, kursname, datum, stunden):
        self.lernzeit_repository.lernzeit_speichern(kursname, datum, stunden)

    def gesamt_lernzeit(self, kursname):
        lernzeiten = self.lernzeit_repository.lade_lernzeiten(kursname)

        return self.lernzeit_service.berechne_wochenstunden(lernzeiten)

    def lade_woechentliche_lernzeit(self):
        """Lädt Lernzeiten als Wochenwerte für das Liniendiagramm."""
        lernzeiten = self.lernzeit_repository.lade_alle_lernzeiten()
        return self.lernzeit_service.berechne_woechentliche_lernzeit(lernzeiten)

    def berechne_aktuellen_wochendurchschnitt(self):
        """Berechnet den Durchschnitt der bisher erfassten Wochenlernzeiten."""
        lernzeiten = self.lernzeit_repository.lade_alle_lernzeiten()
        return self.lernzeit_service.berechne_aktuellen_wochendurchschnitt(lernzeiten)

    def pruefung_hinzufuegen(self, kurs, datum, pruefungsart, note):
        """Speichert eine Prüfung und schließt den Kurs bei bestandener Note ab."""
        pruefung = Pruefung(
            datum=datum,
            pruefungsart=PruefungsartEnum(pruefungsart),
            note=note
        )

        pruefung.pruefung_abschliessen()
        self.pruefung_repository.pruefung_speichern(kurs.kursname, pruefung)

        if pruefung.bestanden:
            self.kurs_service.schliesse_kurs_ab(kurs)

        return pruefung

    def lade_pruefungen(self, kursname=None):
        return self.pruefung_repository.lade_pruefungen(kursname)

    def berechne_erreichte_ects(self):
        return self.kurs_service.berechne_erreichte_ects(self.lade_kurse())

    def berechne_studienfortschritt(self):
        return self.kurs_service.berechne_studienfortschritt(self.lade_kurse())

    def berechne_notendurchschnitt(self):
        """Berechnet den Notendurchschnitt ohne angerechnete Kurse."""
        pruefungen = []

        # Angerechnete Kurse haben keine Note und dürfen deshalb nicht einfließen.
        for kurs in self.lade_kurse():
            if kurs.status != KursStatusEnum.ANGERECHNET:
                pruefungen.extend(self.lade_pruefungen(kurs.kursname))

        return self.ziel_service.berechne_notendurchschnitt(pruefungen)

    def ziel_speichern(self, beschreibung, zielart, zielwert):
        """Speichert ein Ziel über das ZielRepository."""
        self.ziel_repository.ziel_speichern(
            beschreibung,
            zielart,
            zielwert
        )

    def lade_ziele(self):
        """Lädt gespeicherte Ziele aus der Datenbank."""
        return self.ziel_repository.lade_ziele()

    def analysiere_dashboard_risiken(self):
        """Erstellt Warnungen für Lernzeit, aktive Kurse und Notenziel."""
        kurse = self.lade_kurse()
        aktive_kurse = [
            kurs for kurs in kurse
            if kurs.status == KursStatusEnum.IN_BEARBEITUNG
        ]
        lernzeiten_pro_kurs = {}

        for kurs in aktive_kurse:
            lernzeiten_pro_kurs[kurs.kursname] = self.gesamt_lernzeit(kurs.kursname)

        return self.ziel_service.analysiere_dashboard_risiken(
            aktive_kurse,
            lernzeiten_pro_kurs,
            self.berechne_notendurchschnitt()
        )

    def alles_zuruecksetzen(self):
        """Löscht alle Daten, damit der Prototyp neu getestet werden kann."""
        self.database.alles_zuruecksetzen()
