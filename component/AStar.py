import time


class Point:
    def __init__(self, x, y, endx, endy, g=0):
        self.x = x
        self.y = y
        self.g = g
        self.h = abs(endx - x) + abs(endy - y)
        self.father = Point

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return "[" + str(self.x) + "," + str(self.y)+']'


# init mymap
mymap = [[0 for i in range(52)] for i in range(52)]
index = 0
with open('map.txt', 'r') as f:
    a = f.readline().replace('[', '').replace(']', '').replace(',', '').replace('\n', '')
    for i in a:
        if i == '1':
            mymap[int(index / 52)][index % 52] = 1
        index += 1
# init list
openlist = []
closelist = []


# 获取当前开表中代价最小的一个
def getmin():
    current = openlist[0]
    for point in openlist:
        if point.g + point.h < current.g + current.h:
            current = point
    return current


# 向周围四个点试探
def search(minf, x, y, endx, endy):
    if minf.x + x < 0 or minf.x + x > 51:
        return
    if minf.y + y < 0 or minf.y + y > 51:
        return
    if mymap[minf.x + x][minf.y + y] != 0:
        return
    p = Point(minf.x + x, minf.y + y, endx, endy)
    if p in closelist:
        return
    if p not in openlist:
        p.g = minf.g + 1
        p.father = minf
        openlist.append(p)
        return
    current = openlist[openlist.index(p)]
    if minf.g + 1 < current.g:
        current.g = minf.g + 1
        current.father = minf


def getpath(startx, starty, endx, endy):
    startpoint = Point(startx, starty, endx, endy, 0)
    endpoint = Point(endx, endy, endx, endy, 0)
    path = []
    openlist.append(startpoint)
    while True:
        minf = getmin()
        closelist.append(minf)
        openlist.remove(minf)
        search(minf, -1, 0, endx, endy)
        search(minf, 1, 0, endx, endy)
        search(minf, 0, -1, endx, endy)
        search(minf, 0, 1, endx, endy)
        if endpoint in closelist:
            point = closelist[closelist.index(endpoint)]
            while True:
                if point:
                    path.append(point)
                    if point == startpoint:
                        return path
                    point = point.father
                else:
                    return path
        if len(openlist) == 0:
            return


a = getpath(1, 1, 20, 20)
for i in range(52):
    for j in range(52):
        if mymap[i][j] == 0:
            print('.', end=' ')
        elif mymap[i][j] == 1:
            print('X', end=' ')
        else:
            print('*', end=' ')
    print()
print(time.process_time())
for i in a:
    print(str(i)+',', end="")
