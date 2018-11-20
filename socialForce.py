import numpy as np
from numpy import random as nr

class map:
    def __init__(self, wid, hei):
        self.graph = np.zeros((wid,hei))
    def randomPos(self):
        pos = nr.randint(1, 4, size=2)
        while self.graph[pos[0], pos[1]]==1:
            pos = nr.randint(1, 4, size=2)
        return pos
    def direct(self, pos):
        

class person:
    def __init__(self, pos):
        self.pos = pos


m = map(5, 5)
for i in range(10):
    print(m.randomPos())