#-------------------
# Übersicht möglicher Studiengänge, kann zukünftig beliebig erweitert werden.
# Beim Protoyp werden nur die ersten 2 Semester angeführt des Studienganges Angewandte KI verwendet
#-------------------

STUDIENGAENGE = {
    "Angewandte KI": [
            # Kurse 1. Semester:
            {
                "kursname": "Artificial Intelligence",
                "ects": 5,
                "semester": 1,
                "voraussetzung": []
            },
            {
                "kursname": "Einführung in das wissenschaftliche Arbeiten für IT und Technik",
                "ects": 5,
                "semester": 1,
                "voraussetzung": []
            },
            {
                "kursname": "Einführung in die Programmierung mit Python",
                "ects": 5,
                "semester": 1,
                "voraussetzung": []
            },
            {
                "kursname": "Mathematik: Analysis",
                "ects": 5,
                "semester": 1,
                "voraussetzung": []
            },
            {
                "kursname": "Kollaboratives Arbeiten",
                "ects": 5,
                "semester": 1,
                "voraussetzung": []
            },
            {
                "kursname": "Statistik - Wahrscheinlichkeit und deskriptive Statistik",
                "ects": 5,
                "semester": 1,
                "voraussetzung": []
            },
            # Kurse 2. Semester:
            {
                "kursname": "Projekt: Objektorientierte und funktionale Programmierung mit Python",
                "ects": 5,
                "semester": 2,
                "voraussetzung": []
            },
            {
                "kursname": "Mathematik: Lineare Algebra",
                "ects": 5,
                "semester": 2,
                "voraussetzung": []
            },
            {
                "kursname": "Interkulturelle und ethische Handlungskompetenzen",
                "ects": 5,
                "semester": 2,
                "voraussetzung": []
            },
            {
                "kursname": "Statistik - Induktive Statistik",
                "ects": 5,
                "semester": 2,
                "voraussetzung": ["Statistik - Wahrscheinlichkeit und deskriptive Statistik"]
            },
            {
                "kursname": "Statistik - Wahrscheinlichkeit und deskriptive Statistik",
                "ects": 5,
                "semester": 2,
                "voraussetzung": []
            },
            {
                "kursname": "Projekt: Cloud Programming",
                "ects": 5,
                "semester": 2,
                "voraussetzung": []
            },
            {
                "kursname": "Cloud Computing",
                "ects": 5,
                "semester": 2,
                "voraussetzung": []
            },
    ]
}