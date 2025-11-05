from collections import deque
import tkinter as tk


class Tor:
    def __init__(self, id, max_length):
        self.id = id
        self.max_length = max_length
        self.used_length = 0
        self.place =  deque()

    def reinlassen(self, turtle):

        if turtle.in_gate == 0:
            self.place.appendleft(turtle.id)
        else:
            self.place.append(turtle.id)

    
    def rauslassen(self, turtle):
        if turtle.out_gate == 0:
            self.place.popleft()
        else:
            self.place.pop()



    def kann_rauslaufen(self, turtle):
        if not self.place:
            return False
        
        if turtle.out_gate == 0:
            if self.place[0] == turtle.id:
                return True
            else:
                return False
        else:
            if self.place[-1] == turtle.id:
                return True
            else:
                return False


class Turtle:
    status = -1 #-1: T war noch nicht im Tor, 0: T ist gerade im Tor, 1: T war schon im Tor

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
        self.status = Turtle.status


    def reinlaufen(self, sim):
        if self.status == -1:
            sim.reinlassen(self)
            self.status = 0
        else:
            sim.message(sim.index, f"Schildkröte {self.id} kann nicht ein zweitesmal reinfahren")
            
        

    def rauslaufen(self, sim):
        if self.status == 0:
            sim.rauslassen(self)
            self.status = 1
        else:
            sim.message(sim.index, f"Schildkröte {self.id} kann nicht rauslaufen ohne im Tor zu sein")


class Simulation:
    def __init__(self, tor):
        self.tor = tor
        self.states = []
        self.log = []
        self.index = 0
    
    def reinlassen(self, turtle):
        self.index += 1
        self.tor.used_length += turtle.length

        if self.tor.used_length > self.tor.max_length:
            self.message(self.index, f"Schildkröte {Turtle.id} hat im Tor {self.tor.id} kein Platz")

        self.tor.reinlassen(turtle)
            
        if turtle.in_gate == 0:

            self.states_log(self.tor.place.copy())
            richtung = "links"
        else:
            self.states_log(self.tor.place.copy())
            richtung = "rechts"

        self.message(self.index, f"Schildkröte {turtle.id} lief um {turtle.in_time} von {richtung} rein")
        

    
    def rauslassen(self, turtle):
        self.index += 1
        if self.tor.kann_rauslaufen(turtle) == False:
            self.message(self.index, f"Schildkröte {turtle.id} ist blockiert und kann nicht nach {turtle.out_gate} raus")

        self.tor.used_length -= turtle.length

        self.tor.rauslassen(turtle)

        if turtle.out_gate == 0:
            self.states_log(self.tor.place.copy())
            richtung = "links"
        else:
            self.states_log(self.tor.place.copy())
            richtung = "rechts"

        self.message(self.index, f"Schildkröte {turtle.id} lief um {turtle.out_time} von {richtung} raus")


    def message(self, index, msg):
        self.log.append((index, msg))

    def states_log(self, state):
        self.states.append((state))



    def Animation(self):
        r = 20
        root = tk.Tk()
        canvas = tk.Canvas(root, width=600, height=600)
        canvas.pack()

        def Bild(i):
            canvas.delete("all")
            root.title(f"Aktion {self.log[i][0]}/{len(self.log)}")
            canvas.create_text(300, 100, text = self.log[i][1])
            if i == len(self.states):
                return
            
            n = len(self.states[i])
            for j in range(n):
                x = 400 - 50 * (n-j-1)
                y = 400
                canvas.create_oval(x-r, y+r, x+r, y-r, fill="green")
                canvas.create_text(x,y, text=str(self.states[i][j]))

            root.after(1500, lambda: Bild(i+1))

        Bild(0)
        root.mainloop() 
