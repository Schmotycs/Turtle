from pathlib import Path
import numpy as np
import tkinter as tk
import sys
import time
from collections import deque

class Tor:
    used_length = 0
    place = deque()

    def __init__(self, id, max_length):
        self.id = id
        self.max_length = max_length
        self.used_length = Tor.used_length
        self.place = Tor.place

    def reinlassen(self, Turtle):
        global Zustände
        self.used_length += Turtle.length
        if self.used_length > self.max_length:
            print(f"Schildkröte {Turtle.id} hat im Tor {self.id} kein Platz")
        if Turtle.in_gate == 0:
            self.place.appendleft(Turtle.id)
        else:
            self.place.append(Turtle.id)
        zustand = self.place
        Zustände.append(zustand.copy())        

    def rauslassen(self, Turtle):
        global Zustände
        self.used_length -= Turtle.length
        if Turtle.out_gate == 0:
            if self.place[0] == Turtle.id:
                self.place.popleft()
            else:
                self.place.remove(Turtle.id)
                print(f"Schildkröte {Turtle.id} konnte links nicht rausfahren")
        else:
            if self.place[-1] == Turtle.id:
                self.place.pop()
            else:
                self.place.remove(Turtle.id)
                print(f"Schildkröte {Turtle.id} konnte rechts nicht rausfahren")
        zustand = self.place
        Zustände.append(zustand.copy())





class Turtle:
    status = -1
    koordinaten = [400, 400]
    color = "green"
    radius = 200

    def __init__(self, id, length, in_trip, in_pos, in_time, in_gate, out_trip, out_pos, out_time, out_gate, tor):
        self.id = id
        self.length = length
        self.in_trip = in_trip
        self.in_pos = in_pos
        self.in_time = in_time
        self.in_gate = in_gate
        self.out_trip = out_trip
        self.out_pos = out_pos
        self.out_time = out_time
        self.out_gate = out_gate
        self.tor = tor
        self.status = Turtle.status
        self.koordinaten = Turtle.koordinaten
        self.color = Turtle.color
        self.radius = Turtle.radius



    def reinlaufen(self):
        if self.status == -1:
            if self.in_gate == 0:
                richtung = "links"
            else: 
                richtung = "rechts"
            print(f"Schildkröte {self.id} ist um {self.in_time} von {richtung} reingelaufen")
            self.status = 0
            self.tor.reinlassen(self)
        else:
            print(f"Schildkröte {self.id} kann nicht ein zweitesmal reinfahren")
            sys.exit()
        

        

    def rauslaufen(self):
        if self.status == 0:
            if self.in_gate == 0:
                Tor = "links"
            else: Tor = "rechts"
            print(f"Schildkröte {self.id} ist um {self.out_time} aus {Tor} rausgelaufen")
            self.status = 1
            self.tor.rauslassen(self)
        else:
            print(f"Schildkröte {self.id} kann nicht rauslaufen ohne im Tor zu sein")
            sys.exit()
    
    
def daumenkino(Zustände):
    r = 20
    root = tk.Tk()
    canvas = tk.Canvas(root, width=600, height=600)
    canvas.pack()

    def Bild(i):
        canvas.delete("all")

        if i == len(Zustände):
            return
        
        n = len(Zustände[i])
        for j in range(n):
            x = 400 - 50 * (n-j-1)
            y = 400
            canvas.create_oval(x-r, y+r, x+r, y-r, fill="green")
            canvas.create_text(x,y, text=str(Zustände[i][j]))

        root.after(1500, lambda: Bild(i+1))

    Bild(0)
    root.mainloop()  



def Start(Pfad):
    global Zustände

    tor = Tor(1, 260000)
    Daten = np.genfromtxt(Pfad, delimiter=";", dtype=int, skip_header=1)
    anzahl_zeilen, _ = Daten.shape
    Schildkroeten = []
    for i in range(anzahl_zeilen): 
        Schildkroete = Turtle(int(Daten[i,0]), Daten[i,1], Daten[i,2], Daten[i,3], Daten[i,4], Daten[i,5], Daten[i,6], Daten[i,7], Daten[i,8], Daten[i,9], tor)
        Schildkroeten.append(Schildkroete)


    
    Reihenfolge_in = []
    Zeiten_out = []
    Zeiten_in = []

    for i in range(anzahl_zeilen-1, -1, -1):
        Reihenfolge_in.append(Schildkroeten[i].id)
        Zeiten_in.append(Schildkroeten[i].in_time)
        Zeiten_out.append(Schildkroeten[i].out_time)


    Reihenfolge_out = list(zip(Reihenfolge_in, Zeiten_out))
    Reihenfolge_out.sort(key=lambda x: x[1], reverse=True)
    Reihenfolge_in = list(zip(Reihenfolge_in, Zeiten_in))
    Reihenfolge_in.sort(key= lambda x: x[1], reverse=True)


    zaehler_in = anzahl_zeilen -1
    zaehler_out = anzahl_zeilen -1




    while (zaehler_in >= 0) or (zaehler_out >= 0):
        if zaehler_in >= 0:
            if Reihenfolge_in[zaehler_in][1] < Reihenfolge_out[zaehler_out][1]:
                Schildkroeten[zaehler_in].reinlaufen()
                zaehler_in -= 1
            else:
                Schildkroeten[Reihenfolge_out[zaehler_out][0]].rauslaufen()
                zaehler_out -= 1

        else:
            Schildkroeten[Reihenfolge_out[zaehler_out][0]].rauslaufen()
            zaehler_out -= 1

    daumenkino(Zustände)

       


Pfad = Path("C:/Users/dek/Documents/Turtle/TabellenSauber/Tabelle_10.csv")
Zustände = []

Start(Pfad)

 