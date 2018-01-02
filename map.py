import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.lines import Line2D
from matplotlib.text import Annotation
import math
import csv
#import collections # namedtuple
import bisect


class Route:
    def __init__(self, lane_width=3.5, lane_num=3):
        self.x = []
        self.y = []
        self.s = []
        self.sx = []
        self.sy = []
        self.dx = []
        self.dy = []
        self.yaw = []
        self.lane_width = lane_width
        self.lane_num = lane_num
        if lane_num < 1:
            raise("Lane number must > 1")

    def read(self, file, is_loop=True):
        with open(file) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            self.x[:] = []
            self.y[:] = []
            self.s[:] = []
            self.sx[:] = []
            self.sy[:] = []
            self.dx[:] = []
            self.dy[:] = []
            self.yaw[:] = []
            for row in reader:
                self.x.append(float(row['x']))
                self.y.append(float(row['y']))
                self.s.append(float(row['s']))
                self.dx.append(float(row['dx']))
                self.dy.append(float(row['dy']))

            def calc(ax, ay, bx, by):
                yaw = math.atan2(by - ay, bx - ax)
                length = math.sqrt((bx - ax)**2 + (by - ay)**2)
                sx = (bx - ax) / length
                sy = (by - ay) / length
                return sx, sy, yaw

            for i in range(0, len(self.s) - 1):
                sx, sy, yaw = calc(
                    self.x[i], self.y[i], self.x[i + 1], self.y[i + 1])
                self.yaw.append(yaw)
                self.sx.append(sx)
                self.sy.append(sy)

            if is_loop:
                sx, sy, yaw = calc(
                    self.x[-1], self.y[-1], self.x[0], self.y[0])
            else:
                sx, sy, yaw = self.sx[-1], self.sy[-1], self.yaw[-1]
            self.yaw.append(yaw)
            self.sx.append(sx)
            self.sy.append(sy)

    def to_pose(self, s, d):
        idx = self.get_idx(s)
        ds = s - self.s[idx]
        x = self.x[idx] + self.dx[idx] * d + self.sx[idx] * ds
        y = self.y[idx] + self.dy[idx] * d + self.sy[idx] * ds
        yaw = self.yaw[idx]
        return x, y, yaw

    def to_center_pose(self, s, lane=0):
        d = self.lane_width * (lane + 0.5)
        return self.to_pose(s, d)

    def get_idx(self, s):
        return bisect.bisect(self.s, s) - 1

    def get_yaw(self, idx):
        return self.yaw[idx]

    def get_edge_xy(self, idx, lane_edge=0):
        return self.x[idx] + self.dx[idx] * self.lane_width * lane_edge, \
            self.y[idx] + self.dy[idx] * self.lane_width * lane_edge

    def get_center_xy(self, idx, lane=0):
        return self.x[idx] + self.dx[idx] * self.lane_width * (lane + 0.5), \
            self.y[idx] + self.dy[idx] * self.lane_width * (lane + 0.5)


class Map:
    def __init__(self, axes, lane_width=3.5, lane_num=3):
        self.route = Route(lane_width, lane_num)
        self.map = []
        for i in range(lane_num + 1):
            self.map.append(Line2D([], [], 1, linestyle='-.', color='black'))
            axes.add_line(self.map[i])
        self.map[0].set_linestyle('-')
        self.map[-1].set_linestyle('-')

    def read(self, file, is_loop=True):
        self.route.read(file, is_loop)

    def draw(self, is_loop=True):
        for lane_edge in range(self.route.lane_num + 1):
            route_x = []
            route_y = []
            for i in range(len(self.route.s)):
                x, y = self.route.get_edge_xy(i, lane_edge)
                route_x.append(x)
                route_y.append(y)

            if is_loop:
                route_x.append(route_x[0])
                route_y.append(route_y[0])
            self.map[lane_edge].set_data(route_x, route_y)
        return self.map


def main():
    print("Test Map class")
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111, aspect='equal')

    map1 = Map(ax1)
    map1.read("highway_map.csv")
    # print(map1.route.x)
    # print(map1.route.y)
    map1.draw(is_loop=False)

    testx = []
    testy = []
    for i in range(len(map1.route.s)):
        x, y = map1.route.get_center_xy(i)
        testx.append(x)
        testy.append(y)
    test = Line2D(testx, testy, 1, linestyle='-.', color='red')
    ax1.add_line(test)

    for i in range(0, len(map1.route.s)):
        angle = math.atan2(map1.route.dy[i], map1.route.dx[i]) + math.pi / 2
        # dir_x = math.cos(angle)*15
        # dir_y = math.sin(angle)*15
        dir_x = map1.route.dx[i] * 15
        dir_y = map1.route.dy[i] * 15
        ax1.arrow(map1.route.x[i], map1.route.y[i],
                  dir_x, dir_y, linewidth=1, color='r')

    ax1.relim()
    ax1.autoscale_view()
    ax1.grid(True)
    plt.show()


if __name__ == "__main__":
    main()
