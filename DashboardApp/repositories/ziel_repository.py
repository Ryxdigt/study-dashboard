from models.enums import ZielStatusEnum


class ZielRepository:
    """Speichert und lädt Studienziele aus der Datenbank.

    Im aktuellen Prototyp werden die Ziele hauptsächlich im Dashboard angezeigt
    und durch den ZielService ausgewertet. Dieses Repository kapselt trotzdem
    die Datenhaltung, damit die Architektur aus Controller, Service und
    Repository auch für Ziele vollständig nachvollziehbar bleibt.
    """

    def __init__(self, database):
        self.db = database

    def ziel_speichern(self, beschreibung, zielart, zielwert, status=ZielStatusEnum.IN_BEARBEITUNG):
        """Speichert ein Ziel mit Zielart, Zielwert und aktuellem Status."""
        self.db.cursor.execute(
            """
            INSERT INTO ziele(beschreibung, zielart, zielwert, status)
            VALUES (?, ?, ?, ?)
            """,
            (
                beschreibung,
                zielart,
                str(zielwert),
                status.value
            )
        )

        self.db.connection.commit()

    def lade_ziele(self):
        """Lädt alle gespeicherten Ziele als einfache Wörterbücher.

        Die konkreten Zielklassen werden weiterhin im Model beschrieben. Für
        die Anzeige im Dashboard reicht hier eine neutrale Datenstruktur aus.
        """
        daten = self.db.cursor.execute(
            """
            SELECT beschreibung, zielart, zielwert, status
            FROM ziele
            """
        ).fetchall()

        ziele = []

        for beschreibung, zielart, zielwert, status in daten:
            ziele.append({
                "beschreibung": beschreibung,
                "zielart": zielart,
                "zielwert": zielwert,
                "status": ZielStatusEnum(status)
            })

        return ziele

    def alle_ziele_loeschen(self):
        """Löscht alle gespeicherten Ziele aus der Datenbank."""
        self.db.cursor.execute("DELETE FROM ziele")
        self.db.connection.commit()
