import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.lines import Line2D
from matplotlib.text import Annotation
import math


class Car:
    def __init__(self, axes=None, id=0, length=5, width=2, label='car0', color='black'):
        self.id = id
        self.v = 0
        self.set_pose(0, 0, 0)
        self.set_length_width(length, width)
        self.label = Annotation(
            label, [0, 0], size='small', annotation_clip=False)
        self.label.set_rotation_mode('anchor')
        self.bbox = Line2D([], [], 2, color=color)
        if axes:
            axes.add_line(self.bbox)
            axes.add_artist(self.label)

    def set_length_width(self, length, width):
        self.length = length    # x dir
        self.width = width      # y dir
        self._bbox_x = [0, length, length, 0, 0, length * 0.3, 0]
        self._bbox_y = [0, 0, width, width, 0, width * 0.5, width]
        for i in range(0, len(self._bbox_x)):
            self._bbox_x[i] -= length * 0.3
            self._bbox_y[i] -= width * 0.5
        self.bbox_x = [[], [], [], [], [], [], [], ]
        self.bbox_y = [[], [], [], [], [], [], [], ]

    def set_route(self, route, idx=0):
        self.route = route
        self.set_route_idx(0)

    def set_route_idx(self, idx):
        self.s = self.route.s[idx]
        self.route_idx = idx
        self.set_pose(self.route.x[idx],
                      self.route.y[idx], self.route.yaw[idx])

    def follow_route(self, lane=0, dt=0.1):
        next_idx = self.route_idx + 1
        if next_idx >= (len(self.route.s)):
            next_idx = 0

        self.s += self.v * dt
        x, y = self.route.to_center_xy(self.s)
        self.set_pose(x, y, self.yaw)

        if self.s > self.route.s[next_idx] or self.s > self.route.s[-1]:
            self.yaw = self.route.yaw[next_idx]
            self.route_idx = next_idx

    def drive(self, dt=0.1):
        self.x = self.x + self.v * math.cos(self.yaw) * dt
        self.y = self.y + self.v * math.sin(self.yaw) * dt

    def set_pose(self, x, y, yaw):
        self.x, self.y, self.yaw = x, y, yaw

    def draw(self, axes=None):
        # Update bounding box
        for i in range(0, len(self._bbox_x)):
            self.bbox_x[i], self.bbox_y[i] = self.local_to_global(self._bbox_x[i],
                                                                  self._bbox_y[i])
        self.bbox.set_data(self.bbox_x, self.bbox_y)

        # Update label position
        label_x, label_y = self.local_to_global(0.7, -0.2)
        self.label.set_x(label_x)
        self.label.set_y(label_y)
        self.label.set_rotation(self.yaw / math.pi * 180)

        return [self.bbox, self.label]

    def rotate(self, x, y, yaw):
        x_ = x * math.cos(yaw) - y * math.sin(yaw)
        y_ = x * math.sin(yaw) + y * math.cos(yaw)
        return x_, y_

    def local_to_global(self, x, y):
        x_, y_ = self.rotate(x, y, self.yaw)
        return x_ + self.x, y_ + self.y

    def global_to_local(self, x, y, offset, yaw):
        x_, y_ = x - self.x, y - self.y
        return self.rotate(x_, y_, -self.yaw)

    def to_figure_angle(self, radian):
        return -radian / math.pi * 180.


t = Annotation('car0', xy=(2, 1), xytext=(3, 1.5), color='black')


def main():
    print("Test Car class")
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111, aspect='equal')

    car1 = Car(ax1, label='113')
    car1.set_pose(5, 5, math.pi / 4)
    car1.draw()

    car2 = Car(ax1, label='5422', color='r')
    car2.set_pose(0, 0, math.pi * 0.8)
    car2.set_pose(0, 0, 0)
    car2.draw()

    ax1.set_xlim(-10, 10)
    ax1.set_ylim(-10, 10)
    ax1.grid(True)
    plt.show()


if __name__ == "__main__":
    main()
