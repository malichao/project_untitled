from car import Car
from map import Map
import math
from numpy import zeros
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.text import Annotation
import matplotlib.ticker as ticker
import matplotlib.animation as animation


class DriveCar(animation.TimedAnimation):
    def __init__(self):
        self.fig, self.axes = plt.subplots(1, 1, figsize=(12, 8))
        self.axes.grid(True, color='grey', linestyle=':')
        self.axes.set_aspect("equal")
        self.axes.xaxis.set_major_locator(ticker.MultipleLocator(10))
        self.axes.yaxis.set_major_locator(ticker.MultipleLocator(10))

        self.map = Map(self.axes)
        self.map.read("highway_map.csv")

        self.cars = [Car(self.axes, label='0'),
                     Car(self.axes, label='1'),
                     Car(self.axes, label='2')]
        for i in range(len(self.cars)):
            self.cars[i].set_route(self.map.route, s=i * 20, lane=i)
            self.cars[i].v = 40 - i * 5

        animation.TimedAnimation.__init__(
            self, self.fig, interval=50, blit=False)

    def _draw_frame(self, framedata, action_masks=[1, 0, 0, 0]):
        # Update simulation
        for car in self.cars:
            car.follow_route()

        # Update visualization elements
        self._drawn_artists = []
        self._drawn_artists[:] = []
        self._drawn_artists.extend(self.map.draw())
        for car in self.cars:
            self._drawn_artists.extend(car.draw())

        # Update view
        view_x = 50
        view_y = view_x / 2
        self.axes.set_xlim(self.cars[0].x - view_x, self.cars[0].x + view_x)
        self.axes.set_ylim(self.cars[0].y - view_y, self.cars[0].y + view_y)
        #ax.autoscale_view()

    def new_frame_seq(self):
        return iter(range(50))

    def _init_draw(self):
        pass


av = DriveCar()
# Writer = animation.writers['ffmpeg']
# writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
# av.save('PLAN-4223.mp4', writer=writer)
plt.show()
