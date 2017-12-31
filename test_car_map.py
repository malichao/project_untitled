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
        self.axes.grid(True,color='grey', linestyle=':')
        self.axes.set_aspect("equal")
        self.axes.xaxis.set_major_locator(ticker.MultipleLocator(5))
        self.axes.yaxis.set_major_locator(ticker.MultipleLocator(5))

        self.map = Map(self.axes)
        self.map.read("highway_map.csv")

        self.car = Car(self.axes, label='0')
        self.car.set_route(self.map.route)
        self.car.set_route_idx(1)
        self.car.v=20

        animation.TimedAnimation.__init__(self, self.fig, interval=250, blit=False)

    def _draw_frame(self, framedata, action_masks=[1, 0, 0, 0]):
        # Update simulation
        self.car.follow_route()

        # Update visualization elements
        self._drawn_artists = []
        self._drawn_artists[:] = []
        self._drawn_artists.extend(self.map.draw())
        self._drawn_artists.extend(self.car.draw())

        # Update view
        view_x = 50
        view_y = view_x/2
        self.axes.set_xlim(self.car.x - view_x, self.car.x + view_x)
        self.axes.set_ylim(self.car.y - view_y, self.car.y + view_y)
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
