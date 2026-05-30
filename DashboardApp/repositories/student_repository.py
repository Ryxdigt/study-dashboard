from models.student import Student


class StudentRepository:
    """Speichert und lädt Studentendaten aus der Datenbank."""

    def __init__(self, database):
        self.db = database

    def student_speichern(self, student):
        """Speichert genau einen Studenten für das Dashboard."""
        # Für den Prototyp wird nur ein Student verwaltet.
        # Deshalb werden alte Stammdaten vor dem Speichern entfernt.
        self.db.cursor.execute("DELETE FROM student")

        self.db.cursor.execute(
            """
            INSERT INTO student(name, matrikelnummer, studiengang)
            VALUES (?, ?, ?)
            """,
            (
                student.name,
                student.matrikelnummer,
                student.studiengang
            )
        )

        self.db.connection.commit()

    def lade_student(self):
        """Lädt den gespeicherten Studenten oder gibt None zurück."""
        daten = self.db.cursor.execute(
            "SELECT name, matrikelnummer, studiengang FROM student"
        ).fetchone()

        if daten is None:
            return None

        name, matrikelnummer, studiengang = daten

        return Student(
            name,
            matrikelnummer,
            studiengang
        )
