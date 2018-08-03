import pandas as pd
import sys

# python3 concat.py test/a.csv test/b.csv test/c.csv

fs = [sys.argv[1], sys.argv[2]]
fout = sys.argv[3]
dfs = [pd.read_csv(fi, header=None) for fi in fs]
dicts = [f.to_dict() for f in dfs]
keys = list(dicts[0][0].values())+list(dicts[1][0].values())
vals = list(dicts[0][1].values())+list(dicts[1][1].values())
df = pd.DataFrame.from_dict({"Keys":keys, "Vals":vals})
df.to_csv(fout, header=False, index=False)
