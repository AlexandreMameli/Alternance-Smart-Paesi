import numpy
import json
from geopy.distance import distance
import numpy
import math
import matplotlib.pyplot as plt

from scipy.optimize import curve_fit

dist = []
rssi = []




json_file = open("village.json")
datas = json.load(json_file)
for hit in datas["hits"]["hits"]:
    d = distance([hit["_source"]["location"][1], hit["_source"]["location"][0]], [41.935374, 9.153700]).m
    dist.append(d)
    rssi.append(hit["_source"]["rssi"])
    # distRssi.append(temp)
# print(distRssi)

a = 45
def func(x, n):
    return -(10*numpy.log10(x)*n+a)

yn = rssi + 0.2*numpy.random.normal(size=len(dist))
popt, pcov = curve_fit(func, dist, yn)
print(popt)
n=popt[0]
plt.figure()
plt.plot(dist, yn, 'ko', label="Original Noised Data")
plt.plot(dist, func(dist, *popt), 'r-', label="Fitted Curve")
plt.legend()
# plt.show()

print(n)
moyenneDist = []
diffRssi = []
for hit in datas["hits"]["hits"]:
    d = distance([hit["_source"]["location"][1], hit["_source"]["location"][0]], [41.935374, 9.153700]).m
    est = -(10*n* math.log10(d)+a)

    print("rssi mesure :",hit["_source"]["rssi"], "rssi estime ",est)
    print("dist mesuree : ", d, "dist estimee : ", 10**(-(hit["_source"]["rssi"]+a)/(10*n)), "diff : ", abs(d-10**(-(hit["_source"]["rssi"]+a)/(10*n))))
    diffRssi.append(abs(hit["_source"]["rssi"]-est))
    moyenneDist.append(abs(d-10**(-(hit["_source"]["rssi"]+a)/(10*n))))
print("ecart dist", sum(moyenneDist)/len(moyenneDist))
print("ecart rssi", sum(diffRssi)/len(diffRssi))
# plt.plot(dist, rssi, "ro")
# plt.show()

