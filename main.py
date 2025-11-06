from pathlib import Path
import loader
import Model



def run(csv_Path: Path):
    data = loader.load_csv(csv_Path)
    tor = Model.Tor(1, 260000)
    sim = Model.Simulation(tor)

    number_of_trains, _ = data.shape
    Turtles = []
    for i in range(number_of_trains):
        t = Model.Turtle(data[i,0], data[i,1], data[i,2], data[i,3], data[i,4], data[i,5], data[i,6], data[i,7], data[i,8], data[i,9])
        Turtles.append(t)

    order_in = []
    time_in = []
    time_out = []

    for i in range(number_of_trains-1,-1,-1):
        order_in.append(Turtles[i].id)
        time_in.append(Turtles[i].in_time)
        time_out.append(Turtles[i].out_time)

    order_out = list(zip(order_in, time_out))
    order_out.sort(key=lambda x: x[1], reverse=True)
    order_in = list(zip(order_in, time_in))
    order_in.sort(key= lambda x: x[1], reverse=True)

    index_in = number_of_trains -1
    index_out = number_of_trains -1

    while (index_in >= 0) or (index_out >=0):
        if index_in >= 0:
            if order_in[index_in][1] < order_out[index_out][1]:
                Turtles[index_in].reinlaufen(sim)
                index_in -= 1
            else:
                Turtles[order_out[index_out][0]].rauslaufen(sim)
                index_out -= 1
        else:
            Turtles[order_out[index_out][0]].rauslaufen(sim)
            index_out -=1
    sim.Animation()




Pfad = Path("C:/Users/dek/Documents/Turtle/TabellenSauber/Tabelle_19.csv")

run(Pfad)

 #Kuppelungen hinzufügen (trip UND in/out time sind gleich)
 #Log am Ende (wie viele Züge, wie viele Fehler etc)