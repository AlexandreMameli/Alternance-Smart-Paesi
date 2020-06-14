import random
from csv import DictReader, DictWriter
datas = []
f1 = open("data/datas5lat/dataColline.csv")
f2 = open("data/datas5lat/dataFraises.csv")
f3 = open("data/datas5lat/dataMarais.csv")
f4 = open("data/datas5lat/dataOliviers.csv")
txt1 = DictReader(f1)
txt2 = DictReader(f2)
txt3 = DictReader(f3)
txt4 = DictReader(f4)

fW = open("data/datasJS2.csv", "w")

coeffLat = 1.1103*10**-5
coeffLon = 0.8539*10**-5


x1 = 9.153123/coeffLon #4-04
y1 = 42.299159/coeffLat
x2 = 9.153545/coeffLon #4-02
y2 = 42.299270/coeffLat
x3 = 9.153372/coeffLon #4-10
y3 = 42.299083/coeffLat


a = 50
n = 2.1

def trackIoTWearable(x1,y1,r1,x2,y2,r2,x3,y3,r3):
	A = 2*x2 -2*x1
	B = 2*y2 -2*y1
	C= r1**2 -r2**2 -x1**2 + x2**2 -y1**2 + y2**2
	D = 2*x3 -2*x2
	E = 2*y3 -2*y2
	F = r2**2 -r3**2 -x2**2 + x3**2 -y2**2 + y3**2
	x = (C*E - F*B) / (E*A - B*D)
	y = (C*D - A*F) / (B*D - A*E)
	return x,y

def rssiToDistance(rssi):
    return 10**(-(rssi+a)/(10*n))

csv_columns = ['idGW1', "rssiGW1", "idGW2", "rssiGW2", 'idGW3', "rssiGW3", "idGW4", "rssiGW4"]
for data1, data2, data3, data4 in zip(txt1, txt2, txt3, txt4):
	if data1["id"] == data2["id"] and data2["id"]==data3["id"] and data3["id"] == data4["id"]:
		datas.append({"idGW1":data1["id"], "rssiGW1":int(data1["rssi"]), "idGW2":data2["id"], "rssiGW2":int(data2["rssi"]), "idGW3":data3["id"], "rssiGW3":int(data3["rssi"]), "idGW4":data4["id"], "rssiGW4":int(data4["rssi"])})

writer = DictWriter(fW, fieldnames=csv_columns)
writer.writeheader()

lesdonnees = []
for data in datas:
	# d1 = rssiToDistance(int(data["rssi04"]))
	# d2 = rssiToDistance(data["rssi02"])
	# d3 = rssiToDistance(data["rssi10"])
	# print(d1, d2, d3)
	# x,y = trackIoTWearable(x1, y1, d1, x2, y2, d2, x3, y3, d3)
	# lesdonnees.append([y*coeffLat, x*coeffLon])
	writer.writerow(data)
	# print(y*coeffLat,",",x*coeffLon)

print(lesdonnees)