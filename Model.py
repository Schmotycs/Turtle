from collections import deque
import tkinter as tk


class Tor:  #simmuliert ein Gleis und speichert die Zustände zum welchen Zeitpunkt welche Schildkröte da ist und wie und wo rausläuft
    def __init__(self, id, max_length):
        self.id = id
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
            #auf Deadlock prüfen

            self.strafkosten_erhöhen(0) #Coupling Middle



    def verbund_rauslassen(self, verbund, ids, sim):
        if self.verbund_position_order_prüfen(verbund) == False:
            self.strafkosten_erhöhen(1) #Falsche Verbund reihenfolge
            sim.message_log(sim.index, f"Schildkrötenverund aus den Schildkröten {ids} ist beim ausfahren nicht in der richtigen Reihenfolge")

        if self.verbund_kann_rauslaufen(verbund, ids) == True:
            if verbund.out_gate == 0:
                for i in range(len(verbund.t_zsm)):
                    self.place.popleft()
            else:
                for i in range(len(verbund.t_zsm)):
                    self.place.pop()
        else:
            for id in ids:
                self.place.remove(id)
                self.strafkosten_erhöhen(0) #Coupling Middle/ Man müsste prüfen ob WrongTimeOrder günstiger ist

        


    def verbund_position_order_prüfen(self, verbund):#Überprüfen ob beim rauslaufen die richtige Reihenfolge ist
        akt_position = self.place.index(verbund.t_zsm[0].id)
        if verbund.out_gate == 0:
            for i in range(len(verbund.t_zsm)):
                if akt_position + i >= len(self.place):
                    return False
                if self.place[akt_position+i] != verbund.t_zsm[i].id:
                    return False
        else:
            for i in range(len(verbund.t_zsm)):
                if akt_position - i < 0:
                    return False
                if self.place[akt_position-i] != verbund.t_zsm[i].id:
                    return False


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
        
    def strafkosten_erhöhen(self, Kostenart): #0 = Kuppeln aus der Mitte, 1 = falsche Verbund reihenfolge, 2 = WrongTimeOrder, 3 = Deadlock, 4 = Bahnhofslänge
        self.Straf_Kosten[Kostenart] += self.Kosten_pro_Stück[Kostenart]




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
            ids.append(int(verbund.t_zsm[i].id))

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
            ids.append(int(verbund.t_zsm[i].id))

        if self.tor.verbund_kann_rauslaufen(verbund, ids) == False:
            self.message_log(self.index, f"Schildkörtenverbund aus den Schildkröten {ids} ist blockiert")
        
        self.tor.used_length -= verbund_length

        self.tor.verbund_rauslassen(verbund, ids, self)

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
        r = 23
        root = tk.Tk()
        höhe = 600
        breite = 600
        Zughöhe = 350
        canvas = tk.Canvas(root, width=breite, height=höhe)
        canvas.pack()
        root.bind("<Return>", lambda e: Bild(0))


        def Bahnhof():
            canvas.delete("all")

            root.title(f"Aktion 0/{len(self.states)}")
            canvas.create_rectangle(-10, Zughöhe+10, breite+10, Zughöhe-10, fill="azure3", width=4)
            canvas.create_text(25, Zughöhe-35, text= str("L"), fill="green3", font=("Segoe UI", 16))
            canvas.create_text(breite-25, Zughöhe-35, text= str("R"), fill="red2", font=("Segoe UI", 16))
            
            x_pos = 0
            while x_pos < breite:
                canvas.create_rectangle(x_pos+3, Zughöhe+15, x_pos-3, Zughöhe-15, fill="sienna4")
                x_pos += 30


        def Bild(i):
            canvas.delete("all")
            if i >= len(self.states):
                return
            Bahnhof()

            
            root.title(f"Aktion {i+1}/{len(self.states)}")

            n = len(self.states[i])
    
            

            for j in range(n):
                x = 350 - 50*(n-j-1)

                canvas.create_oval(x-r, Zughöhe+r, x+r, Zughöhe-r, fill="green")    #Ball
                canvas.create_text(x,Zughöhe, text=str(self.states[i][j]))    #Nummer


            for j in range(len(self.messages[i+1])):    #Log nachrichten
                canvas.create_text(50, 100+30*j, text = f"- {self.messages[i+1][j]}", anchor="w")
                
        index = -1

        def weiter(event = None):
            nonlocal index
            index += 1
            Bild(index)
        
        Bahnhof()

        root.bind("<Return>", weiter)

        root.mainloop() 

   
