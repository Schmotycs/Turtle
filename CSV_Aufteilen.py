import csv
from pathlib import Path
import numpy as np



Pfad = Path("C:/Users/dek/Documents/Turtle/E20-44521.xml-251002-110553-opt_1-tracks.csv")


with open(Pfad, mode="r", encoding="utf-8", newline="") as datei:
    daten = datei.readlines()


zeilen = []
for i in range(len(daten)):
    saubere_zeile = daten[i].strip()
    zeilen.append(saubere_zeile) 

tabellen = []
aktuelle_überschrift = None
aktuelle_tabelle = []

leere_zeile_index = 0
in_tabelle = False

for i in range(len(zeilen)):
    zeile = zeilen[i]

    if zeile == "":
        leere_zeile_index += 1
        continue

    if ";" not in zeile:
        if aktuelle_tabelle != []:
            tabellen.append((aktuelle_überschrift, aktuelle_tabelle))
            aktuelle_tabelle = []
        aktuelle_überschrift = zeile
        leere_zeile_index = 0
        in_tabelle = False

    elif leere_zeile_index >= 2:
        aktuelle_tabelle = []
        in_tabelle = True
        leere_zeile_index = 0
        aktuelle_tabelle.append(zeile.split(";"))

    elif in_tabelle:
        aktuelle_tabelle.append(zeile.split(";"))

if aktuelle_tabelle != []:
   tabellen.append((aktuelle_überschrift, aktuelle_tabelle))

Ausgabe = Path("C:/Users/dek/Documents/Turtle/Tabellen")
Ausgabe.mkdir(exist_ok=True)
überschriften = []

for i in range(len(tabellen)):
    überschrift = tabellen[i][0]
    tabelle = tabellen[i][1]


    dateiname_basis = f"Tabelle_{i+1}"
    dateiname = f"{dateiname_basis}.csv"

    überschriften.append(dateiname)
    dateipfad = Ausgabe / dateiname
    print(f"dateipfad {dateipfad}")

    with open(dateipfad, mode="w", newline="", encoding="utf-8") as ausgabedatei:
        writer = csv.writer(ausgabedatei, delimiter=";")
        for k in range(len(tabelle)):
            writer.writerow(tabelle[k])

    print(f"Tabelle '{überschrift}' gespeichert als '{dateiname}'")


dateipfad2 = Path("C:/Users/dek/Documents/Turtle/Tabellen/Tabellen.csv")


with open(dateipfad2, mode="w", newline="", encoding="utf-8") as ausgabedatei:
    writer = csv.writer(ausgabedatei, delimiter=";")
    for name in überschriften:
        writer.writerow([name])

print(f"CSV-Tabelle '{dateipfad2}' wurde gespeichert.")







