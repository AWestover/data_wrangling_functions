# Alek Westover
# Parse out all checkboxes

import pandas as pd
from bs4 import BeautifulSoup
from pdb import set_trace as tr

# this has all the xml data for the word document that is usefull (for us, other files are mostly useless)
with open("data/word/document.xml") as fp:
    soup = BeautifulSoup(fp, "xml")

# read all check boxes (not just binary input every box)
realTs = []
for t in soup.find_all("checkbox"):
  cur = t.checked.attrs
  cur = list(cur.values())[0]
  realTs.append(int(cur))

# put data in csv
# print(realTs)
df = pd.DataFrame.from_dict({"binary_stuff":realTs})
df.to_csv("output/init.csv", index=False)

