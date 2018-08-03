
import os
from os.path import join

for fi in os.listdir("input"):
	print(fi)
	os.system("python3 single.py {} {}".format(join("input", fi), join("output", fi.replace(".txt", ".csv"))))
