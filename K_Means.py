from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import os
from collections import Counter


def k_means(csv_path, k, Varianzen = 4*[1], Mittelwerte = 4*[0], x_achse = 0, y_achse = 0, Diagramm=False, sil=False):
    Daten = np.genfromtxt(csv_path, delimiter=";", dtype=float, skip_header=1)
    X = Daten[:,2:6]
    kmeans = KMeans(n_clusters= k, init="k-means++", max_iter=300, n_init=10, random_state=23)
    y_kmeans = kmeans.fit_predict(X)
    sse = kmeans.inertia_
    
    Eigenschaften = ["TimeOrder", "Deadlock", "Postion" ,"Bahnhofslänge"]
    df = pd.DataFrame(X, columns=Eigenschaften)
    df["cluster"] = y_kmeans

    sil = silhouette_score(X, y_kmeans)

    Schnitt_pro_Spalte = df.groupby("cluster").mean(numeric_only=True).T
    for i, spalte in enumerate(Eigenschaften):
        if spalte in Schnitt_pro_Spalte.index:
            Schnitt_pro_Spalte.loc[spalte] *= Varianzen[i]
            Schnitt_pro_Spalte.loc[spalte] += Mittelwerte[i]
  
    count = df["cluster"].value_counts().sort_index()
    Schnitt_pro_Spalte.loc["count"] = count
    Schnitt_pro_Spalte = Schnitt_pro_Spalte.round(4)


    #print(f"Stats = {stats}")

    if sil == True:
        print(f"Silhouttenscore von k = {k}: {sil}")
        print(f"Absolute werte Werte \n {Schnitt_pro_Spalte}")

    if Diagramm == True:
        Diagramm_2(X, y_kmeans, x_achse, y_achse, k)

    return sil, sse

    
def Diagramm_2(X, y_kmeans, x_achse, y_achse, k):
    clusters = np.unique(y_kmeans)
    for c in clusters:
        mask = y_kmeans == c
        X_cluster = X[mask]

        punkte_cluster = [(X_cluster[i, x_achse], X_cluster[i, y_achse]) for i in range(len(X_cluster))]
        haeufigkeit = Counter(punkte_cluster)

        groessen = np.clip([haeufigkeit[(X_cluster[i, x_achse], X_cluster[i, y_achse])] * 10 for i in range(len(X_cluster))], 5, 200)


        plt.scatter(X_cluster[:, x_achse], X_cluster[:, y_achse],s=groessen, label=f"Cluster {c}",c=f'C{c}')
    plt.xlabel(f"{x_achse}")
    plt.ylabel(f"{y_achse}")
    plt.title(f"K = {k}")
    plt.legend()
    plt.show()




    

Pfad = Path(r"C:\Users\dek\Documents\Turtle\genormte_werte_track454.csv")

#0: WrongTimeOrder
#1: Deadlock
#2: Position
#3: Bahnhofslänge