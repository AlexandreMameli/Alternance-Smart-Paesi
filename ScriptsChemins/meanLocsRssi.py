from os import listdir
from os.path import isfile, join

mypath = "D:/Users/Alexm/Documents/SmartPaesi/Map Sites/data/donneesPycomTxRx"

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

# for f in onlyfiles:
#     fichier = open(join(mypath, f), "r")
#     print(f)
#     lignes = fichier.read().split("\n")
#     lignes = tuple(l[1:-1] for l in lignes )
#     print(lignes)

fichier = open(join(mypath, onlyfiles[0]))
lignes = fichier.read().split("\n")
valeurs = []
# lignes = [l for l in lignes]
for l in lignes:
    valeurs.append(l[1:-1].split(", "))

tpsTab, rssiTab, snrTab, sfrxTab = [],[],[],[]
for v in valeurs[:-1]:
    print(v)
    tpsTab.append(v[0])
    rssiTab.append(int(v[1][5:]))
    snrTab.append(v[2])
    sfrxTab.append(v[3])




print(int(sum(rssiTab)/len(rssiTab)))
# print("*******************************************************\r\n***************************************************\r\n"+str(lignes)
# +"\r\n*******************************************************\r\n***************************************************")