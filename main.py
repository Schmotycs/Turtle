from pathlib import Path
import loader
import Model
from collections import defaultdict



def run(csv_Path: Path):
    data = loader.load_csv(csv_Path) #csv wird ausgelesen
    tor = Model.Tor(1, 260000)  #Tor wird mit Länge erstellt
      

    number_of_trains, _ = data.shape

    Turtles = []
    for i in range(number_of_trains):   #für jede Zeile wird ein einzelnes Objekt erstellt
        t = Model.Turtle(data[i,0], data[i,1], data[i,2], data[i,3], data[i,4], data[i,5], data[i,6], data[i,7], data[i,8], data[i,9])
        Turtles.append(t)

    sim = Model.Simulation(tor, Turtles)

    order_in = []
    time_in = []
    time_out = []

    for i in range(number_of_trains-1,-1,-1):   #2 listen die nach reinlaufzeit und rauslaufzeit sortiert werden
        order_in.append(Turtles[i].id)
        time_in.append(Turtles[i].in_time)
        time_out.append(Turtles[i].out_time)

    order_out = list(zip(order_in, time_out))
    order_out.sort(key=lambda x: x[1], reverse=True)

    #Fahrzeuge die zusammen reifahren werden in eine Gruppe gesteckt
    order_in = list(zip(order_in, time_in))
    groups = defaultdict(list)
    
    for i in Turtles:
        groups[(i.in_trip, i.in_time)].append(i.id)

    order_in = [((tuple(ids)), time) for (trip, time), ids in groups.items()]
    
    order_in.sort(key= lambda x: x[1], reverse=True)
    print(order_in)
    print(order_out)

    index_in = len(order_in) -1
    index_out = len(order_out) -1

    while (index_in >= 0) or (index_out >=0):       #es wird überprüft in welcher reihenfolge die schildkörten rein und rauslaufen
        if index_in >= 0:
            if order_in[index_in][1] < order_out[index_out][1]:
                if len(order_in[index_in][0]) == 1:
                    Turtles[order_in[index_in][0][0]].reinlaufen(sim)
                else:
                    verbund = []
                    for i in range(len(order_in[index_in][0])):
                        verbund.append(Turtles[order_in[index_in][0][i]])
                    verbund_turtles = Model.Verbund(verbund)
                    verbund_turtles.reinlaufen(sim)
                index_in -= 1
            else:
                Turtles[order_out[index_out][0]].rauslaufen(sim)
                index_out -= 1
        else:
            Turtles[order_out[index_out][0]].rauslaufen(sim)
            index_out -=1
    sim.Animation()




Pfad = Path("C:/Users/dek/Documents/Turtle/TabellenSauber/Testlinksrechts.csv")

run(Pfad)

 #Kuppelungen hinzufügen (trip UND in/out time sind gleich)
    #out kuppeln hinzufügen und rein/laus methoden updaten 
 #Log am Ende (wie viele Züge, wie viele Fehler etc)