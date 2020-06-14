import math


lng, lat = 41.935311, 9.153702
dist = 100
decLon = 0.00001 / 1.11072
decLat = 0.00001/1.11319
rad = 30 / 360 * 2 * math.pi

for i in range(12):
	print([lng + (dist * decLon) * math.sin(i * rad),lat + (dist * decLat) * math.cos(i * rad)])
