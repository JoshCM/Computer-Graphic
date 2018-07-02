from Tkinter import *
from Canvas import *
import sys
import numpy as np

WIDTH = 400  # width of canvas
HEIGHT = 400  # height of canvas

HPSIZE = 2  # half of point size (must be integer)
CCOLOR = "#000000"  # blue (color of control-points and polygon)

BCOLOR = "#00FFFF"  # black (color of bezier curve)
BWIDTH = 2  # width of bezier curve

k = 3
m = 150

pointList = []  # list of (control-)points
elementList = []  # list of elements (used by Canvas.delete(...))

class Point(object):

    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __eq__(self,point):

        self.x = point.x
        self.y = point.y

        return self


    def __add__(self,point):

        p = Point(0,0)
        p.x = self.x + point.x
        p.y = self.y + point.y

        return p

    def __sub__(self,point):

        p = Point(0,0)
        p.x = self.x - point.x
        p.y = self.y - point.y

        return p

    def __mul__(self, fac):
        p = Point(0,0)
        p.x = self.x *fac
        p.y = self.y *fac

        return p

    def __truediv__(self, fac):

        p = Point(0,0)
        p.x = self.x /fac
        p.y = self.y /fac

        return p

    def __repr__(self):
        return "x" + str(self.x) + "y" + str(self.y)


def drawPoints():
    """ draw (control-)points """
    for p in pointList:
        element = can.create_oval(p.x - HPSIZE, p.y - HPSIZE,
                                  p.x + HPSIZE, p.y + HPSIZE,
                                  fill=CCOLOR, outline=CCOLOR)
        elementList.append(element)


def drawPolygon():
    """ draw (control-)polygon conecting (control-)points """
    if len(pointList) > 1:
        for i in range(len(pointList) - 1):
            element = can.create_line(pointList[i].x, pointList[i].y,
                                      pointList[i + 1].x, pointList[i + 1].y,
                                      fill=CCOLOR)
            elementList.append(element)


def deBoor(j,i,degree,controlpoints,knotvector,t):

    if j == 0:
        return controlpoints[i]
    else:
        a = (t - knotvector[i])/ (knotvector[i-j + degree] - knotvector[i]) #alpha berechnen
        return (deBoor(j-1,i-1,degree,controlpoints,knotvector,t) * (1-a))  + (deBoor(j-1,i,degree,controlpoints,knotvector,t) * a)


def drawBSpline():
    """ draw bezier curve defined by (control-)points """

    points = []

    n = len(pointList) -1
    knotvector = []

    count = 1

    for ele in range(k):
        knotvector.append(0)

    for e in range(1,n - (k-2)):
        knotvector.append(count)
        count+=1

    for ele in range(k):
        knotvector.append(count)

    print(knotvector)

    if len(pointList) >= k: #nur kurve zeichnen, wenn wenigstens k-Punkte definiert sind

        dis = knotvector[-1]
        idx = 0
        while idx < dis:

            r = findr(idx,knotvector)

            if r != -1:

                p = deBoor(k-1,r,k,pointList,knotvector,idx)

                points.append(p)
                idx += 1./m



        for p in points:
            element = can.create_oval(p.x - HPSIZE, p.y - HPSIZE, p.x + HPSIZE, p.y + HPSIZE, fill=BCOLOR,outline=BCOLOR)
            elementList.append(element)



def findr(t,knotvector):

    for i in range(1,len(knotvector)):
        if t < knotvector[i]:
            return i-1
        elif t == knotvector[-1]:
            return len(knotvector)-1

    return -1

def slide(value=None):

    global k,m
    k= w1.get()
    m = w2.get()
    draw()

def quit(root=None):
    """ quit programm """
    if root == None:
        sys.exit(0)
    root._root().quit()
    root._root().destroy()


def draw():
    """ draw elements """
    can.delete(*elementList)
    drawPoints()
    drawPolygon()
    drawBSpline()


def clearAll():
    """ clear all (point list and canvas) """
    can.delete(*elementList)
    del pointList[:]


def mouseEvent(event):
    """ process mouse events """
    pointList.append(Point(event.x, event.y))
    draw()


if __name__ == "__main__":
    # check parameters
    if len(sys.argv) != 1:
        print("pointViewerTemplate.py")
        sys.exit(-1)

    # create main window
    mw = Tk()

    # create and position canvas and buttons
    cFr = Frame(mw, width=WIDTH, height=HEIGHT, relief="sunken", bd=1)
    cFr.pack(side="top")
    can = Canvas(cFr, width=WIDTH, height=HEIGHT)
    can.bind("<Button-1>", mouseEvent)
    can.pack()
    cFr = Frame(mw)
    cFr.pack(side="left")
    bClear = Button(cFr, text="Clear", command=clearAll)
    bClear.pack(side="left")
    w1 = Scale(mw,from_=3,to_=10,orient=HORIZONTAL,command = slide)
    w1.pack()
    w2 = Scale(mw, from_=50, to_=400, orient=HORIZONTAL,command = slide)
    w2.pack()
    eFr = Frame(mw)
    eFr.pack(side="right")
    bExit = Button(eFr, text="Quit", command=(lambda root=mw: quit(root)))
    bExit.pack()

    # start
    mw.mainloop()

