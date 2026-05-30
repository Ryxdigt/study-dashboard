import sqlite3
from pathlib import Path


class Database:
    """Stellt die Verbindung zur SQLite-Datenbank her.

    Diese Klasse kennt die technische Datenbankverbindung und legt beim Start
    die benötigten Tabellen an, falls sie noch nicht existieren.
    """

    def __init__(self):
        # Der Datenbankpfad wird relativ zum Projekt berechnet.
        # Dadurch funktioniert die App auch, wenn sie aus einem anderen Ordner gestartet wird.
        datenbank_pfad = Path(__file__).resolve().parents[1] / "data" / "studium.db"

        self.connection = sqlite3.connect(
            datenbank_pfad,
            check_same_thread=False
        )
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        """Legt alle Tabellen für Student, Kurse, Ziele, Lernzeiten und Prüfungen an."""
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS student(
            name TEXT,
            matrikelnummer TEXT,
            studiengang TEXT
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS kurse(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kursname TEXT UNIQUE,
            ects INTEGER,
            semester INTEGER,
            status TEXT,
            voraussetzungen TEXT
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS ziele(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            beschreibung TEXT,
            zielart TEXT,
            zielwert TEXT,
            status TEXT
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS lernzeiten(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kursname TEXT,
            datum TEXT,
            stunden REAL
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS pruefungen(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kursname TEXT,
            datum TEXT,
            pruefungsart TEXT,
            note REAL,
            bestanden INTEGER
        )
        """)
        self.connection.commit()

    def close(self):
        """Schließt die Datenbankverbindung."""
        self.connection.close()

    def alles_zuruecksetzen(self):
        """Löscht alle gespeicherten Prototyp-Daten aus der Datenbank."""
        tabellen = [
            "pruefungen",
            "lernzeiten",
            "ziele",
            "kurse",
            "student"
        ]

        for tabelle in tabellen:
            self.cursor.execute(f"DELETE FROM {tabelle}")

        # Setzt die automatisch vergebenen IDs wieder zurück.
        self.cursor.execute(
            """
            DELETE FROM sqlite_sequence
            WHERE name IN ('pruefungen', 'lernzeiten', 'ziele', 'kurse')
            """
        )

        self.connection.commit()
    
