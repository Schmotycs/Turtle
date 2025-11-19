from collections import deque
import tkinter as tk


class Tor:  #simmuliert ein Gleis und speichert die Zustände zum welchen Zeitpunkt welche Schildkröte da ist und wie und wo rausläuft
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

    def verbund_reinlassen(self, verbund):
        if verbund.in_gate == 0:
            for i in range(len(verbund.t_zsm)):
                self.place.appendleft(verbund.t_zsm[i].id)
        else:
            for i in range(len(verbund.t_zsm)):
                self.place.append(verbund.t_zsm[i].id)
    
    def rauslassen(self, turtle):
        if self.kann_rauslaufen(turtle) == True:
            if turtle.out_gate == 0:
                self.place.popleft()
            else:
                self.place.pop()
        else:
            self.place.remove(turtle.id)

    def verbund_rauslassen(self, verbund, ids):
        if self.verbund_kann_rauslaufen(verbund, ids) == True:
            if verbund.out_gate == 0:
                for i in range(len(verbund.t_zsm)):
                    self.place.popleft()
            else:
                self.place.pop()
        else:
            for id in ids:
                self.place.remove(id)




    def kann_rauslaufen(self, turtle):  #überprüft ob die Schildkröte einfach rauslaufen kann
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
            
    def verbund_kann_rauslaufen(self, verbund, ids):
        if verbund.out_gate == 0:
            for i in range(len(ids)):
                if self.place[i] not in ids:
                    return False
            return True
        else:
            for i in range(len(ids)):
                if self.place[-1-i] not in ids:
                    return False
            return True

class Turtle:   #Für jedes Fahrzeug wird ein Turtle Objekt erstellt, mit folgenden eigenschaftten:
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
        if self.status == -1:       #(-1) Schildkröte war noch nicht im Gleis
            sim.reinlassen(self)    #löst die reinlassfunktion von der Simulation auf
            self.status = 0
        else:
            sim.message_log(sim.index, f"Schildkröte {self.id} kann nicht ein zweitesmal reinfahren")
            


    def rauslaufen(self, sim):
        if self.status == 0:
            sim.rauslassen(self)
            self.status = 1
        else:
            sim.message_log(sim.index, f"Schildkröte {self.id} kann nicht rauslaufen ohne im Tor zu sein")

class Verbund:
    def __init__(self, t_zsm):
        self.t_zsm = t_zsm
        self.in_time = t_zsm[0].in_time
        self.in_gate = t_zsm[0].in_gate
        self.out_time = t_zsm[0].out_time
        self.out_gate = t_zsm[0].out_gate

    def reinlaufen(self, sim):
        for i in range(len(self.t_zsm)):
            if not self.t_zsm[i].status == -1:
                sim.message_log(sim.index, f"Schildköte {self.t_zsm[i].id} kann nicht ein zweitesmal reinlaufen")
                return
        sim.verbund_reinlassen(self)

        for i in range(len(self.t_zsm)):
            self.t_zsm[i].status = 0
        
    def rauslassen(self, sim):
        for i in range(len(self.t_zsm)):
            if not self.t_zsm[i].status == 0:
                sim.message_log(sim.index, f"Schildköte {self.t_zsm[i].id} kann nicht rauslaufen ohne im Tor zu sein")
                return
        sim.verbund_rauslassen(self)



class Simulation:
    def __init__(self, tor, turtles):
        self.tor = tor
        self.turtles = turtles
        self.states = []
        self.messages = []
        self.index = 0
    
    def reinlassen(self, turtle):
        self.index += 1
        self.tor.used_length += turtle.length

        if self.tor.used_length > self.tor.max_length:  #überprüft die maximale Gleislänge
            self.message_log(self.index, f"Schildkröte {turtle.id} hat im Tor {self.tor.id} kein Platz")

        self.tor.reinlassen(turtle)
            
        if turtle.in_gate == 0:     #kopiert den jetztigen Zustand vom Tor und speichert den
            self.states_log(self.tor.place.copy())
            richtung = "links"
        else:
            self.states_log(self.tor.place.copy())
            richtung = "rechts"

        self.message_log(self.index, f"Schildkröte {turtle.id} lief um {turtle.in_time} von {richtung} rein")


    def verbund_reinlassen(self, verbund):
        self.index += 1
        verbund_length = 0
        ids = []
        for i in range(len(verbund.t_zsm)):
            verbund_length += verbund.t_zsm[i].length
            ids.append(verbund.t_zsm[i].id)

        self.tor.used_length += verbund_length

        if self.tor.used_length > self.tor.max_length:  #überprüft die maximale Gleislänge
            self.message_log(self.index, f"Schildkrötenverbund aus den Schildkröten {ids} hat im Tor {self.tor.id} kein Platz")
        
        self.tor.verbund_reinlassen(verbund)

        if verbund.in_gate == 0:
            self.states_log(self.tor.place.copy())
            richtung = "links"
        else:
            self.states_log(self.tor.place.copy())
            richtung = "rechts"
        self.message_log(self.index, f"Schildkrötenverbund aus den Schildkröten {ids} lief um {verbund.in_time} von {richtung} rein")

    
    def rauslassen(self, turtle):   #Analog zu reinlassen
        self.index += 1
        if self.tor.kann_rauslaufen(turtle) == False:
            self.message_log(self.index, f"Schildkröte {turtle.id} ist blockiert und möchte nach {turtle.out_gate} raus")

        self.tor.used_length -= turtle.length

        self.tor.rauslassen(turtle)

        if turtle.out_gate == 0:
            self.states_log(self.tor.place.copy())
            richtung = "links"
        else:
            self.states_log(self.tor.place.copy())
            richtung = "rechts"

        self.message_log(self.index, f"Schildkröte {turtle.id} lief um {turtle.out_time} von {richtung} raus")

    def verbund_rauslassen(self, verbund):
        self.index += 1
        verbund_length = 0
        ids = []

        for i in range(len(verbund.t_zsm)):
            verbund_length += verbund.t_zsm[i].length
            ids.append(verbund.t_zsm[i].id)

        if self.tor.verbund_kann_rauslaufen(verbund, ids) == False:
            self.message_log(self.index, f"Schildkörtenverbund aus den Schildkröten {ids} ist blockiert")
        
        self.tor.used_length -= verbund_length

        self.tor.verbund_rauslassen(verbund, ids)

        if verbund.out_gate == 0:
            self.states_log(self.tor.place.copy())
            richtung = "links"
        else:
            self.states_log(self.tor.place.copy())
            richtung = "rechts"
        self.message_log(self.index, f"Schildkrötenverbund aus den Schildkröten {ids} lief um {verbund.out_time} aus {richtung} raus")



        
        



    def message_log(self, index, msg):  #speichert Texte um diese später wiederzugeben
        while len(self.messages) <= index:
            self.messages.append([])
        self.messages[index].append(msg)


    def states_log(self, state):
        self.states.append((state))



    def Animation(self):    #Animation wird erstellt
        r = 20
        root = tk.Tk()
        canvas = tk.Canvas(root, width=600, height=600)
        canvas.pack()
        root.bind("<Return>", lambda e: Bild(0))

        def Bild(i):
            canvas.delete("all")

            if i == len(self.states):
                return
            
            root.title(f"Aktion {i+1}/{len(self.states)}")

            n = len(self.states[i])
            for j in range(n):
                x = 350 - 50*(n-j-1)
                y = 350
                canvas.create_oval(x-r, y+r, x+r, y-r, fill="green")    #Ball
                canvas.create_text(x,y, text=str(self.states[i][j]))    #Nummer

                if self.turtles[self.states[i][j]].out_gate == 0:  #Pfeil
                    direction_out = tk.FIRST
                else:
                    direction_out = tk.LAST
                canvas.create_line(x-15, y-30, x+15, y-30, arrow=direction_out)

            for j in range(len(self.messages[i+1])):    #Log nachrichten
                canvas.create_text(50, 100+30*j, text = f"- {self.messages[i+1][j]}", anchor="w")
                
            

            root.bind("<Return>", lambda e: Bild(i+1))

        root.mainloop() 
