class ZielService:
    """Prüft Zielerreichung und erstellt Kennzahlen für die Übersicht."""

    def pruefe_ziel(self, ziel):
        """Prüft ein einzelnes Ziel über dessen eigene Zielmethode."""
        return ziel.pruefe_zielerreichung()

    def pruefe_alle_ziele(self, ziele):
        """Prüft mehrere Ziele und gibt die Ergebnisse als Liste zurück."""
        ergebnisse = []
        for ziel in ziele:
            ergebnisse.append(ziel.pruefe_zielerreichung())
        return ergebnisse

    def berechne_notendurchschnitt(self, pruefungen):
        """Berechnet den Durchschnitt aller vorhandenen Prüfungsnoten."""
        noten = [
            pruefung.note
            for pruefung in pruefungen
            if pruefung.note is not None
        ]

        if len(noten) == 0:
            return 0

        return sum(noten) / len(noten)

    def analysiere_dashboard_risiken(
        self,
        aktive_kurse,
        lernzeiten_pro_kurs,
        notendurchschnitt,
        ziel_note=2.0,
        soll_lernzeit=5
    ):
        """Bewertet Risiken für Zielerreichung, Lernzeit und aktive Kurse."""
        risiken = []

        # Ohne aktive Kurse gibt es nichts zu lernen oder zu prüfen.
        if len(aktive_kurse) == 0:
            risiken.append({
                "stufe": "Info",
                "bereich": "Kurse",
                "meldung": "Aktuell ist kein Kurs in Bearbeitung."
            })

        for kurs in aktive_kurse:
            lernzeit = lernzeiten_pro_kurs.get(kurs.kursname, 0)

            # Liegt die Lernzeit unter dem Sollwert, wird der Kurs als Risiko gemeldet.
            if lernzeit < soll_lernzeit:
                risiken.append({
                    "stufe": "Hoch",
                    "bereich": kurs.kursname,
                    "meldung": (
                        f"Die Lernzeit liegt mit {lernzeit} h unter dem "
                        f"Sollwert von {soll_lernzeit} h."
                    )
                })
            else:
                risiken.append({
                    "stufe": "Niedrig",
                    "bereich": kurs.kursname,
                    "meldung": "Die erfasste Lernzeit liegt im Zielbereich."
                })

        # Das Notenziel kann erst sinnvoll bewertet werden, wenn Noten vorhanden sind.
        if notendurchschnitt == 0:
            risiken.append({
                "stufe": "Info",
                "bereich": "Notenziel",
                "meldung": "Das Notenziel kann erst nach der ersten Note bewertet werden."
            })
        elif notendurchschnitt > ziel_note:
            risiken.append({
                "stufe": "Hoch",
                "bereich": "Notenziel",
                "meldung": (
                    f"Der aktuelle Durchschnitt {notendurchschnitt:.2f} "
                    f"liegt über dem Zielwert {ziel_note:.1f}."
                )
            })
        else:
            risiken.append({
                "stufe": "Niedrig",
                "bereich": "Notenziel",
                "meldung": "Das Notenziel wird aktuell erreicht."
            })

        return risiken
