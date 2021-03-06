import math
import numpy as np
from matplotlib.lines import Line2D


class TrajectoryGenerator:
    TRAJ = 0
    VEL = 1
    ACC = 2
    JERK = 3
    TRAJ_S = 0
    TRAJ_D = 1

    def __init__(self, axes):
        self.traj_coefs = []
        self.t = []
        self.lines = [[], [], [], []]
        self.axes = axes  # assuming [traj,vel,acc,jerk]
        self._draw_traj = self.draw_traj
        self.lines[self.TRAJ].append(Line2D([], [], 1, color='orange'))
        self.lines[self.TRAJ].append(Line2D([], [], 1, color='orange'))
        self.lines[self.TRAJ].append(Line2D([], [], 1, color='orange'))
        self.lines[self.VEL].append(Line2D([], [], 1, color='r'))
        self.lines[self.VEL].append(Line2D([], [], 1, color='b'))
        self.lines[self.ACC].append(Line2D([], [], 1, color='r'))
        self.lines[self.ACC].append(Line2D([], [], 1, color='b'))
        self.lines[self.JERK].append(Line2D([], [], 1, color='r'))
        self.lines[self.JERK].append(Line2D([], [], 1, color='b'))

        for line in self.lines[self.TRAJ]:
            self.axes[self.TRAJ].add_line(line)

    def clear(self):
        self.traj_coefs[:] = []
        self.t[:] = []

    def generate(self, start_s, start_d, goal_s, goal_d, t):
        self.traj_coefs.append(
            [self.jmt(start_s, goal_s, t), self.jmt(start_d, goal_d, t)])
        self.t.append(t)

    def draw(self):
        for i in range(len(self.t)):
            x, y = self._draw_traj(self.traj_coefs[i], self.t[i])
            self.lines[self.TRAJ][i].set_data(x, y)

        return

        i = -1
        for traj, t in zip(self.traj_coefs, self.t):
            i += 1
            if i >= len(self.lines[self.TRAJ]):
                self.lines[self.TRAJ].append(Line2D([], [], 1, color='orange'))
                self.axes[self.TRAJ].add_line(self.lines[self.TRAJ][-1])
            x, y = self._draw_traj(traj, t)
            self.lines[self.TRAJ][i].set_data(x, y)

            if len(self.axes) == 1:
                continue
            vel_s = self.differentiate(traj[self.TRAJ_S])
            x, y = self.draw_curve(vel_s, t)
            self.lines[self.VEL][i * 2].set_data(x, y)
            vel_d = self.differentiate(traj[self.TRAJ_D])
            x, y = self.draw_curve(vel_d, t)
            self.lines[self.VEL][i * 2 + 1].set_data(x, y)

            if len(self.axes) == 2:
                continue
            acc_s = self.differentiate(vel_s)
            x, y = self.draw_curve(acc_s, t)
            self.lines[self.ACC][i * 2].set_data(x, y)
            acc_d = self.differentiate(vel_d)
            x, y = self.draw_curve(vel_d, t)
            self.lines[self.ACC][i * 2 + 1].set_data(x, y)

            if len(self.axes) == 3:
                continue
            jerk_s = self.differentiate(acc_s)
            x, y = self.draw_curve(jerk_s, t)
            self.lines[self.JERK][i * 2].set_data(x, y)
            jerk_d = self.differentiate(acc_d)
            x, y = self.draw_curve(jerk_d, t)
            self.lines[self.JERK][i * 2 + 1].set_data(x, y)

        for i in range(4):
            if len(self.axes) > i:
                for line in self.lines[i]:
                    self.axes[i].add_line(line)

    def set_transform(self, to_pose):
        def _draw_traj(traj, T):
            x, y = self.draw_traj(traj, T)
            for i in range(len(x)):
                x[i], y[i], _ = to_pose(x[i], y[i])
            return x, y

        self._draw_traj = _draw_traj

    def draw_traj(self, traj, T):
        t = 0
        s = self.to_equation(traj[0])
        d = self.to_equation(traj[1])
        x = []
        y = []
        while t <= T + 0.01:
            x.append(s(t))
            y.append(d(t))
            t += 0.1
        return x, y

    def draw_curve(self, coef, T):
        t = 0
        func = self.to_equation(coef)
        x = []
        y = []
        while t <= T + 0.01:
            x.append(t)
            y.append(func(t))
            t += 0.1
        return x, y

    def jmt(self, start, end, T):
        """
        Calculates Jerk Minimizing Trajectory for start, end and T.
        """
        a_0, a_1, a_2 = start[0], start[1], start[2]

        A = np.array([
            [T**3,   T**4,    T**5],
            [3 * T**2, 4 * T**3,  5 * T**4],
            [6 * T,   12 * T**2, 20 * T**3],
        ])

        B = np.array([
            end[0] - (a_0 + a_1 * T + .5 * a_2 * T**2),
            end[1] - (a_1 + a_2 * T),
            end[2] - a_2
        ])

        a_3_4_5 = np.linalg.solve(A, B)
        alphas = np.concatenate([np.array([a_0, a_1, a_2]), a_3_4_5])
        return alphas

    def to_equation(self, coefficients):
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

    def differentiate(self, coefficients):
        """
        Calculates the derivative of a polynomial and returns
        the corresponding coefficients.
        """
        new_cos = []
        for deg, prev_co in enumerate(coefficients[1:]):
            new_cos.append((deg + 1) * prev_co)
        return new_cos


def test(traj_gen):
    import collections
    TestCase = collections.namedtuple('JMT', 'start goal t answer')
    test_cases = [
        TestCase(start=[0, 10, 0], goal=[10, 10, 0], t=1,
                 answer=[0.0, 10.0, 0.0, 0.0, 0.0, 0.0]),
        TestCase(start=[0, 10, 0], goal=[20, 15, 20], t=2,
                 answer=[0.0, 10.0, 0.0, 0.0, -0.625, 0.3125]),
        TestCase(start=[5, 10, 2], goal=[-30, -20, -4], t=5,
                 answer=[5.0, 10.0, 1.0, -3.0, 0.64, -0.0432]),
    ]
    np.set_printoptions(precision=3)
    for tc in test_cases:
        result = traj_gen.jmt(tc.start, tc.goal, tc.t)
        result_v = traj_gen.differentiate(result)
        result_a = traj_gen.differentiate(result_v)
        result_j = traj_gen.differentiate(result_a)
        print "answer :", tc.answer
        print "result s:", result
        print "result v:", result_v
        print "result a:", result_a
        print "result j:", result_j
        print ""


def main():
    print("Test trajectory generation")
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    axes = axes.flatten()

    traj_gen = TrajectoryGenerator(axes)

    #test(traj_gen)

    v = 10
    T = 7

    # straight
    start_s = np.array([0, 10, 0])
    delta_s = np.array([70, 0, 0])
    start_d = np.array([0, 0, 0])
    delta_d = np.array([0, 0, 0])
    traj_gen.generate(start_s, start_d,
                      start_s + delta_s,
                      start_d + delta_d,
                      T)
    # left
    start_s = np.array([0, 10, 0])
    delta_s = np.array([70, 0, 0])
    start_d = np.array([0, 0, 0])
    delta_d = np.array([-4, 0, 0])
    traj_gen.generate(start_s, start_d,
                      start_s + delta_s,
                      start_d + delta_d,
                      T)
    # right
    start_s = np.array([0, 10, 0])
    delta_s = np.array([70, 0, 0])
    start_d = np.array([0, 0, 0])
    delta_d = np.array([4, 0, 0])
    traj_gen.generate(start_s, start_d,
                      start_s + delta_s,
                      start_d + delta_d,
                      T)

    # traj_gen.traj_coefs.append([[1.00000000e+01,   1.00000000e+01,   0.00000000e+00,
    #                             -3.11756226e-02,   4.27280119e-03,  -1.65311853e-04],
    #                            [4.00000000e+00,   0.00000000e+00,   0.00000000e+00,
    #                             -1.23868869e-01,   2.54917914e-02,  -1.38838430e-03]])
    # traj_gen.t.append(7)

    traj_gen.draw()

    axes[0].set_xlim(-1, 100)
    axes[0].set_ylim(-5, 5)
    axes[0].grid(True, linestyle=':')

    for i in range(1, 4):
        axes[i].set_xlim(-1, T + 1)
        axes[i].set_ylim(-2 * v, 2 * v)
        axes[i].grid(True, linestyle=':')
    plt.show()


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    main()
