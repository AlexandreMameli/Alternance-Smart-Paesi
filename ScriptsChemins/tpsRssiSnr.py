import csv

with open("Map Sites/data/donneesPycomTxRx/0.csv") as fCsv:
    data = csv.reader(fCsv)
    
    timestamp, rssi, snr = [], [], []
    for row in data:
        timestamp, rssi, snr = row
    print(rssi)