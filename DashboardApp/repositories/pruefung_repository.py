from models.enums import PruefungsartEnum
from models.pruefung import Pruefung


class PruefungRepository:
    """Speichert und lädt Prüfungen eines Kurses aus der Datenbank."""

    def __init__(self, database):
        self.db = database

    def pruefung_speichern(self, kursname, pruefung):
        """Speichert eine Prüfung mit Kursbezug."""
        self.db.cursor.execute(
            """
            INSERT INTO pruefungen(kursname, datum, pruefungsart, note, bestanden)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                kursname,
                str(pruefung.datum),
                pruefung.pruefungsart.value,
                pruefung.note,
                int(pruefung.bestanden)
            )
        )

        self.db.connection.commit()

    def lade_pruefungen(self, kursname=None):
        """Lädt Prüfungen für einen Kurs oder alle Prüfungen."""
        if kursname is None:
            daten = self.db.cursor.execute(
                """
                SELECT datum, pruefungsart, note, bestanden
                FROM pruefungen
                """
            ).fetchall()
        else:
            daten = self.db.cursor.execute(
                """
                SELECT datum, pruefungsart, note, bestanden
                FROM pruefungen
                WHERE kursname = ?
                """,
                (kursname,)
            ).fetchall()

        pruefungen = []

        for datum, pruefungsart, note, bestanden in daten:
            pruefungen.append(
                Pruefung(
                    datum=datum,
                    pruefungsart=PruefungsartEnum(pruefungsart),
                    note=note,
                    bestanden=bool(bestanden)
                )
            )

        return pruefungen

    def loesche_pruefungen(self, kursname):
        """Löscht Prüfungen eines Kurses, wenn ein Kurs zurückgesetzt wird."""
        self.db.cursor.execute(
            """
            DELETE FROM pruefungen
            WHERE kursname = ?
            """,
            (kursname,)
        )

        self.db.connection.commit()
