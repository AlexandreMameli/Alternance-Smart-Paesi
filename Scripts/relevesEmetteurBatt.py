import csv

from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import matplotlib.pyplot as plt


with open("./releveFrigo.txt") as f:
    data = csv.reader(f)
    y = []
    temp = []
    for row in data:
        y.append(row[0])
        temp.append(float(row[4]))
        print(row[0],row[4])

        
    host = host_subplot(111)

    par1 = host.twinx()

    host.set_xlabel("Temps (min)")
    host.set_ylabel("Tension (V)")
    par1.set_ylabel("Temperature (°C)")

    p1, = host.plot(range(len(y)), y, label="Tension (V)")
    p2, = par1.plot(range(len(y)), temp, label="Temperature (°C)")


    host.legend()

    host.axis["left"].label.set_color(p1.get_color())
    par1.axis["right"].label.set_color(p2.get_color())
    plt.gca().invert_yaxis()
    plt.plot()
    plt.show()