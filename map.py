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
        self.dx = []
        self.dy = []
        self.yaw = []
        self.lane_width = lane_width
        self.lane_num = lane_num
        if lane_num < 1:
            raise("Lane number must > 1")

    def read(self, file):
        with open(file) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            self.x[:] = []
            self.y[:] = []
            self.s[:] = []
            self.dx[:] = []
            self.dy[:] = []
            self.yaw[:] = []
            for row in reader:
                self.x.append(float(row['x']))
                self.y.append(float(row['y']))
                self.s.append(float(row['s']))
                self.dx.append(float(row['dx']))
                self.dy.append(float(row['dy']))

            for i in range(0, len(self.s) - 1):
                self.yaw.append(math.atan2(self.y[i + 1] - self.y[i],
                                           self.x[i + 1] - self.x[i]))
            self.yaw.append(self.yaw[-1])

    def to_center_xy(self, s, lane=0):
        idx = bisect.bisect(self.s, s) - 1
        next_idx = idx + 1
        if next_idx >= (len(self.s)):
            next_idx = 0

        cur_x, cur_y = self.get_center_xy(idx, lane)
        next_x, next_y = self.get_center_xy(next_idx, lane)

        ds = s - self.s[idx]
        ratio = ds / (self.s[next_idx] - self.s[idx])
        dx = (next_x - cur_x) * ratio
        dy = (next_y - cur_y) * ratio

        return cur_x + dx, cur_y + dy

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

    def read(self, file):
        self.route.read(file)

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
