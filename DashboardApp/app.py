import altair as alt
import pandas as pd
import streamlit as st

from controllers.dashboard_controller import DashboardController
from data.studiengaenge import STUDIENGAENGE
from models.enums import PruefungsartEnum


st.set_page_config(
    page_title="Studium Dashboard",
    page_icon="🎓",
    layout="wide"
)

controller = DashboardController()

# Dialogfenster für die Eintragung der Lernzeit.
@st.dialog("Lernzeit erfassen")
def lernzeit_dialog(kursname):
    st.write(f"Kurs: {kursname}")

    datum = st.date_input("Datum")
    stunden = st.number_input("Stunden", min_value=0.5, step=0.5)

    if st.button("Lernzeit speichern"):
        controller.lernzeit_hinzufuegen(kursname, datum, stunden)
        st.success("Lernzeit gespeichert.")
        st.rerun()


@st.dialog("Prüfung erfassen")
def pruefung_dialog(kurs):
    """Öffnet ein Dialogfenster zum Speichern einer Prüfung."""
    st.write(f"Kurs: {kurs.kursname}")

    datum = st.date_input("Prüfungsdatum")
    pruefungsart = st.selectbox(
        "Prüfungsart",
        [art.value for art in PruefungsartEnum]
    )
    note = st.number_input(
        "Note",
        min_value=1.0,
        max_value=5.0,
        step=0.1,
        value=2.0
    )

    if st.button("Prüfung speichern"):
        pruefung = controller.pruefung_hinzufuegen(
            kurs,
            datum,
            pruefungsart,
            note
        )

        if pruefung.bestanden:
            st.success("Prüfung bestanden. Der Kurs wurde abgeschlossen.")
        else:
            st.warning("Prüfung gespeichert, aber noch nicht bestanden.")

        st.rerun()

student = controller.lade_student()

st.title("🎓 Studium Dashboard")


# -------------------------------------------------
# Erststart: Student anlegen
# -------------------------------------------------

if student is None:

    st.subheader("Ersteinrichtung")

    st.info(
        "Bitte gib deine Stammdaten ein. Danach werden die Kurse "
        "deines Studiengangs automatisch geladen."
    )

    with st.form("student_formular"):

        name = st.text_input("Name")

        matrikelnummer = st.text_input("Matrikelnummer")

        studiengang = st.selectbox(
            "Studiengang",
            list(STUDIENGAENGE.keys())
        )

        speichern = st.form_submit_button("Dashboard einrichten")

        if speichern:

            if name == "" or matrikelnummer == "":

                st.warning(
                    "Bitte Name und Matrikelnummer eingeben."
                )

            else:

                controller.student_anlegen(
                    name,
                    matrikelnummer,
                    studiengang
                )

                st.success(
                    "Dashboard wurde eingerichtet. Bitte Seite neu laden."
                )

                st.rerun()


# -------------------------------------------------
# Dashboard anzeigen
# -------------------------------------------------

else:
    st.success(
    f"Angemeldet als: {student.name} | "
    f"Matrikelnummer: {student.matrikelnummer} | "
    f"Studiengang: {student.studiengang}"
)
    st.sidebar.title("Navigation")

    st.sidebar.write("Student")
    st.sidebar.write(student.name)
    st.sidebar.write(student.matrikelnummer)
    st.sidebar.write(student.studiengang)

    st.sidebar.divider()
    st.sidebar.subheader("Prototyp")
    st.sidebar.caption("Setzt alle gespeicherten Testdaten zurück.")

    if st.sidebar.button("Alles zurücksetzen"):
        controller.alles_zuruecksetzen()
        st.success("Alle Daten wurden zurückgesetzt.")
        st.rerun()

    kurse = controller.lade_kurse()
    offene_kurse = controller.offene_kurse_laden()

    # Aktive Kurse werden in der Übersicht angezeigt und können dort bearbeitet werden.
    aktive_kurse = [
        kurs for kurs in kurse
        if kurs.status.value == "In Bearbeitung"
    ]

    # Das Lernzeitziel aus Phase 1 beträgt 10 Stunden pro Woche.
    lernzeit_ziel = 10
    aktueller_wochendurchschnitt = controller.berechne_aktuellen_wochendurchschnitt()

    # Kennzahlen im oberen Bereich des Dashboards.
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Alle Kurse",
            len(kurse)
        )

    with col2:
        st.metric(
            "Offene Kurse",
            len(offene_kurse)
        )

    with col3:
        st.metric(
            "Erreichte ECTS",
            f"{controller.berechne_erreichte_ects()}"
        )

    with col4:
        if aktueller_wochendurchschnitt < lernzeit_ziel:
            st.error(f"Ø Lernzeit/Woche: {aktueller_wochendurchschnitt:.1f} h")
        else:
            st.success(f"Ø Lernzeit/Woche: {aktueller_wochendurchschnitt:.1f} h")

    tab1, tab2, tab3 = st.tabs([
        "Übersicht",
        "Offene Kurse",
        "Abgeschlossene Kurse"
    ])

    with tab1:

        st.subheader("Übersicht")

        st.write(
            "Die wichtigsten Ziele und Risiken werden hier gebündelt dargestellt."
        )

        st.subheader("Ziele und Zielverfolgung")

        fortschritt = controller.berechne_studienfortschritt()
        notendurchschnitt = controller.berechne_notendurchschnitt()
        erreichte_ects = controller.berechne_erreichte_ects()
        offene_ects = max(0, 180 - erreichte_ects)

        # Zielkennzahlen aus dem Konzeptdokument der Phase 1.
        ziel_col1, ziel_col2, ziel_col3 = st.columns(3)

        with ziel_col1:
            st.metric("Studienabschluss", "September 2028")

        with ziel_col2:
            st.metric(
                "ECTS-Ziel",
                f"{erreichte_ects} / 180"
            )

        with ziel_col3:
            st.metric("Jahresziel", "60 ECTS")

        st.caption(
            "Ziele aus Phase 1: Studienabschluss bis September 2028, "
            "60 ECTS pro Kalenderjahr von 2026 bis 2028, 10 Stunden "
            "wöchentliche Lernzeit im Monatsdurchschnitt und frühzeitige "
            "Erkennung kritischer Kurse."
        )

        st.progress(min(100, int(fortschritt)))

        st.metric(
            "Aktueller Notendurchschnitt",
            f"{notendurchschnitt:.2f}" if notendurchschnitt > 0 else "Noch keine Note"
        )

        if notendurchschnitt > 0 and notendurchschnitt <= 2.0:
            st.success("Das Notenziel 2,0 wird aktuell erreicht.")
        elif notendurchschnitt > 0:
            st.warning("Das Notenziel 2,0 wird aktuell noch nicht erreicht.")
        else:
            st.info("Noch keine Prüfungsnoten für die Zielverfolgung vorhanden.")

        st.subheader("Risikoanalyse")

        # Die Risikobewertung kommt aus dem ZielService.
        # Die Oberfläche entscheidet nur, wie die Meldungen dargestellt werden.
        for risiko in controller.analysiere_dashboard_risiken():
            meldung = f"**{risiko['bereich']}**: {risiko['meldung']}"

            if risiko["stufe"] == "Hoch":
                st.error(meldung)
            elif risiko["stufe"] == "Niedrig":
                st.success(meldung)
            else:
                st.info(meldung)

        st.caption(
            "Die Risikoanalyse bewertet, ob aktive Kurse ausreichend Lernzeit "
            "haben und ob das Notenziel gefährdet ist."
        )

        st.subheader("Grafische Übersicht")

        # Tortendiagramm: erreichte ECTS im Verhältnis zum Gesamtziel 180 ECTS.
        ects_daten = pd.DataFrame([
            {"Bereich": "Erreichte ECTS", "ECTS": erreichte_ects},
            {"Bereich": "Offene ECTS bis 180", "ECTS": offene_ects}
        ])

        ects_torte = alt.Chart(ects_daten).mark_arc(innerRadius=45).encode(
            theta=alt.Theta(field="ECTS", type="quantitative"),
            color=alt.Color(field="Bereich", type="nominal"),
            tooltip=["Bereich", "ECTS"]
        )

        # Balkendiagramm: Jahresziel von 60 ECTS für 2026 bis 2028.
        jahresziel_daten = pd.DataFrame([
            {"Jahr": "2026", "ECTS": erreichte_ects, "Art": "Aktuell erreicht"},
            {"Jahr": "2026", "ECTS": max(0, 60 - erreichte_ects), "Art": "Offen bis Jahresziel"},
            {"Jahr": "2027", "ECTS": 60, "Art": "Jahresziel"},
            {"Jahr": "2028", "ECTS": 60, "Art": "Jahresziel"}
        ])

        jahresziel_balken = alt.Chart(jahresziel_daten).mark_bar().encode(
            x=alt.X("Jahr:N", title="Kalenderjahr"),
            y=alt.Y("ECTS:Q", title="ECTS"),
            color=alt.Color("Art:N", title="Zielstatus"),
            tooltip=["Jahr", "Art", "ECTS"]
        )

        ziel_grafik_col1, ziel_grafik_col2 = st.columns(2)

        with ziel_grafik_col1:
            st.write("ECTS bis zum Studienabschluss")
            st.altair_chart(ects_torte, use_container_width=True)

        with ziel_grafik_col2:
            st.write("Jahresziel 60 ECTS")
            st.altair_chart(jahresziel_balken, use_container_width=True)

        lernzeit_daten = pd.DataFrame(controller.lade_woechentliche_lernzeit())

        st.write("Lernzeitübersicht")

        if len(lernzeit_daten) == 0:
            st.info("Noch keine Lernzeiten für die Wochenübersicht vorhanden.")
        else:
            # Liniendiagramm: Lernzeit pro Kalenderwoche mit roter Zielwert-Linie.
            lernzeit_linie = alt.Chart(lernzeit_daten).mark_line(point=True).encode(
                x=alt.X("Woche:N", title="Kalenderwoche"),
                y=alt.Y("Stunden:Q", title="Lernzeit in Stunden"),
                tooltip=["Woche", "Stunden"]
            )

            ziel_linie = alt.Chart(pd.DataFrame([{"Ziel": lernzeit_ziel}])).mark_rule(
                color="red",
                strokeDash=[6, 4]
            ).encode(
                y="Ziel:Q"
            )

            st.altair_chart(
                (lernzeit_linie + ziel_linie).properties(height=320),
                use_container_width=True
            )
            st.caption(
                f"Zielwert: {lernzeit_ziel} Stunden pro Woche. "
                f"Aktueller Durchschnitt: {aktueller_wochendurchschnitt:.1f} Stunden."
            )

        st.subheader("Aktive Kurse")

        if len(aktive_kurse) == 0:
            st.info("Derzeit sind keine Kurse in Bearbeitung")
        else:
            for kurs in aktive_kurse:
                with st.container():
                    st.markdown(f"### {kurs.kursname}")
                    st.write(f"ECTS: {kurs.ects}")
                    st.write(f"Semester: {kurs.semester}")
                    st.write(f"Status: {kurs.status.value}")

                    gesamtstunden = controller.gesamt_lernzeit(kurs.kursname)
                    st.write(f"Lernzeit gesamt: {gesamtstunden} h")
                    fehlende_voraussetzungen = controller.fehlende_voraussetzungen(kurs)

                    # Falls ein Kurs früher versehentlich gestartet wurde,
                    # obwohl Voraussetzungen fehlen, kann er hier zurückgesetzt werden.
                    if len(fehlende_voraussetzungen) > 0:
                        st.warning(
                            "Dieser Kurs wurde gestartet, obwohl noch Voraussetzungen fehlen: "
                            + ", ".join(fehlende_voraussetzungen)
                        )

                        if st.button("Kurs zurücksetzen", key=f"reset_aktiv_{kurs.kursname}"):
                            controller.kurs_zuruecksetzen(kurs)
                            st.success(f"{kurs.kursname} wurde zurückgesetzt.")
                            st.rerun()

                    col1, col2 = st.columns(2)

                    with col1:
                        if st.button("Lernzeit eintragen", key=f"lernzeit_{kurs.kursname}"):
                            lernzeit_dialog(kurs.kursname)

                    with col2:
                        if st.button("Prüfung eintragen", key=f"pruefung_{kurs.kursname}"):
                            pruefung_dialog(kurs)

                    st.write("---")

    with tab2:

        st.subheader("Offene Kurse")
        semester_liste = []

        if len(offene_kurse) == 0:
            st.warning("Keine offenen Kurse vorhanden.")

        else:
            semester_liste = sorted(
                set(kurs.semester for kurs in offene_kurse)
            )

        for semester in semester_liste:
            st.markdown(f"### Semester {semester}")
            kurse_im_semester = [
                kurs
                for kurs in offene_kurse
                if kurs.semester == semester
            ]

            for kurs in kurse_im_semester:
                st.write(
                    f"**{kurs.kursname}** | "
                    f"{kurs.ects} ECTS | "
                    f"{kurs.status.value}"
                )

                if len(kurs.voraussetzungen) > 0:
                    st.caption(
                        "Voraussetzungen: "
                        + ", ".join(kurs.voraussetzungen)
                    )

                aktion_col1, aktion_col2 = st.columns(2)
                fehlende_voraussetzungen = controller.fehlende_voraussetzungen(kurs)

                with aktion_col1:
                    # Der Startbutton wird deaktiviert, solange Voraussetzungen fehlen.
                    if st.button(
                        "Kurs starten",
                        key=f"start_{kurs.kursname}",
                        disabled=len(fehlende_voraussetzungen) > 0
                    ):
                        controller.kurs_aktivieren(kurs)
                        st.success(f"{kurs.kursname} wurde gestartet.")
                        st.rerun()

                    if len(fehlende_voraussetzungen) > 0:
                        st.warning(
                            "Start erst möglich nach: "
                            + ", ".join(fehlende_voraussetzungen)
                        )

                with aktion_col2:
                    # Angerechnete Kurse zählen für ECTS, haben aber keine Note.
                    if st.button("Kurs anrechnen", key=f"anrechnen_offen_{kurs.kursname}"):
                        controller.kurs_anrechnen(kurs)
                        st.success(f"{kurs.kursname} wurde angerechnet.")
                        st.rerun()

                st.write("---")

    with tab3:

        st.subheader("Abgeschlossene Kurse")

        # Angerechnete Kurse werden hier mit angezeigt, aber ohne Note.
        abgeschlossene_kurse = [
            kurs
            for kurs in kurse
            if kurs.status.value in ["Abgeschlossen", "Angerechnet"]
        ]

        if len(abgeschlossene_kurse) == 0:

            st.info(
                "Noch keine abgeschlossenen Kurse vorhanden."
            )

        else:

            for kurs in abgeschlossene_kurse:

                st.write(
                    f"**{kurs.kursname}** | "
                    f"{kurs.ects} ECTS | "
                    f"{kurs.status.value}"
                )

                if kurs.status.value == "Angerechnet":
                    st.caption("Angerechnet ohne Note. Dieser Kurs fließt nicht in den Notendurchschnitt ein.")
                else:
                    # Prüfungsnoten werden nur bei wirklich abgeschlossenen Kursen angezeigt.
                    pruefungen = controller.lade_pruefungen(kurs.kursname)
                    for pruefung in pruefungen:
                        st.caption(
                            f"{pruefung.pruefungsart.value} am {pruefung.datum} | "
                            f"Note: {pruefung.note}"
                        )

                if st.button("Zurücksetzen", key=f"reset_{kurs.kursname}"):
                    # Zurücksetzen korrigiert versehentliche Abschlüsse oder Anrechnungen.
                    controller.kurs_zuruecksetzen(kurs)
                    st.success(f"{kurs.kursname} wurde zurückgesetzt.")
                    st.rerun()
