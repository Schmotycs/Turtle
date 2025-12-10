from pathlib import Path
import loader
import Model



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
    out_groups = {}
    for i in Turtles:
        out_trip_time = (i.out_trip, i.out_time)

        if out_trip_time not in out_groups:
            out_groups[out_trip_time] = []
        out_groups[out_trip_time].append(i.id)

    order_out = []

    for (_, out_time), ids in out_groups.items():
        id_out_pos = []
        for id in ids:
            id_out_pos.append((id, Turtles[id].in_pos))

        id_out_pos.sort(key = lambda x: x[1])
        id_out_sort = [x[0] for x in id_out_pos]
        ids_out_tupel = tuple(id_out_sort)
        order_out.append((ids_out_tupel, out_time))

    order_out.sort(key=lambda x: x[1], reverse=True)

    #Fahrzeuge die zusammen reifahren werden in eine Gruppe gesteckt
    order_in = list(zip(order_in, time_in))

    in_groups = {}
    
    for i in Turtles:
        in_trip_time = (i.in_trip, i.in_time)

        if in_trip_time not in in_groups:
            in_groups[in_trip_time] = []

        in_groups[in_trip_time].append(i.id)

    order_in = []

    for (_, in_time), ids in in_groups.items():
        id_in_pos = []
        for id in ids:
            id_in_pos.append((id, Turtles[id].in_pos))

        id_in_pos.sort(key = lambda x: x[1])     #sortieren nach in_pos
        id_in_sort = [x[0] for x in id_in_pos]

        ids_in_tupel = tuple(id_in_sort)
        order_in.append((ids_in_tupel, in_time))

    
    order_in.sort(key= lambda x: x[1], reverse=True)



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
                if len(order_out[index_out][0]) == 1:
                    Turtles[order_out[index_out][0][0]].rauslaufen(sim)
                else:
                    verbund = []
                    for i in range(len(order_out[index_out][0])):
                        verbund.append(Turtles[order_out[index_out][0][i]])
                    verbund_turtles = Model.Verbund(verbund)
                    verbund_turtles.rauslassen(sim)
                index_out -= 1
        else:
            if len(order_out[index_out][0]) == 1:
                    Turtles[order_out[index_out][0][0]].rauslaufen(sim)

            else:
                verbund = []
                for i in range(len(order_out[index_out][0])):
                    verbund.append(Turtles[order_out[index_out][0][i]])
                verbund_turtles = Model.Verbund(verbund)
                verbund_turtles.rauslassen(sim)

            index_out -=1


    sim.Animation()
    print(tor.Straf_Kosten)





Pfad = Path("C:/Users/dek/Documents/Turtle/TestTrackSauber/track1_2.csv")

run(Pfad)