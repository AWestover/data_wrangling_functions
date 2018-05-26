# Alek Westover
# Parse out non checkbox fields
# Uses the files cols.txt and regexs.txt to generate the files
import pandas as pd
from bs4 import BeautifulSoup
from pdb import set_trace as tr
import re

# get the soup
with open("data/word/document.xml") as fp:
    soup = BeautifulSoup(fp, "xml")

cols = []
with open("cols.txt") as f:
  for r in f:
    cols.append(r)

regexs = []
with open("regexs.txt") as f:
    for r in f:
      regexs.append(re.compile(r.strip()))

# manually hard code these in
print(cols)
print(regexs)

# get all text
realTs = []
for t in soup.find_all("w:t"):
  if t.text not in [" ", ":"]:
    realTs.append(t.text)
    print(t.text)
print(realTs)

allT = " ".join(realTs)
#t = soup.text
#print(t)

data = {}

# read text for the regexes
for i in range(0, len(cols)):
  print(cols[i])
  cc = re.findall(regexs[i], allT)
  data[cols[i]] = cc

with open("output/stuff.txt", "w") as f:
   f.write(allT)

# put it in a file
df = pd.DataFrame.from_dict(data)
df.to_csv("output/data.csv", index=False)


