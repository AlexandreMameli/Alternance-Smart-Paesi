import itertools
import math


def crossBoundaries(sitesObs, zoneBan): #Verifie si les chemins que peut emprunter le drone croisent la zone interdite
    paths = []
    for comb in itertools.combinations(sitesObs, 2):
        paths.append(tuple([*comb]))
    pathClean = []
    pathExclu = []

    for pathPoss in paths:
        for i in range(len(pathPoss))[:-1]:
            cote1 = (pathPoss[i][1] - pathPoss[i+1][1])/(pathPoss[i][0]-pathPoss[i+1][0])
            ordO1 = pathPoss[i][1] - (cote1*pathPoss[i][0])
            xcom = 0
            for j in range(len(zoneBan))[:-1]:
                cote2 = (zoneBan[i][1] - zoneBan[i+1][1])/(zoneBan[i][0]-zoneBan[i+1][0])
                ordO2 = zoneBan[i][1] - (cote2*zoneBan[i][0])
                if cote1 - cote2 != 0:
                    xcom = (ordO2-ordO1)/(cote1-cote2)
                    if (pathPoss[i][0]<=xcom<=pathPoss[i+1][0]) and (zoneBan[j][0]<=xcom<=zoneBan[j+1][0]): #verifie si les segments se croisent
                        pathExclu.append((pathPoss[i], pathPoss[i+1]))

    for p in paths:
        if p not in pathExclu:
            pathClean.append(p)
    pathClean = list(set(pathClean))
    return list(set(pathExclu)), pathClean, list(set(paths))

"""def writeLatLonClean(locArray): #Ecrit dans un fichier les coordonees pour les reutiliser dans ElectronMap
    fWeb = open("./ElectronMap/coordClean.txt", 'w+')
    for coordArray in locArray:
        for coord in coordArray:
            txt = [*coord]
            fWeb.write(str(txt[0])+","+str(txt[1]) + "\r\n")
    fWeb.close()"""

def writeTest(locArray):
    paths = []
    for comb in itertools.combinations(locArray, 2):
        paths.append(tuple([*comb]))
    fWeb = open('./ElectronMap/coordClean.txt', 'w+')
    for coord in paths:
        fWeb.write(str(coord[0][0])+','+str(coord[0][1])+','+str(coord[1][0])+','+str(coord[1][1])+'\r\n')
    fWeb.close()

def writePolyBan(banArray):
    fBan = open("./ElectronMap/coordBan.txt", 'w+')
    for coord in banArray:
        fBan.write(str(coord[0])+","+str(coord[1])+"\r\n")
    fBan.close()

def sortTrig(locsFence): #tri des points de la barriere dans le sens horaire/antiH
    ori = midSegment(*bottLUppR(locsFence))
    sortedLocs = {}
    retLocs = []
    print(ori)
    for point in locsFence:
        if point[0]>ori[0] and point[1]>ori[1]:
            angle = math.acos((point[0]-ori[0])/(math.sqrt((point[0]-ori[0])**2+(point[1]-ori[1])**2)))
            sortedLocs[angle] = point
        if point[0]<ori[0] and point[1]>ori[1]:
            angle = math.pi - math.acos(abs(point[0]-ori[0])/(math.sqrt((point[0]-ori[0])**2+(point[1]-ori[1])**2)))
            sortedLocs[angle] = point
        if point[0]<ori[0] and point[1]<ori[1]:
            angle = math.acos(abs(point[0]-ori[0])/abs(math.sqrt((point[0]-ori[0])**2+(point[1]-ori[1])**2))) - math.pi
            sortedLocs[angle] = point
        if point[0]>ori[0] and point[1]<ori[1]:
            angle = - math.acos(abs(point[0]-ori[0])/abs(math.sqrt((point[0]-ori[0])**2+(point[1]-ori[1])**2)))
            sortedLocs[angle] = point
    for key in sorted(sortedLocs):
        retLocs.append(sortedLocs[key])
    return retLocs


def bottLUppR(fenceArray): #determine le point le plus en bas a gauche et le point le plus en bas a droite
    minLatLon = ""
    maxLatLon = ""
    minLoc = 100000
    maxLoc = -100000
    for locs in fenceArray:
        if locs[0]+locs[1]<minLoc:
            minLoc = locs[0]+locs[1]
            minLatLon = (locs[0], locs[1])
        if locs[0]+locs[1]>maxLoc:
            maxLoc = locs[0]+locs[1]
            maxLatLon = (locs[0], locs[1])
    return minLatLon, maxLatLon

def midSegment(p1, p2):
    return (p1[0]+p2[0])/2, (p1[1]+p2[1])/2


