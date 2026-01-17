from pathlib import Path
import pandas as pd
from Main import run

def säubern_und_prüfen(Eingabeordner, Ausgabeordner, Dateiname):


    Eingabedatei = Eingabeordner / Dateiname
    Ausgabedatei = Ausgabeordner / Dateiname

    df = pd.read_csv(Eingabedatei, sep =";", encoding="utf-8")
    df = df.drop(columns=[" Vehicle Type"])
    df[" in gate"] = df[" in gate"].replace({"(L)": 0,"(R)": 1})
    df[" out gate"] = df[" out gate"].replace({"(L)": 0,"(R)": 1})
    df[" in time"] = pd.to_timedelta(df[" in time"].astype(str)).dt.total_seconds().astype(int)
    df[" out time"] = pd.to_timedelta(df[" out time"].astype(str)).dt.total_seconds().astype(int)

    #print(f"Tabelle {Dateiname} wurde gesäubert")

    for Zeile, Spalte in df.iterrows():
        Einfahrtszeit = Spalte[" in time"]
        Ausfahrtszeit = Spalte[" out time"]

        if Einfahrtszeit > Ausfahrtszeit:
            print("Ausfahrtszeit darf nicht kleiner als Einfahrtszeit sein")
        elif Einfahrtszeit == Ausfahrtszeit:
            df.at[Zeile, " out time"] += 1
            print(f"In der Datei {Dateiname} wurde die Ausfahrtszeit von {Zeile} wurde um 1 erhöht")

    #print(f"Tabelle {Dateiname} wurde überprüft")

    df.to_csv(Ausgabedatei, sep=";", index=False, encoding="utf-8")
    print(f"Tabelle {Dateiname} wurde gespeichert")


def run_für_ganzen_ordner(ordner_sauber):
    ordner_sauber.mkdir(parents=True, exist_ok=True)
    ergebnisse = []
    
    for datei in sorted(ordner_sauber.iterdir(), key=lambda p: p.name):
        Anzhal_Züge, WrongTimeOrder, Deadlock, Position, Bahnhofslänge, anzahl_verbünde_in, anzahl_verbünde_out, durchschnittslänge_verbünde_in, durchschnittslänge_verbünde_out = run(datei)
        Summe = WrongTimeOrder + Deadlock + Position + Bahnhofslänge
        ergebnisse.append([datei.name, Anzhal_Züge, WrongTimeOrder, Deadlock, Position, Bahnhofslänge, Summe, anzahl_verbünde_in, anzahl_verbünde_out, durchschnittslänge_verbünde_in, durchschnittslänge_verbünde_out])


    df_ergebnisse = pd.DataFrame(ergebnisse, columns=["dateiname","Anzahl Züge", "TimeOrder", "Deadlock", "Postion", "Bahnhofslänge", "Summe", "Anzahl Verbünde in", "Anzahl Verbünde out", "Länge Verbünde in", "Länge Verbünde out"])
    df_ergebnisse.to_csv("Auswertung.csv", sep=";", index = False, encoding ="utf-8")



def säubern_ganzen_ordner(ordner_original, ordner_sauber):
    ordner_sauber.mkdir(parents=True, exist_ok=True)

    for datei in sorted(ordner_original.iterdir(), key=lambda p: p.name):
        säubern_und_prüfen(ordner_original, ordner_sauber, datei.name)




original = Path(r"C:\Users\dek\Documents\tracks539\csv")
sauber = Path(r"C:\Users\dek\Documents\tracks539\csv_sauber")

#säubern_ganzen_ordner(original, sauber)
run_für_ganzen_ordner(sauber)