import random
import math
import numpy
import trilateration
from csv import DictReader, DictWriter, writer
from itertools import combinations

earthR = 6371
a = 35
n = 2
coeffLat = 1.1103*10**-5
coeffLon = 0.8539*10**-5

fW = open("data/datasJS2.csv")
datas = list(DictReader(fW))

locs = open("locs.csv", "w")
colonnes = ["pool1", "pool2", "pool3", "pool4"]
writer = DictWriter(locs, fieldnames=colonnes)
writer.writeheader()
def rssiToDistance(rssi):
    return 10**(-(rssi+a)/(10*n))

def trackIoTWearable(x1,y1,r1,x2,y2,r2,x3,y3,r3):
    A = 2*x2 -2*x1
    B = 2*y2 -2*y1
    C= r1**2 -r2**2 -x1**2 + x2**2 -y1**2 + y2**2
    D = 2*x3 -2*x2
    E = 2*y3 -2*y2
    F = r2**2 -r3**2 -x2**2 + x3**2 -y2**2 + y3**2
    x = (C*E - F*B) / (E*A - B*D)
    y = (C*D - A*F) / (B*D - A*E)
    return y*coeffLat, x*coeffLon

gw1 = {"lat":41.9973938, "lon":8.8269047, "id":"colline", "idRSSI":"rssiGW1"}
gw2 = {"lat":41.997522, "lon":8.827901, "id":"fraises", "idRSSI":"rssiGW2"}
gw3 = {"lat":41.9977982, "lon":8.8280001, "id":"vasque", "idRSSI":"rssiGW3"}
gw4 = {"lat":41.996695, "lon":8.827148, "id":"oliviers","idRSSI":"rssiGW4"}

gws= (gw1, gw2, gw3, gw4)
sites = [*combinations(gws,3)]
# LonA = 9.153123 #4-04
# LatA = 42.299159
# LonB = 9.153545 #4-02
# LatB = 42.299270
# LonC = 9.153372 #4-10
# LatC = 42.299083
 
lesLocs = [[],[],[],[]]
cpt = 0
for combi in sites:
    LonA = combi[0]["lon"]/coeffLon
    LatA = combi[0]["lat"]/coeffLat
    LonB = combi[1]["lon"]/coeffLon
    LatB = combi[1]["lat"]/coeffLat
    LonC = combi[2]["lon"]/coeffLon
    LatC = combi[2]["lat"]/coeffLat
    print("#######################")
    # print(combi[0]["id"], combi[1]["id"], combi[2]["id"])
    # print(list(combi))
    for data in datas:
        DistA = rssiToDistance(int(data[combi[0]["idRSSI"]]))/1000
        DistB = rssiToDistance(int(data[combi[1]["idRSSI"]]))/1000
        DistC = rssiToDistance(int(data[combi[2]["idRSSI"]]))/1000
        print(combi[0]["id"], DistA, combi[1]["id"], DistB, combi[2]["id"], DistC)
        lesLocs[cpt].append(trackIoTWearable(LonA, LatA, DistA, LonB, LatB, DistB, LonC, LatC, DistC))
        print(trackIoTWearable(LonA, LatA, DistA, LonB, LatB, DistB, LonC, LatC, DistC))
        #using authalic sphere
        #if using an ellipsoid this step is slightly different
        #Convert geodetic Lat/Long to ECEF xyz
        #   1. Convert Lat/Long to radians
        #   2. Convert Lat/Long(radians) to ECEF
        xA = earthR *(math.cos(math.radians(LatA)) * math.cos(math.radians(LonA)))
        yA = earthR *(math.cos(math.radians(LatA)) * math.sin(math.radians(LonA)))
        zA = earthR *(math.sin(math.radians(LatA)))

        xB = earthR *(math.cos(math.radians(LatB)) * math.cos(math.radians(LonB)))
        yB = earthR *(math.cos(math.radians(LatB)) * math.sin(math.radians(LonB)))
        zB = earthR *(math.sin(math.radians(LatB)))

        xC = earthR *(math.cos(math.radians(LatC)) * math.cos(math.radians(LonC)))
        yC = earthR *(math.cos(math.radians(LatC)) * math.sin(math.radians(LonC)))
        zC = earthR *(math.sin(math.radians(LatC)))

        P1 = numpy.array([xA, yA, zA])
        P2 = numpy.array([xB, yB, zB])
        P3 = numpy.array([xC, yC, zC])

        #from wikipedia
        #transform to get circle 1 at origin
        #transform to get circle 2 on x axis
        ex = (P2 - P1)/(numpy.linalg.norm(P2 - P1))
        i = numpy.dot(ex, P3 - P1)
        ey = (P3 - P1 - i*ex)/(numpy.linalg.norm(P3 - P1 - i*ex))
        ez = numpy.cross(ex,ey)
        d = numpy.linalg.norm(P2 - P1)
        j = numpy.dot(ey, P3 - P1)

        #from wikipedia
        #plug and chug using above values
        x = (pow(DistA,2) - pow(DistB,2) + pow(d,2))/(2*d)
        y = ((pow(DistA,2) - pow(DistC,2) + pow(i,2) + pow(j,2))/(2*j)) - ((i/j)*x)

        # only one case shown here
        print(pow(DistA,2) - pow(x,2) - pow(y,2))
        try:
            z = numpy.sqrt(pow(DistA,2) - pow(x,2) - pow(y,2))
        except:
            pass
        # triPt is an array with ECEF x,y,z of trilateration point
        triPt = P1 + x*ex + y*ey + z*ez

        #convert back to lat/long from ECEF
        #convert to degrees
        lat = math.degrees(math.asin(triPt[2] / earthR))
        lon = math.degrees(math.atan2(triPt[1],triPt[0]))

        if(not math.isnan(lat) or not math.isnan(lon)):
            print("lat",lat,", lon ",lon)
            # lesDonnees.append([lat, lon])
    cpt+=1
    print("#####################")
for i in range(len(lesLocs[0])):
    writer.writerow({"pool1":lesLocs[0][i],"pool2":lesLocs[1][i],"pool3":lesLocs[2][i],"pool4":lesLocs[3][i]})