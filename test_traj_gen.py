from car import Car
from map import Map
from trajectory_generation import TrajectoryGenerator
import math
from numpy import zeros
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.text import Annotation
import matplotlib.ticker as ticker
import matplotlib.animation as animation
import time

class DriveCar(animation.TimedAnimation):
    def __init__(self):
        self.fig, self.axes = plt.subplots(1, 1, figsize=(12, 8))
        self.axes.grid(True, color='grey', linestyle=':')
        self.axes.set_aspect("equal")
        self.axes.xaxis.set_major_locator(ticker.MultipleLocator(10))
        self.axes.yaxis.set_major_locator(ticker.MultipleLocator(10))

        self.map = Map(self.axes)
        self.map.read("highway_map.csv")

        self.cars = [Car(self.axes, label='0')]
        for i in range(len(self.cars)):
            self.cars[i].set_route(self.map.route, s=i * 20, lane=i)
            self.cars[i].v = 20 - i * 2

        self.traj_gen = TrajectoryGenerator([self.axes])
        self.traj_gen.set_transform(self.cars[0].route.to_pose)

        animation.TimedAnimation.__init__(
            self, self.fig, interval=50, blit=False)

        self.test = 0
        self.last_call = time.time()

    def _draw_frame(self, framedata, action_masks=[1, 0, 0, 0]):
        # Update simulation
        for car in self.cars:
            car.follow_route()

        # self.test+=1
        # if self.test>=3: return

        # Update trajectory generation
        self.traj_gen.clear()
        start_s = [self.cars[0].s, self.cars[0].v, 0]
        start_d = [self.cars[0].d, 0, 0]
        T = 3
        for i in range(self.cars[0].route.lane_num):
            goal_d = [self.cars[0].route.to_d(i), 0, 0]
            delta_d = goal_d[0] - start_d[0]
            goal_s = [start_s[0] + self.cars[0].v * T, self.cars[0].v, 0]
            #print start_s,start_d,goal_s,goal_d
            self.traj_gen.generate(start_s, start_d, goal_s, goal_d, T)

        # Update visualization elements
        self.map.draw()
        for car in self.cars:
            car.draw()
        self.traj_gen.draw()

        # Update view
        view_x = 80
        view_y = view_x / 2
        self.axes.set_xlim(self.cars[0].x - view_x, self.cars[0].x + view_x)
        self.axes.set_ylim(self.cars[0].y - view_y, self.cars[0].y + view_y)
        #ax.autoscale_view()
        print time.time() - self.last_call
        self.last_call = time.time()

    def new_frame_seq(self):
        return iter(range(50))

    def _init_draw(self):
        pass


av = DriveCar()
# Writer = animation.writers['ffmpeg']
# writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
# av.save('PLAN-4223.mp4', writer=writer)
plt.show()
