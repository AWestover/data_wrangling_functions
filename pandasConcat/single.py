
import os
from os.path import join
import sys

if not os.path.exists("temp"):
	os.mkdir("temp")

fileIn = sys.argv[1]
fileOut = sys.argv[2]

data = ""
with open(fileIn, "r") as f:
	data = f.read()

with open(fileOut, "w") as f:
	f.write(data)

os.rmdir("temp")
