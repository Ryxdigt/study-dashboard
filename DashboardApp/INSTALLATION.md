# Installationsanleitung

## GitHub-Repository

GitHub-Link: https://github.com/Ryxdigt/Study_Dashboard_IU

## Voraussetzungen

- Windows 10 oder Windows 11
- Python 3.11 oder neuer
- Internetverbindung zur Installation der Python-Bibliotheken

## Installation

1. Projektordner herunterladen oder aus GitHub klonen.
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

## Hinweis zur Datenspeicherung

Die Daten werden lokal in der SQLite-Datenbank `data/studium.db` gespeichert. Wenn die Datenbank noch nicht vorhanden ist wird sie erstellt. Dadurch bleiben Studentendaten, Kurse, Lernzeiten und Prüfungen zwischen Programmstarts erhalten.
