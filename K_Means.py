from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt


def k_means(csv_path, k):
    Daten = np.genfromtxt(csv_path, delimiter=";", dtype=float, skip_header=1)
    X = Daten[:,1:10]
    Summen = Daten[:,10]
    kmeans = KMeans(n_clusters= k, init="k-means++", max_iter=300, n_init=10, random_state=23)
    y_kmeans = kmeans.fit_predict(X)
    
    Eigenschaften = ["Anzahl Züge", "TimeOrder", "Deadlock", "Postion" ,"Bahnhofslänge", "Anzahl Verbünde in", "Anzahl Verbünde out", "Länge Verbünde in", "Länge Verbünde out"]#, "SUmme"]
    df = pd.DataFrame(X, columns=Eigenschaften)
    df["cluster"] = y_kmeans

    stats = df.groupby("cluster").agg(["mean", "std", "min", "max"])
    centers = kmeans.cluster_centers_
    sil = silhouette_score(X, y_kmeans)
    Schnitt_pro_Spalte = df.groupby("cluster").mean(numeric_only=True).T
    count = df["cluster"].value_counts().sort_index()
    Schnitt_pro_Spalte.loc["count"] = count

    print(f"Silhouttenscore von k = {k}: {sil}")
    #print(f"{Schnitt_pro_Spalte}")
    #Diagramm_2(X, y_kmeans, Summen)

    
def Diagramm_2(X, y_kmeans, Summen):

    clusters = np.unique(y_kmeans)
    for c in clusters:
        mask = y_kmeans == c
        plt.scatter(X[mask, 0], X[mask, 1], s=10, alpha = 0.1, label = f"Cluster {c}")
    plt.xlabel(f"Anzahl Züge")
    plt.ylabel(f"Timeorder Konflikte")
    plt.title("KMeans-Cluster in 2D")
    plt.legend()
    plt.show()

    

Pfad = Path(r"C:\Users\dek\Documents\Turtle\genormte_werte.csv")
for i in range(10):
    k_means(Pfad,i+2)