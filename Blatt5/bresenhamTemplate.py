from Tkinter import *
from Canvas import *
import sys


WIDTH  = 400 # width of canvas
HEIGHT = 400 # height of canvas

HPSIZE = 10 # half of point size (must be integer)
FCOLOR = "#AAAAAA" # fill color
BCOLOR = "#000000" # boundary color

pointList = []   # list of points
elementList = [] # list of elements (used by Canvas.delete(...))


def drawGrid(s):
    """ draw a rectangular grid """
    for i in range(0,WIDTH,s):
	element = can.create_line(i,0,i,HEIGHT)
    for i in range(0,HEIGHT,s):
	element = can.create_line(0,i,WIDTH,i)


def drawPoints():
    """ draw points """
    for p in pointList:
	element = can.create_rectangle(p[0]-HPSIZE, p[1]-HPSIZE,
				       p[0]+HPSIZE, p[1]+HPSIZE,
				       fill=FCOLOR, outline=BCOLOR)
	elementList.append(element)    


def drawLines():
    """ draw lines """
    for line in zip(pointList[::2],pointList[1::2]):
	drawBresenhamLine(line[0],line[1])
	element = can.create_line(line,width=1)
	elementList.append(element)    


def drawBresenhamLine(p,q):
    """ draw a line using bresenhams algorithm """
    gespiegelt = False
    gedreht = False
    if not p[0]<= q[0]:
        p,q = q,p

    m = (q[1]-p[1])/(q[0]-p[0])

    if abs(m) > 1:
        gedreht = True
        p[0],p[1] = p[1],p[0]
        q[0],q[1] = q[1],q[0]

    if m < 0:
        gespiegelt = True
        p[0],p[1] = p[0],-p[1]
        q[0],q[1] = q[0],-q[1]
    
    
    #Mittelpunktalgo
    a, b = q[1]-p[1],p[0]-q[0]
    d = 2*a + b
    IncE = 2*a
    IncNE = 2*(a+b)
    y = p[1]
    for x in range(p[0], q[0]+HPSIZE*2,HPSIZE*2):
        if gespiegelt and gedreht:
            pointList.append([-y,x])
        elif gespiegelt:
            pointList.append([x,-y])
        elif gedreht:
            pointList.append([y,x])
        if d<= 0:
            d += IncE
        else:
            d+= IncNE
            y += HPSIZE*2

    drawPoints()
    

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
    drawLines()

def clearAll():
    """ clear all (point list and canvas) """
    can.delete(*elementList)
    del pointList[:]


def mouseEvent(event):
    """ process mouse events """
    # get point coordinates
    d = 2*HPSIZE
    p = [d/2+d*(event.x/d), d/2+d*(event.y/d)] 
    pointList.append(p)
    draw()


if __name__ == "__main__":
    #check parameters
    if len(sys.argv) != 1:
       print "draw lines using bresenhams algorithm"
       sys.exit(-1)

    # create main window
    mw = Tk()
    mw._root().wm_title("Line drawing using bresenhams algorithm")

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

    drawGrid(2*HPSIZE)
    # start
    mw.mainloop()
    
