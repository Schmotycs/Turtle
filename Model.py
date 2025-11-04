from collections import deque

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


    def reinlaufen(self, sim):
        if self.status == -1:
            sim.reinlassen(self)
            self.status = 0
        else:
            print(f"Schildkröte {self.id} kann nicht ein zweitesmal reinfahren")
            
            



    def rauslaufen(self, sim):
        if self.status == 0:
            sim.rauslassen(self)
            self.status = 1
        else:
            print(f"Schildkröte {self.id} kann nicht rauslaufen ohne im Tor zu sein")


class Simulation:
    def __init__(self, tor):
        self.tor = tor
        self.states = []
        self.log = []
    
    def reinlassen(self, turtle):
        self.tor.used_length += turtle.length

        if self.tor.used_length > self.tor.max_length:
            self.message(f"Schildkröte {Turtle.id} hat im Tor {self.tor.id} kein Platz")

        self.tor.reinlassen(turtle)
            
        if turtle.in_gate == 0:

            self.states.append(self.tor.place.copy())
            richtung = "links"
        else:
            self.states.append(self.tor.place.copy())
            richtung = "rechts"

        self.message(f"Schildkröte {turtle.id} lief um {turtle.in_time} von {richtung} rein")
        

    
    def rauslassen(self, turtle):
        if self.tor.kann_rauslaufen(turtle) == False:
            self.message(f"Schildkröte {turtle.id} ist blockiert und kann nicht nach {turtle.out_gate} raus")

        self.tor.used_length -= turtle.length

        self.tor.rauslassen(turtle)

        if turtle.out_gate == 0:
            self.states.append(self.tor.place.copy())
            richtung = "links"
        else:
            self.states.append(self.tor.place.copy())
            richtung = "rechts"

        self.message(f"Schildkröte {turtle.id} lief um {turtle.out_time} von {richtung} raus")





    def message(self, msg):
        self.log.append(msg)

    def state(self, index):
        return self.states[index]
    

    