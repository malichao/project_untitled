from car import Car
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
        self.fig, self.axes = plt.subplots(2, 2, figsize=(12, 8))
        self.axes = self.axes.flatten()
        for ax in self.axes:
            ax.grid(True,color='grey', linestyle=':')
            ax.set_aspect("equal")
            ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
            ax.yaxis.set_major_locator(ticker.MultipleLocator(5))
        self.axes[3].get_xaxis().set_visible(False)
        self.axes[3].get_yaxis().set_visible(False)

        self.cars = [Car(self.axes[0], label='0'),
                     Car(self.axes[1], label='1'), ]
        self.cars[0].set_pose(0, 0, math.pi / 2)
        self.cars[0].v = 2
        self.cars[1].set_pose(0, 0, math.pi / 4)
        self.cars[1].v = 2

        animation.TimedAnimation.__init__(
            self, self.fig, interval=250, blit=False)

    def _draw_frame(self, framedata, action_masks=[1, 0, 0, 0]):
        self._drawn_artists = []
        self._drawn_artists[:] = []
        for car in self.cars:
            car.drive(0.25)
            self._drawn_artists.extend(car.draw())

        for car, ax in zip(self.cars, self.axes):
            ax.set_xlim(car.x - 15, car.x + 15)
            ax.set_ylim(car.y - 10, car.y + 10)
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
