import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.lines import Line2D
from matplotlib.text import Annotation
import math
import csv
import collections

Route = collections.namedtuple('Route','x,y,s,dx,dy,yaw')

class Map:
    def __init__(self,axes=None):
        self.route = Route
        self.route.x=[]
        self.route.y=[]
        self.route.s=[]
        self.route.dx=[]
        self.route.dy=[]
        self.route.yaw=[]
        # A map is a collection of lines
        self.map = [Line2D([], [], 1, color='black')]
        if axes:
            axes.add_line(self.map[0])

    def read(self,file,is_loop=True):
        with open(file) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            self.route.x[:]=[]
            self.route.y[:]=[]
            self.route.s[:]=[]
            self.route.dx[:]=[]
            self.route.dy[:]=[]
            self.route.yaw[:]=[]
            for row in reader:
                self.route.x.append(float(row['x']))
                self.route.y.append(float(row['y']))
                self.route.s.append(float(row['s']))
                self.route.dx.append(float(row['dx']))
                self.route.dy.append(float(row['dy']))
            if is_loop:
                self.route.x.append(self.route.x[0])
                self.route.y.append(self.route.y[0])
            for i in range(0, len(self.route.s) - 1):
                self.route.yaw.append(math.atan2(self.route.y[i + 1] - self.route.y[i],
                                                 self.route.x[i + 1] - self.route.x[i]))
            self.route.yaw.append(self.route.yaw[-1])
            # for dx,dy in zip(self.route.dx,self.route.dy):
            #     self.route.yaw.append(math.atan2(dy,dx) +math.pi/2)
    
    def draw(self):
        self.map[0].set_data(self.route.x,self.route.y)
        return self.map

def main():
    print("Test Map class")
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111, aspect='equal')

    map1 = Map(ax1)
    map1.read("highway_map.csv")
    print(map1.route.x)
    print(map1.route.y)
    map1.draw()

    for i in range(0,len(map1.route.s)):
        angle = math.atan2(map1.route.dy[i],map1.route.dx[i]) + math.pi/2
        # dir_x = math.cos(angle)*15
        # dir_y = math.sin(angle)*15        
        dir_x = map1.route.dx[i]*15
        dir_y = map1.route.dy[i]*15
        ax1.arrow(map1.route.x[i],map1.route.y[i],dir_x,dir_y,linewidth=2,color='r')

    ax1.relim()
    ax1.autoscale_view()
    ax1.grid(True)
    plt.show()


if __name__ == "__main__":
    main()
