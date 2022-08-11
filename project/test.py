import os

vect = ["1e-1","1e-2","1e-4","1e-6","1e-8","1e-10"]

for el in vect:
    os.system("python Main.py -i ..\datasets\\facebook\\0.edges  -d facebook -a 0.9 -e "+el) 

