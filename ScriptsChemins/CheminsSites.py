import random
import itertools
import FonctionsSmartPaesi as fsp

banLatLon = [(random.uniform(42, 42.5), random.uniform(8.7, 9.2)) for i in range(10)]
sites = [[41.9352222, 9.155194444444446],
        [41.9343889,9.152666666666667],
        [41.9398056,9.153194444444445],
        [41.9319167,9.149027777777777],
        [41.9335833,9.182666666666666],
        [41.9403056,9.149416666666665],
        [41.9325833,9.15538888888889]]
#cheminsExc, cheminsClean, chemins = fsp.crossBoundaries(sites, banLatLon)

fsp.writeTest(sites)
#print(cheminsExc[0], chemins[0])
