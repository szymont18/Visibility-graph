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
        index = bisect.bisect_left(self.tab, val)-1
        #binindex = self.binSearch(val, Line.cmpLine)

        for i in range(max(index,0), len(self.tab)):
            if self.tab[i] == val:
                self.tab.pop(i)
                return True
        for i in range(len(self.tab)):
            print(self.tab[i])
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
        while l < r:
            mid = (l+r)//2
            print(mid, self.tab[mid])
            ipoint = halfLine.getIntersectionPoint(self.tab[mid])
            clen = math.sqrt((op.x-ipoint[0])**2 + (op.y - ipoint[1])**2)
            if clen - tarLen > EPS:
                r = mid-1
            elif clen - tarLen < -EPS:
                l = mid+1
            else:
                return mid