from collections import deque
import tkinter as tk

class Turtle:
    def __init__(self, id, length, in_trip, in_pos, in_time, in_gate, out_trip, out_pos, out_time, out_gate):
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
        self.status = -1

class Tor:
    def __init__(self, max_length):
        self.max_length = max_length
        self.used_length = 0
        self.place =  deque()
        self.Straf_Kosten = 5*[0]
        self.Kosten_pro_Stück = [0.612500, 2.062500, 0.367500, 0.735000, 0]  #0 = Kuppeln aus der Mitte, 1 = falsche Verbund reihenfolge, 2 = WrongTimeOrder, 3 = Deadlock, 4 = Bahnhofslänge


    def reinlassen(self, turtle):
        if turtle.in_gate == 0:
            self.place.appendleft(turtle.id)
        else:
            self.place.append(turtle.id)
        
    def rauslassen(self, turtle):
        if self.kann_rauslaufen(self, turtle) == True:
            pass


    def kann_rauslaufen(self, turtle):
        if turtle.out_gate == 0:
            return self.place[0] == turtle.id
        else:
            return self.place[-1] == turtle.id

