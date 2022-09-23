import os

vect = ["1e-2","1e-8"]

for el in vect:
    os.system("python .\project\Main.py -i datasets\\HepPh\\ca-HepPh.mtx  -d HepPh -a 0.9 -e "+el+ " -o output.txt") 

