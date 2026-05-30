from models.kurs import Kurs
from models.enums import KursStatusEnum


class KursRepository:
    """Speichert und lädt Kurse aus der Datenbank."""

    def __init__(self, database):
        self.db = database

    def kurs_speichern(self, kurs):
        """Speichert einen Kurs, falls er noch nicht vorhanden ist."""
        # Kursnamen sind eindeutig. Dadurch wird verhindert,
        # dass ein Kurs mehrfach aus der Studiengangsvorlage geladen wird.
        vorhandener_kurs = self.db.cursor.execute(
            "SELECT kursname FROM kurse WHERE kursname = ?",
            (kurs.kursname,)
        ).fetchone()

        if vorhandener_kurs is not None:
            return False

        self.db.cursor.execute(
            """
            INSERT INTO kurse(kursname, ects, semester, status, voraussetzungen)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                kurs.kursname,
                kurs.ects,
                kurs.semester,
                kurs.status.value,
                ",".join(kurs.voraussetzungen)
            )
        )

        self.db.connection.commit()
        return True

    def lade_kurse(self):
        """Lädt alle Kurse und wandelt Datenbankzeilen wieder in Kurs-Objekte um."""
        daten = self.db.cursor.execute(
            """
            SELECT kursname, ects, semester, status, voraussetzungen
            FROM kurse
            """
        ).fetchall()

        kurse = []

        for kursname, ects, semester, status, voraussetzungen in daten:
            voraussetzungen_liste = []

            if voraussetzungen:
                voraussetzungen_liste = voraussetzungen.split(",")

            kurse.append(
                Kurs(
                    kursname,
                    ects,
                    semester,
                    KursStatusEnum(status),
                    voraussetzungen_liste
                )
            )

        return kurse
    
    def aktualisiere_kurs_status(self, kursname, status):
        """Aktualisiert nur den Status eines bestehenden Kurses."""
        self.db.cursor.execute(
            """
            UPDATE kurse
            SET status = ?
            WHERE kursname = ?
            """,
            (
                status.value,
                kursname
            )
        )

        self.db.connection.commit()
