from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt


def k_means(csv_path,k, attr1, attr2):
    Daten = np.genfromtxt(csv_path, delimiter=";", dtype=float, skip_header=1)
    X = Daten[:, 1:]
    kmeans = KMeans(n_clusters= k, init="k-means++", max_iter=300, n_init=10, random_state=23)
    y_kmeans = kmeans.fit_predict(X)
    
    Eigenschaften = ["Anzahl Züge", "TimeOrder", "Deadlock", "Postion", "Bahnhofslänge", "Summe", "Anzahl Verbünde in", "Anzahl Verbünde out", "Länge Verbünde in", "Länge Verbünde out"]
    df = pd.DataFrame(X, columns=Eigenschaften)
    df["cluster"] = y_kmeans

    stats = df.groupby("cluster").agg(["mean", "std", "min", "max"])
    centers = kmeans.cluster_centers_
    sil = silhouette_score(X, y_kmeans)
    Schnitt_pro_Spalte = df.groupby("cluster").mean(numeric_only=True).T
    count = df["cluster"].value_counts().sort_index()
    Schnitt_pro_Spalte.loc["count"] = count

    print(f"Silhouttenscore: {sil}")
    print(f"schnitt{Schnitt_pro_Spalte}")

    plt.scatter(X[:, attr1], X[:, attr2], c = y_kmeans, cmap="viridis", s=10)
    plt.xlabel(f"Feature {attr1}")
    plt.ylabel(f"Feature {attr2}")
    plt.title("KMeans-Cluster in 2D")
    plt.colorbar(label="Cluster")
    plt.show()
    

    

Pfad = Path(r"C:\Users\dek\Documents\Turtle\genormte_werte.csv")

k_means(Pfad,3, 0, 5) #0 und 5 sind Anzahl züge und Summe der Kosten

