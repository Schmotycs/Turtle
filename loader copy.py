from pathlib import Path
import pandas as pd
import numpy as np
from collections import deque



Test = deque()

Test.append(2)
Test.append(1)
Test.append(0)
Test.append(3)
Test.append(4)

print(Test)
Fahrzeugerechtsvon0 = len(Test)-Test.index(0)
print(f"Fahrzegerechts = {Fahrzeugerechtsvon0}")

for i in range(Fahrzeugerechtsvon0-1):
    nachbar = Test.index(0)+i+1
    print(Test[nachbar])
