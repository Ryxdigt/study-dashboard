# Study Dashboard

Dieses Projekt ist ein prototypisches Dashboard zur Erfassung und Auswertung des eigenen Studienfortschritts. Es wurde im Rahmen des Moduls Objektorientierte und funktionale Programmierung mit Python entwickelt.

## Funktionen

- Übersicht über Studienziele, erreichte ECTS und Lernzeit
- Darstellung des ECTS-Fortschritts in einem Tortendiagramm
- Auswertung der wöchentlichen Lernzeit in einem Liniendiagramm
- Risikoanalyse für Lernzeit, Kursstatus und Zielerreichung
- Verwaltung offener, aktiver, abgeschlossener und angerechneter Kurse
- Prüfung von Kursvoraussetzungen vor dem Start eines Kurses
- Speicherung der Daten in einer lokalen SQLite-Datenbank

## Voraussetzungen

- Windows 10 oder Windows 11
- Python 3.11 oder neuer
- Internetverbindung zur Installation der Python-Bibliotheken

## Installation

1. Repository herunterladen oder klonen.
2. Terminal im Ordner `DashboardApp` öffnen.
3. Virtuelle Umgebung erstellen:

   ```powershell
   python -m venv .venv
   ```

4. Virtuelle Umgebung aktivieren:

   ```powershell
   .\.venv\Scripts\activate
   ```

5. Abhängigkeiten installieren:

   ```powershell
   pip install -r requirements.txt
   ```

6. Dashboard starten:

   ```powershell
   streamlit run app.py
   ```

Nach dem Start öffnet Streamlit das Dashboard im Browser. Beim ersten Start werden Name, Matrikelnummer und Studiengang erfasst. Danach werden die Kurse automatisch aus der Studiengangsvorlage geladen.

## Datenspeicherung

Die Daten werden lokal in der SQLite-Datenbank `data/studium.db` gespeichert. Wenn die Datenbank noch nicht vorhanden ist, wird sie beim Start der Anwendung erstellt. Dadurch bleiben Studentendaten, Kurse, Lernzeiten und Prüfungen zwischen Programmstarts erhalten.

## Projektstruktur

- `app.py`: Streamlit-Oberfläche des Dashboards
- `controllers`: Koordination zwischen Oberfläche, Fachlogik und Datenhaltung
- `services`: Fachliche Berechnungen und Regeln
- `repositories`: Zugriff auf die SQLite-Datenbank
- `models`: Fachliche Klassen und Enums
- `data`: Studiengangsvorlage und lokale Datenbank
