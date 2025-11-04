from pathlib import Path
import pandas as pd
import numpy as np


def load_csv(csv_path: Path):
    Daten = np.genfromtxt(csv_path, delimiter=";", dtype=int, skip_header=1)
    return Daten
    
