from pathlib import Path
import loader
import Model

def run(csv_Path: Path):
    data = loader.load_csv(csv_Path) #csv wird ausgelesen
    
      

    number_of_trains, _ = data.shape

    Turtles = []
    for i in range(number_of_trains):   #für jede Zeile wird ein einzelnes Objekt erstellt
        t = Model.Turtle(data[i,0], data[i,1], data[i,2], data[i,3], data[i,4], data[i,5], data[i,6], data[i,7], data[i,8], data[i,9])
        Turtles.append(t)

    tor = Model.Tor(1, 182000, Turtles)
    sim = Model.Simulation(tor, Turtles)
    Ereignisse = [] #Uhrzeit, Liste an IDs, Aktion (0 reinlaufen, 1 rauslaufen)

    order_in = []
    for i in range(number_of_trains):
        order_in.append([int(Turtles[i].id), int(Turtles[i].in_time), int(Turtles[i].in_trip)])
    
    order_in.sort(key=lambda x: x[1])#nach in_time sortieren
    
    order_in_new = []
    for turtle in order_in:
        turtle_id = turtle[0]
        in_time = turtle[1]
        in_trip = turtle[2]

        if len(order_in_new) == 0:
            order_in_new.append([[turtle_id], in_time, in_trip])
        else:
            letzter = order_in_new[-1]
            if in_time == letzter[1] and in_trip == letzter[2]:
                letzter[0].append(turtle_id)                               #Turtles mit gleicher inTrip und intime werden vereinigt
            else:
                order_in_new.append([[turtle_id], in_time, in_trip])

    order_out = []
    for i in range(number_of_trains):
        order_out.append([int(Turtles[i].id), int(Turtles[i].out_time), int(Turtles[i].out_trip)])
    order_out.sort(key=lambda x: x[1]) #nach out_time sortieren

    order_out_new = []
    for turtle in order_out:
        turtle_id = turtle[0]
        out_time = turtle[1]
        out_trip = turtle[2]

        if len(order_out_new) == 0:
            order_out_new.append([[turtle_id], out_time, out_trip])
        else:
            letzter = order_out_new[-1]
            if out_time == letzter[1] and out_trip == letzter[2]:
                letzter[0].append(turtle_id)
            else:
                order_out_new.append([[turtle_id], out_time, out_trip])
    

    for i in range(len(order_in_new)):
        order_in_new[i].append(0)
    for i in range(len(order_out_new)):
        order_out_new[i].append(1)
    
    Ereignisse = order_in_new + order_out_new
    Ereignisse.sort(key=lambda x: x[1])

    id_to_in_pos = {}
    for t in Turtles:
        id_to_in_pos[int(t.id)] = int(t.in_pos)

    id_to_out_pos = {}
    for t in Turtles:
        id_to_out_pos[int(t.id)] = int(t.out_pos)


    for ereignis in Ereignisse: #sortieren nach pos_nr
        if ereignis[3] == 0:   #Einfahrt
            ereignis[0].sort(key=lambda turtle_id: id_to_in_pos[turtle_id])
        else:
            ereignis[0].sort(key=lambda turtle_id: id_to_out_pos[turtle_id])
    

    for ereignis in Ereignisse:
        if ereignis[3] == 0: #Einfahrt
            if len(ereignis[0]) == 1:
                Turtles[ereignis[0][0]].reinlaufen(sim)
            else:
                verbund = []
                for i in range(len(ereignis[0])):
                    verbund.append(Turtles[ereignis[0][i]])
                verbund_turtles = Model.Verbund(verbund)
                verbund_turtles.reinlaufen(sim)
        else:
            if len(ereignis[0]) == 1:
                Turtles[ereignis[0][0]].rauslaufen(sim)
            else:
                verbund = []
                for i in range(len(ereignis[0])):
                    verbund.append(Turtles[ereignis[0][i]])
                verbund_turtles = Model.Verbund(verbund)
                verbund_turtles.rauslassen(sim)
            
    sim.Animation(Turtles)
    tor.strafkostenausgeben()

           


Pfad = Path("C:/Users/dek/Documents/Turtle/TabellenSauber/Tabelle_1.csv")

#Verbund bahhhofslänge einzlen berechenen nicht zusammen

run(Pfad)