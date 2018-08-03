import pandas as pd
import os
from os.path import join

from pdb import set_trace as tr

datas = []
fNames = []
folder="trashcan"
for fi in os.listdir(folder):
    if ".csv" in fi:
        datas.append(pd.read_csv(join(folder, fi), header=None))
        fNames.append(fi)

newData = {"fileName": list(datas[0][0])}
for d in range(len(datas)):
    newData[fNames[d]] = datas[d][1]

df = pd.DataFrame.from_dict(newData)

df.T.to_csv("master.csv", header=None)
