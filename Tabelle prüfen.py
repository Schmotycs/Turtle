import csv
from pathlib import Path
import numpy as np
import pandas as pd


pfad = Path("C:/Users/dek/Documents/Turtle/TestTrack/Tabellen.csv")

df = pd.read_csv(pfad, sep=";", header=None, encoding="utf-8")
überschriften = df.iloc[:, 0].tolist()


Eingabeordner = Path("C:/Users/dek/Documents/Turtle/TestTrackSauber")



for i in range(len(überschriften)):
    Eingabedatei = Eingabeordner / überschriften[i]

    df = pd.read_csv(Eingabedatei, sep =";", encoding="utf-8")
    for index, Spalte in df.iterrows():
        Einfahrtszeit = Spalte[" in time"]
        Ausfahrtszeit = Spalte[" out time"]

        if Einfahrtszeit > Ausfahrtszeit:
            print("Ausfahrtszeit darf nicht kleiner als Einfahrtszeit sein")
        elif Einfahrtszeit == Ausfahrtszeit:
            df.at[index, " out time"] += 1
            print(f"In der Datei {überschriften[i]} wurde die Ausfahrtszeit von {Ausfahrtszeit} von {i} wurde um 1 erhöht")
        


    df.to_csv(Eingabedatei, sep=";", index=False, encoding="utf-8")
    print(f"Tabelle {Eingabedatei} wurde gespeichert")



