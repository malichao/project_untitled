import math
import numpy as np

class TrajectoryGenerator:
    def __init__(self, axes=None):
        self.trajs = []
        self.t = []
        self.lines = []
        self.axes = axes
        
    def generate(self,start_s,start_d,goal_s,goal_d,t):
        self.trajs.append([self.jmt(start_s,goal_s,t),self.jmt(start_d,goal_d,t)])
        self.t.append(t)

    def draw(self):
        self.lines[:]=[]
        for traj,t in zip(self.trajs,self.t):
            x,y=self.draw_traj(traj,t)
            self.lines.append(Line2D(x,y,1,color='r'))

        for line in self.lines:
            self.axes.add_line(line)

    def draw_traj(self,traj,T):
        t = 0
        s = self.to_equation(traj[0])
        d = self.to_equation(traj[1])
        x = []
        y = []
        while t <= T+0.01:
            x.append(s(t))
            y.append(d(t))
            t += 0.1
        return x,y

    def jmt(self,start, end, T):
        """
        Calculates Jerk Minimizing Trajectory for start, end and T.
        """
        a_0, a_1, a_2 = start[0], start[1], start[2] / 2.0
        c_0 = a_0 + a_1 * T + a_2 * T**2
        c_1 = a_1 + 2* a_2 * T
        c_2 = 2 * a_2

        A = np.array([
                [  T**3,   T**4,    T**5],
                [3*T**2, 4*T**3,  5*T**4],
                [6*T,   12*T**2, 20*T**3],
            ])
        B = np.array([
                end[0] - c_0,
                end[1] - c_1,
                end[2] - c_2
            ])
        a_3_4_5 = np.linalg.solve(A,B)
        alphas = np.concatenate([np.array([a_0, a_1, a_2]), a_3_4_5])
        return alphas

    def to_equation(self,coefficients):
        """
        Takes the coefficients of a polynomial and creates a function of
        time from them.
        """
        def f(t):
            total = 0.0
            for i, c in enumerate(coefficients):
                total += c * t ** i
            return total
        return f
        

def main():
    print("Test trajectory generation")
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111, aspect='equal')

    traj_gen = TrajectoryGenerator(ax1)
    T = 5.0
    v = 2
    start_s = np.array([ 0, v, 0])
    start_d = np.array([ 4, 0, 0])
    delta_s = np.array([10, 0, 0])
    delta_d = np.array([-4, 0, 0])
    traj_gen.generate(start_s,start_d,
                        start_s+delta_s,
                        start_d+delta_d,
                        T)
    traj_gen.draw()

    ax1.set_xlim(-30, 30)
    ax1.set_ylim(-30, 30)
    ax1.grid(True)
    plt.show()


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    from matplotlib.lines import Line2D
    main()
