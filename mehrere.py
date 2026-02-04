from pathlib import Path
import pandas as pd
from Main import run
import numpy as np

def säubern_und_prüfen(Eingabeordner, Ausgabeordner, Dateiname):


    Eingabedatei = Eingabeordner / Dateiname
    Ausgabedatei = Ausgabeordner / Dateiname
    print(Dateiname)

    with Eingabedatei.open(encoding="utf-8") as ein:
        _ = ein.readline()
        meta = ein.readline()
        meta = meta.strip()
        abschnitte = meta.split()
        Location = abschnitte[1].rstrip(",")
        df = pd.read_csv(Eingabedatei, sep =";", encoding="utf-8", skiprows = 3)
    df = df.drop(columns=[" Vehicle Type"])
    df[" in gate"] = df[" in gate"].replace({"(L)": 0,"(R)": 1})
    df[" out gate"] = df[" out gate"].replace({"(L)": 0,"(R)": 1})
    df[" in time"] = pd.to_timedelta(df[" in time"].astype(str)).dt.total_seconds().astype(int)
    df[" out time"] = pd.to_timedelta(df[" out time"].astype(str)).dt.total_seconds().astype(int)


    for Zeile, Spalte in df.iterrows():
        Einfahrtszeit = Spalte[" in time"]
        Ausfahrtszeit = Spalte[" out time"]

        if Einfahrtszeit > Ausfahrtszeit:
            print("Ausfahrtszeit darf nicht kleiner als Einfahrtszeit sein")
        elif Einfahrtszeit == Ausfahrtszeit:
            df.at[Zeile, " out time"] += 1


    df.to_csv(f"{Ausgabedatei}_{Location}.csv", sep=";", index=False, encoding="utf-8")


def run_für_ganzen_ordner(ordner_sauber, k):
    ordner_sauber.mkdir(parents=True, exist_ok=True)
    ergebnisse = []
    
    for datei in sorted(ordner_sauber.iterdir(), key=lambda p: p.name):
        WrongTimeOrder, Deadlock, Position, Bahnhofslänge = run(datei)
        dateiname, Bahnhof = datei.name.split(".csv",1)
        Bahnhof = Bahnhof[1:-4]

        ergebnisse.append([dateiname, Bahnhof, WrongTimeOrder, Deadlock, Position, Bahnhofslänge,])


    df_ergebnisse = pd.DataFrame(ergebnisse, columns=["dateiname","Bahnhof","TimeOrder", "Deadlock", "Postion", "Bahnhofslänge"])
    df_ergebnisse.to_csv(f"Auswertung_{k}.csv", sep=";", index = False, encoding ="utf-8")



def säubern_ganzen_ordner(ordner_original, ordner_sauber):
    ordner_sauber.mkdir(parents=True, exist_ok=True)

    for datei in sorted(ordner_original.iterdir(), key=lambda p: p.name):
        säubern_und_prüfen(ordner_original, ordner_sauber, datei.name)


def Werte_normieren(data, k):
    dateinamen = np.genfromtxt(data, delimiter =";", skip_header = 1, dtype=str, usecols=0)
    Bahnhofsnahmen = np.genfromtxt(data, delimiter =";", skip_header = 1, dtype=str, usecols=1)
    werte = np.genfromtxt(data, delimiter = ";", skip_header = 1, dtype=float)
    werte = werte[:, 2:]

    anzahl_zeilen, anzahl_spalten = werte.shape
    
    Summe_der_Spalten = [0]*(anzahl_spalten)
    Mittelwert_der_Spalten = [0]*(anzahl_spalten)

    for i in range(anzahl_spalten):
        for j in range(anzahl_zeilen):
            Summe_der_Spalten[i] += werte[j,i]
    
    for i in range(anzahl_spalten):
        Mittelwert_der_Spalten[i] = Summe_der_Spalten[i]/anzahl_zeilen

    Varianz_der_Spalten = [0]*(anzahl_spalten)
    Summe_Abweichung_zu_Mitte_quadrat = [0]*(anzahl_spalten)

    for i in range(anzahl_spalten):
        for j in range(anzahl_zeilen):
            Summe_Abweichung_zu_Mitte_quadrat[i] += (werte[j,i]-Mittelwert_der_Spalten[i])**2

    for i in range(anzahl_spalten):
        Varianz_der_Spalten[i] = Summe_Abweichung_zu_Mitte_quadrat[i]/anzahl_zeilen

    ergebnisse_ges = []
 
    for i in range(anzahl_zeilen):
        zeile = []
        zeile.append(dateinamen[i])
        zeile.append(Bahnhofsnahmen[i])
        for j in range(anzahl_spalten):
            if Varianz_der_Spalten[j] == 0:
                z = 0.0
            else:
                z = (werte[i, j]-Mittelwert_der_Spalten[j])/np.sqrt(Varianz_der_Spalten[j])
            zeile.append(z)
        ergebnisse_ges.append(zeile)

    df_ergebnisse = pd.DataFrame(ergebnisse_ges, columns=["dateiname", "Bahnhof","TimeOrder", "Deadlock", "Postion", "Bahnhofslänge"])
    df_ergebnisse.to_csv(f"genormte_werte_{k}.csv", sep = ";", index= False, encoding="utf-8")


original = Path(r"C:\Users\dek\Documents\tracks\454NC")
sauber = Path(r"C:\Users\dek\Documents\tracks\454NC_sauber")

#säubern_ganzen_ordner(original, sauber)
#run_für_ganzen_ordner(sauber, 2)

Pfad_Auswertung = Path(r"C:\Users\dek\Documents\Turtle\Auswertung_2.csv")
Werte_normieren(Pfad_Auswertung, 2)