import numpy as np
import numpy.random as nr
from component import BFS as bfs
from component import person


class ForceMap:
    def __init__(self, graph, width, height, x, y, num):
        self.crowd = []
        self.width = width
        self.height = height
        self.distMap = bfs.BFS(graph, width, height, x, y).dist
        self.randomPos(width, height, num)
        print(self.personMap())
        np.set_printoptions(threshold=np.NaN)
        print(self.distMap)
        self.A = 2000
        self.B = 0.08
        self.r = 0.2
        self.k = 120000
        self.K = 240000

    def randomPos(self, width, height, num):  # 随机生成行人位置，行人不会在墙内，多个行人也不会出现在同一块中
        i = 0
        tmp = []
        while i < num:
            px = nr.randint(1, width - 1)
            py = nr.randint(1, height - 1)
            if self.distMap[px, py] != -1:
                if (px+0.5, py+0.5) not in self.crowd:
                    tmp.append((px, py))
                    self.crowd.append(person.Person(px+0.5, py+0.5))
                    i += 1

    def obstacleMap(self):  # 导出障碍地图格式字符串
        st = '['
        for i in range(self.height):
            for j in range(self.width):
                if self.distMap[i, j] == -1:
                    st += '[{},{}],'.format(i, j)
        st += ']'
        return st

    def personMap(self):  # 导出行人位置图字符串
        st = '['
        for p in self.crowd:
            st += str(p) + ','
        return st + '],'

    def clear(self):  # 清空上一轮计算的力
        for p in self.crowd:
            p.clearForce()

    def setDir(self):  # 确定每个行人的寻路方向
        for p in self.crowd:
            x = int(p.pos[0])
            y = int(p.pos[1])
            nd = self.distMap[x, y]
            if nd - self.distMap[x - 1, y] == 1:
                p.setDir(np.array([-1, 0]))
            elif nd - self.distMap[x + 1, y] == 1:
                p.setDir(np.array([1, 0]))
            elif nd - self.distMap[x, y - 1] == 1:
                p.setDir(np.array([0, -1]))
            elif nd - self.distMap[x, y + 1] == 1:
                p.setDir(np.array([0, 1]))

    def g(self, dis):
        if dis <= 0:
            return 0
        else:
            return dis

    def wallR(self, i, x, y):
        for xi in range(x + 1, self.width):
            if self.distMap[xi, y] == -1:
                return xi - self.crowd[i].pos[0]
        return self.width

    def wallL(self, i, x, y):
        for xi in range(x - 1, -1, -1):
            if self.distMap[xi, y] == -1:
                return self.crowd[i].pos[0] - xi - 1
        return self.width

    def wallU(self, i, x, y):
        for yi in range(y + 1, self.height):
            if self.distMap[x, yi] == -1:
                return yi - self.crowd[i].pos[1]
        return self.height

    def wallD(self, i, x, y):
        for yi in range(y - 1, -1, -1):
            if self.distMap[x, yi] == -1:
                return self.crowd[i].pos[1] - yi - 1
        return self.height

    def wallForce(self, diw, niw, vi):
        return (self.A * np.exp((self.r - diw) / self.B) + self.k * self.g(self.r - diw)) * niw - \
               self.K * self.g(self.r - diw) * vi.dot(np.array(-niw[1], niw[0]))*np.array(-niw[1], niw[0])

    def step(self):
        self.clear()  # 清空上一步的力
        self.setDir()  # 计算目标方向
        for i in range(len(self.crowd)):  # 计算两行人之间的力
            for j in range(i + 1, len(self.crowd)):
                Dij = self.crowd[i].pos - self.crowd[j].pos
                dij = np.linalg.norm(Dij)  # 两行人间距离
                rij = self.r * 2  # 两行人的半径之和
                nij = Dij / dij
                tij = np.array([-nij[1], nij[0]])
                force = (self.A * np.exp((rij - dij) / self.B) + self.k * self.g(rij - dij)) * nij + \
                        self.K * self.g(rij - dij) * (self.crowd[j].curV - self.crowd[i].curV).dot(tij)*tij
                self.crowd[i].force(force)
                self.crowd[j].force(-force)

        for i in range(len(self.crowd)):  # 计算墙力
            x = int(self.crowd[i].pos[0])
            y = int(self.crowd[i].pos[1])
            dup = self.wallU(i, x, y)
            ddown = self.wallD(i, x, y)
            dright = self.wallR(i, x, y)
            dleft = self.wallL(i, x, y)
            fup = self.wallForce(dup, np.array([0, -1]), self.crowd[i].curV)
            fdown = self.wallForce(ddown, np.array([0, 1]), self.crowd[i].curV)
            fright = self.wallForce(dright, np.array([-1, 0]), self.crowd[i].curV)
            fleft = self.wallForce(dleft, np.array([1, 0]), self.crowd[i].curV)
            self.crowd[i].force(fup)
            self.crowd[i].force(fdown)
            self.crowd[i].force(fright)
            self.crowd[i].force(fleft)
            self.crowd[i].calculate()
        print(self.personMap())


graph = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, 0,
         0,
         0, 0, 0, 0, 0, 0, 0, 0, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, 0,
         0,
         0, 0, 0, 0, 0, 0, 0, 0, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1,
         -1,
         -1, -1, -1, -1, -1, -1, -1, -1, -1]

forceMap = ForceMap(graph, 12, 12, 10, 5, 10)
print(forceMap.obstacleMap())
for i in range(80):
    forceMap.step()
# p1 = person.Person(1, 1)
# p2 = person.Person(2, 2)
# print(p2.pos - p1.pos)