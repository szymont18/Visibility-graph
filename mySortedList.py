import bisect
import math

from Obstacle import Line

EPS = 10**(-10)

class mySortedList:
    def __init__(self):
        self.tab = []


    def insertInOrder(self, val):
        index = bisect.bisect_right(self.tab,val)
        self.tab.insert(index, val)

    def removeElement(self,val: Line):
        binindex = self.binSearch(val, Line.cmpLine)

        for i in range(max(binindex,0), len(self.tab)):
            if self.tab[i] == val:
                self.tab.pop(i)
                return True
        return False

    def __len__(self):
        return len(self.tab)

    def __iter__(self):
        return self.tab.__iter__()

    def __getitem__(self, item):
        return self.tab[item]

    def clear(self):
        self.tab.clear()

    def binSearch(self, el: Line, halfLine: Line):
        l = 0
        r=len(self.tab)


        op = halfLine.p1
        targetIntersection = halfLine.getIntersectionPoint(el)


        tarLen = math.sqrt((op.x - targetIntersection[0])**2 + (op.y - targetIntersection[1])**2)
        while r > l:
            mid = (l+r)//2
            #print(mid, self.tab[mid], el)
            ipoint = halfLine.getIntersectionPoint(self.tab[mid])
            clen = math.sqrt((op.x-ipoint[0])**2 + (op.y - ipoint[1])**2)

            if mid != 0:
                im1point = halfLine.getIntersectionPoint(self.tab[mid - 1])
                clen2 = math.sqrt((op.x - im1point[0]) ** 2 + (op.y - im1point[1]) ** 2)

            if mid == 0 or (tarLen - clen2 > 0 and abs(clen-tarLen) < EPS):
                return mid
            elif tarLen - clen < EPS:
                l = mid+1
            else:
                r = mid-1

        return -1