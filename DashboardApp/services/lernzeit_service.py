from datetime import date


class LernzeitService:
    """Verarbeitet Lernzeiten und bereitet sie für Kennzahlen und Diagramme auf."""

    def berechne_wochenstunden(self, lernzeiten):
        """Addiert alle übergebenen Lernzeiten."""
        gesamt = 0

        for lernzeit in lernzeiten:
            if hasattr(lernzeit, "ist_stunden"):
                gesamt += lernzeit.ist_stunden
            else:
                gesamt += lernzeit

        return gesamt

    def berechne_durchschnitt(self, lernzeiten):
        """Berechnet den Durchschnitt aus einer Liste von Lernzeiten."""
        if len(lernzeiten) == 0:
            return 0

        return self.berechne_wochenstunden(lernzeiten) / len(lernzeiten)

    def berechne_woechentliche_lernzeit(self, lernzeiten):
        """Gruppiert einzelne Lernzeiteinträge nach Kalenderwochen."""
        wochen = {}

        for lernzeit in lernzeiten:
            datum = date.fromisoformat(lernzeit["datum"])
            kalender = datum.isocalendar()
            schluessel = (kalender.year, kalender.week)

            if schluessel not in wochen:
                wochen[schluessel] = 0

            wochen[schluessel] += lernzeit["stunden"]

        return [
            {
                "Woche": f"{jahr}-KW{woche:02d}",
                "Stunden": stunden
            }
            for (jahr, woche), stunden in sorted(wochen.items())
        ]

    def berechne_aktuellen_wochendurchschnitt(self, lernzeiten):
        """Berechnet den Durchschnitt über alle vorhandenen Kalenderwochen."""
        wochenwerte = self.berechne_woechentliche_lernzeit(lernzeiten)

        if len(wochenwerte) == 0:
            return 0

        return sum(
            eintrag["Stunden"]
            for eintrag in wochenwerte
        ) / len(wochenwerte)
