import os

vect = ["1e-2","1e-8"]

for el in vect:
    os.system("python .\project\Main.py -i datasets\\AstroPh\\AstroPh.txt  -d AstroPh -a 0.9 -e "+el+ " -o output.txt") 




    

