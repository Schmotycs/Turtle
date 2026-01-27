from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import os


def k_means(csv_path, k, x_achse, y_achse):
    Daten = np.genfromtxt(csv_path, delimiter=";", dtype=float, skip_header=1)
    X = Daten[:,1:5]
    kmeans = KMeans(n_clusters= k, init="k-means++", max_iter=300, n_init=10, random_state=23)
    y_kmeans = kmeans.fit_predict(X)
    
    Eigenschaften = ["TimeOrder", "Deadlock", "Postion" ,"Bahnhofslänge"]
    df = pd.DataFrame(X, columns=Eigenschaften)
    df["cluster"] = y_kmeans

    stats = df.groupby("cluster").agg(["mean", "std", "min", "max"])
    sil = silhouette_score(X, y_kmeans)
    Schnitt_pro_Spalte = df.groupby("cluster").mean(numeric_only=True).T
    count = df["cluster"].value_counts().sort_index()
    Schnitt_pro_Spalte.loc["count"] = count

    print(f"Silhouttenscore von k = {k}: {sil}")
    #print(f"Stats = {stats}")
    #print(f"{Schnitt_pro_Spalte}")
    
    Diagramm_2(X, y_kmeans, x_achse, y_achse, k)

    
def Diagramm_2(X, y_kmeans, x_achse, y_achse, k):
    Pfad = Path(r"C:\Users\dek\Documents\Diagramme\k_3")

    clusters = np.unique(y_kmeans)
    for c in clusters:
        mask = y_kmeans == c
        plt.scatter(X[mask, x_achse], X[mask,y_achse], s=10, alpha = 0.1, label = f"Cluster {c}")
    plt.xlabel(f"{x_achse}")
    plt.ylabel(f"{y_achse}")
    plt.title(f"K = {k}")
    plt.legend()
    plt.savefig(os.path.join(Pfad, f"K{k}_X{x_achse}_Y{y_achse}"))
    plt.show()

    

Pfad = Path(r"C:\Users\dek\Documents\Turtle\genormte_werte.csv")

#0: WrongTimeOrder
#1: Deadlock
#2: Position
#3: Bahnhofslänge

for i in range(4):
    j = 0
    while j<i:
        k_means(Pfad, 3, i, j)
        j += 1