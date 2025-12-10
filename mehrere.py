from pathlib import Path
import csv
from main import run


Tabellennamen = Path("C:/Users/dek/Documents/Turtle/TestTrack/Tabellen.csv")
Tabellenüberschriften = []
with open(Tabellennamen, newline="", encoding="utf-8", ) as df:
    reader = csv.reader(df, delimiter=";")
    for zeile in reader:
        Tabellenüberschriften.append(zeile[0].strip())

ausgabedatei = Path("C:/Users/dek/Documents/Turtle/TestTrackSauber/Kosten.csv")


with ausgabedatei.open(mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f,delimiter=";")
    writer.writerow(["Track", "Kosten"])
    for name in Tabellenüberschriften:
        Pfad = Path(rf"C:/Users/dek/Documents/Turtle/TestTrackSauber/{name}")

        kosten = run(Pfad)
        writer.writerow([name, kosten])