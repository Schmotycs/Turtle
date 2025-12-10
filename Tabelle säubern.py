import csv
from pathlib import Path
import numpy as np
import pandas as pd


pfad = Path("C:/Users/dek/Documents/Turtle/TestTrack/Tabellen.csv")

df = pd.read_csv(pfad, sep=";", header=None, encoding="utf-8")
überschriften = df.iloc[:, 0].tolist()


Eingabeordner = Path("C:/Users/dek/Documents/Turtle/TestTrack")
Ausgabeordner = Path("C:/Users/dek/Documents/Turtle/TestTrackSauber")


for i in range(len(überschriften)):
    Eingabedatei = Eingabeordner / überschriften[i]
    Ausgabedatei = Ausgabeordner / überschriften[i]

    df = pd.read_csv(Eingabedatei, sep =";", encoding="utf-8")
    df = df.drop(columns=[" Vehicle Type"])

    df[" in gate"] = df[" in gate"].replace({"(L)": 0,"(R)": 1})
    df[" out gate"] = df[" out gate"].replace({"(L)": 0,"(R)": 1})
    df[" in time"] = pd.to_timedelta(df[" in time"].astype(str)).dt.total_seconds().astype(int)
    df[" out time"] = pd.to_timedelta(df[" out time"].astype(str)).dt.total_seconds().astype(int)


    df.to_csv(Ausgabedatei, sep=";", index=False, encoding="utf-8")
    print(f"Tabelle {Ausgabedatei} wurde gespeichert")



