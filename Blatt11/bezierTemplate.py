from Tkinter import *
from Canvas import *
import numpy as np
import sys

WIDTH = 400  # width of canvas
HEIGHT = 400  # height of canvas

HPSIZE = 2  # half of point size (must be integer)
CCOLOR = "#0000FF"  # blue (color of control-points and polygon)

BCOLOR = "#000000"  # black (color of bezier curve)
BWIDTH = 2  # width of bezier curve

pointList = []   # list of (control-)points
elementList = []  # list of elements (used by Canvas.delete(...))
k = 0
m = 0

    

def drawPoints():
    """ draw (control-)points """
    for p in pointList:
	element = can.create_oval(p[0]-HPSIZE, p[1]-HPSIZE,
                                  p[0]+HPSIZE, p[1]+HPSIZE,
                                  fill=CCOLOR, outline=CCOLOR)
	elementList.append(element)    


def drawPolygon(pointList = pointList):
    """ draw (control-)polygon conecting (control-)points """
    if len(pointList) > 1:
        for i in range(len(pointList)-1):
            element = can.create_line(pointList[i][0], pointList[i][1],
                                      pointList[i+1][0], pointList[i+1][1],
                                      fill=CCOLOR)
            elementList.append(element)

def deBoor(j,i,degree,controlpoints,knotvector,t):

    if j == 0:
        return np.array(controlpoints[i])
    else:
        a = (t - knotvector[i])/ (knotvector[i-j + degree] - knotvector[i]) #alpha berechnen
        return (deBoor(j-1,i-1,degree,controlpoints,knotvector,t) * (1-a))  + (deBoor(j-1,i,degree,controlpoints,knotvector,t) * a)


def drawCurve():
    global pointList,m,k
    curvepoints = []

    n = len(pointList)-1
    lastKnot = n-(k-2)

    T = [0]*k+[x for x in range(1,lastKnot)]+[lastKnot]*k

    if len(pointList) >= k:
        end = T[-1]
        idx = 0
        while idx < end:
            r = getR(idx,T)
            if r != None:
                curvepoints.append(deBoor(k-1,r,k,pointList,T,idx))
                idx += 1.0/m

        drawPolygon(curvepoints)

def getR(t,T):
    for index in range(1,len(T)):
        if t == T[-1]:
            return len(T)-1
        elif t < T[index]:
            return index-1
    return None


def quit(root=None):
    """ quit programm """
    if root==None:
        sys.exit(0)
    root._root().quit()
    root._root().destroy()


def draw():
    """ draw elements """
    can.delete(*elementList)
    drawPoints()
    drawPolygon()
    drawCurve()


def clearAll():
    """ clear all (point list and canvas) """
    can.delete(*elementList)
    del pointList[:]


def mouseEvent(event):
    """ process mouse events """
    print "left mouse button clicked at ", event.x, event.y
    pointList.append([event.x, event.y])
    draw()

def kslider(slider):
    global k
    k = int(slider)
    draw()
    print(k)

def mslider(slider):
    global m
    m = int(slider)
    draw()
    print(m)



if __name__ == "__main__":
    # check parameters
    if len(sys.argv) != 1:
       print "pointViewerTemplate.py"
       sys.exit(-1)

    # create main window
    mw = Tk()

    # create and position canvas and buttons
    cFr = Frame(mw, width=WIDTH, height=HEIGHT, relief="sunken", bd=1)
    cFr.pack(side="top")
    can = Canvas(cFr, width=WIDTH, height=HEIGHT)
    can.bind("<Button-1>",mouseEvent)
    can.pack()
    cFr = Frame(mw)
    cFr.pack(side="left")
    bClear = Button(cFr, text="Clear", command=clearAll)
    bClear.pack(side="left")
    eFr = Frame(mw)
    eFr.pack(side="right")
    bExit = Button(eFr, text="Quit", command=(lambda root=mw: quit(root)))
    bExit.pack()
    sFr = Frame(mw)
    sFr.pack()
    kslider = Scale(sFr, from_ = 3, to = 10, command = kslider, orient=HORIZONTAL)
    kslider.pack()
    mslider = Scale(sFr, from_ = 20, to = 100, command = mslider, orient=HORIZONTAL)
    mslider.pack()

    # start
    mw.mainloop()