from pathlib import Path
import pandas as pd
from Main import run
import numpy as np
import K_Means
import matplotlib.pyplot as plt
from collections import Counter

def säubern_und_prüfen(Eingabeordner, Ausgabeordner, Dateiname):


    Eingabedatei = Eingabeordner / Dateiname
    Ausgabedatei = Ausgabeordner / Dateiname
    print(Dateiname)

    with Eingabedatei.open(encoding="utf-8") as eingabe:
        _ = eingabe.readline()
        meta = eingabe.readline()
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
    AnzahlZüge_pro_Spalte = []
    AnzahlKonf_pro_Spalte = []
    
    for datei in sorted(ordner_sauber.iterdir(), key=lambda p: p.name):
        #print(f"der datei name ist {datei}")
        WrongTimeOrder, Deadlock, Position, Bahnhofslänge, AnzahlZüge, AnzahlKonflikte = run(datei, 182000, 1)
        
        dateiname, Bahnhof = datei.name.split(".csv",1)
        Bahnhof = Bahnhof[1:-4]

        ergebnisse.append([dateiname, Bahnhof, WrongTimeOrder, Deadlock, Position, Bahnhofslänge,])

        AnzahlKonf_pro_Spalte.append(AnzahlKonflikte)
        AnzahlZüge_pro_Spalte.append(AnzahlZüge)
    

    df_ergebnisse = pd.DataFrame(ergebnisse, columns=["dateiname","Bahnhof","TimeOrder", "Deadlock", "Postion", "Bahnhofslänge"])
    df_ergebnisse.to_csv(f"Auswertung_{k}.csv", sep=";", index = False, encoding ="utf-8")
    return AnzahlZüge_pro_Spalte, AnzahlKonf_pro_Spalte



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
    return Varianz_der_Spalten, Mittelwert_der_Spalten

Dateinamen = "csv"

original = Path(rf"C:\Users\dek\Documents\tracks\{Dateinamen}")
sauber = Path(rf"C:\Users\dek\Documents\tracks\{Dateinamen}_sauber")
#säubern_ganzen_ordner(original, sauber)



AnzahlZüge, AnzahlKonflikte = run_für_ganzen_ordner(sauber, Dateinamen)

Pfad_Auswertung = Path(rf"C:\Users\dek\Documents\Turtle\Auswertung_{Dateinamen}.csv")
Pfad_genormt = Path(rf"C:\Users\dek\Documents\Turtle\genormte_werte_{Dateinamen}.csv")

Varianzen, Mittelwerte = Werte_normieren(Pfad_Auswertung, Dateinamen)



#SSE Diagramm
k = []
y = []

for i in range(10):
    sil, sse = K_Means.k_means(Pfad_genormt, i+2, Varianzen, Mittelwerte)
    k.append(i+2)
    y.append(sse)


fig, ax = plt.subplots()
ax.plot(k,y)
ax.set(xlim=(2, 6), xticks=np.arange(2, max(k)+2,1),
       ylim=(0, max(y)*1.1))
ax.grid(True)
ax.set_xlabel('k')
ax.set_ylabel('SSE(k)')
ax.set_title('Summe der quadrierten inneren Abstände')
plt.show()


#2 Konflikte gegenüberstellen
K_Means.k_means(Pfad_genormt, 4, x_achse=0, y_achse=1, Diagramm=True, sil = True)


#AnzahlZüge gegen Konfliktanzahl
punkte = list(zip(AnzahlZüge, AnzahlKonflikte))
häufigkeit = Counter(punkte)
größen = [häufigkeit[(x,y)] * 5 for x,y in punkte] 
fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(AnzahlZüge, AnzahlKonflikte, s = größen)
ax.set_xlabel('Anzahl der Züge')
ax.set_ylabel('Anzahl Konflikte (gesamt)')
ax.set_title('Konflikte vs. Anzahl Züge')
ax.grid(True)
plt.tight_layout()
plt.show()


