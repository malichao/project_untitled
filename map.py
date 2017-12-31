import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.lines import Line2D
from matplotlib.text import Annotation
import math
import csv

class Map:
    def __init__(self,axes=None):
        self.x=[]
        self.y=[]
        # A map is a collection of lines
        self.map = [Line2D([], [], 1, color='black')]
        if axes:
            axes.add_line(self.map[0])

    def read(self,file,is_loop=True):
        with open(file) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            self.x[:]=[]
            self.y[:]=[]
            for row in reader:
                self.x.append(float(row['x']))
                self.y.append(float(row['y']))
            if is_loop:
                self.x.append(self.x[0])
                self.y.append(self.y[0])
    
    def draw(self):
        self.map[0].set_data(self.x,self.y)
        return self.map

def main():
    print("Test Map class")
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111, aspect='equal')

    map1 = Map(ax1)
    map1.read("lake_track_waypoints.csv")
    print(map1.x)
    print(map1.y)
    map1.draw()


    ax1.set_xlim(-200, 200)
    ax1.set_ylim(-200, 200)
    ax1.grid(True)
    plt.show()


if __name__ == "__main__":
    main()