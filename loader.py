from pathlib import Path
import pandas as pd
import numpy as np


def load_csv(csv_path):
    data = np.genfromtxt(csv_path, delimiter=";", dtype=int, skip_header=1)

    # Falls nur 1 Zeile, wird kein 2d angegeben sondern nur ein 1d array deswegen->
    if data.ndim == 1:
        data = data.reshape(1, -1)

    return data

    

