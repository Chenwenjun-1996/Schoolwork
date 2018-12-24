import numpy as np


class Person:
    def __init__(self, x, y):
        self.pos = np.array([x, y], dtype=float)
        self.maxV = 0.4    # 最大速度
        self.desV = 0.3     # 期望速度
        self.curV = np.zeros(2, dtype=float)  # 当前速度
        self.dir = np.array(2)  # 寻路方向
        self.fc = np.array(2, dtype=float)  # 力
        self.tao = 0.5  # 寻路算法部分常数
        self.m = 80.0   # 力部分常数
        self.dt = 0.5   # 时间间隔

    def clearForce(self):
        self.fc = np.zeros(2)
        self.dir = np.zeros(2)

    def force(self, f):
        self.fc += f

    def setDir(self, dire):
        self.dir += dire

    def calculate(self):
        dl = np.linalg.norm(self.dir)
        if dl == 0:
            self.curV += ((np.random.normal(0, 1, size=2) * self.desV - self.curV) / self.tao + self.fc / self.m) * self.dt
        else:
            self.curV += ((self.dir / dl * self.desV - self.curV) / self.tao + self.fc / self.m)*self.dt + np.random.normal(0, 1, size=2)/1000
        v = np.linalg.norm(self.curV)
        if v > self.maxV:
            self.curV = self.curV/v*self.maxV
        self.pos += self.curV * self.dt

    def __str__(self):
        return '[' + '%.6f' % (self.pos[0]) + ',' + '%.6f' % (self.pos[1]) + ']'
