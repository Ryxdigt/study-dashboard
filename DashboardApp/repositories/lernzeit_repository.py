class LernzeitRepository:
    """Speichert und lädt Lernzeiten aus der Datenbank."""

    def __init__(self, database):
        self.db = database

    def lernzeit_speichern(self, kursname, datum, stunden):
        """Speichert eine Lernzeit zu einem bestimmten Kurs."""
        self.db.cursor.execute(
            """
            INSERT INTO lernzeiten(
                kursname,
                datum,
                stunden
            )
            VALUES (?, ?, ?)
            """,
            (
                kursname,
                str(datum),
                stunden
            )
        )

        self.db.connection.commit()

    def lade_lernzeiten(
        self,
        kursname
    ):
        """Lädt die Stundenwerte eines einzelnen Kurses."""

        daten = self.db.cursor.execute(
            """
            SELECT stunden
            FROM lernzeiten
            WHERE kursname = ?
            """,
            (kursname,)
        ).fetchall()

        return [eintrag[0] for eintrag in daten]

    def lade_alle_lernzeiten(self):
        """Lädt alle Lernzeiten für die wöchentliche Lernzeitübersicht."""
        daten = self.db.cursor.execute(
            """
            SELECT datum, stunden
            FROM lernzeiten
            ORDER BY datum
            """
        ).fetchall()

        return [
            {
                "datum": eintrag[0],
                "stunden": eintrag[1]
            }
            for eintrag in daten
        ]
