from Tkinter import *
from Canvas import *
import sys

WIDTH  = 400 # width of canvas
HEIGHT = 400 # height of canvas

HPSIZE = 2 # half of point size (must be integer)
CCOLOR = "#0000FF" # blue

elementList = [] # list of elements (used by Canvas.delete(...))

polygon1 = []
polygon2 = []
displayedPolygon = []

time = 0
dt = 0.01
def printPoints():
    print "displayedPolygon","  polygon1","   polygon2"
    for ele in zip(displayedPolygon,zip(polygon1,polygon2)):
        print ele

def readPolygon(path):
    with open(path) as poly:
        list = []
        for line in poly:
            list.append([int(float(line.split()[0])*HEIGHT),HEIGHT-int(float(line.split()[1])*HEIGHT)])
        return list

def drawObjekts():
    """ draw polygon and points """
    # TODO: inpterpolate between polygons and render
    for (p,q) in zip(displayedPolygon,displayedPolygon[1:]):
        elementList.append(can.create_line(p[0], p[1], q[0], q[1],
                                           fill=CCOLOR))
        elementList.append(can.create_oval(p[0]-HPSIZE, p[1]-HPSIZE,
                                           p[0]+HPSIZE, p[1]+HPSIZE,
                                           fill=CCOLOR, outline=CCOLOR))
            


def quit(root=None):
    """ quit programm """
    if root==None:
        sys.exit(0)
    root._root().quit()
    root._root().destroy()


def draw():
    """ draw elements """
    can.delete(*elementList)
    del elementList[:]
    drawObjekts()
    can.update()


def forward():
    global time
    while(time<1):
        time += dt
        for idx in range(len(displayedPolygon)):
            displayedPolygon[idx][0], displayedPolygon[idx][1] = (polygon1[idx][0]+time*(polygon2[idx][0]-polygon1[idx][0])),(polygon1[idx][1]+time*(polygon2[idx][1]-polygon1[idx][1]))
        print time
        draw()
    printPoints()


def backward():
    global time
    while(time>0):
        time -= dt
        for idx in range(len(displayedPolygon)):
            displayedPolygon[idx][0], displayedPolygon[idx][1] = (polygon1[idx][0]+time*(polygon2[idx][0]-polygon1[idx][0])),(polygon1[idx][1]+time*(polygon2[idx][1]-polygon1[idx][1]))
        print time
        draw()
    

if __name__ == "__main__":
    # check parameters
    if len(sys.argv) != 3:
       print "morph.py firstPolygon secondPolygon"
       sys.exit(-1)

    # TODOS:
    # - read in polygons
    # - transform from local into global coordinate system 
    # - make both polygons contain same number of points

    polygon1 = readPolygon(sys.argv[1])
    polygon2 = readPolygon(sys.argv[2])

    if len(polygon1)<=len(polygon2):
        while len(polygon1) != len(polygon2):
            polygon1.append(polygon1[-1])
    else:
        while len(polygon2) != len(polygon1):
            polygon2.append(polygon2[-1])

    for ele in polygon1:
        displayedPolygon.append([ele[0],ele[1]])
    #displayedPolygon = polygon1[:]
    printPoints()





    # create main window
    mw = Tk()
    mw._root().wm_title("Morphing")

    # create and position canvas and buttons
    cFr = Frame(mw, width=WIDTH, height=HEIGHT, relief="sunken", bd=1)
    cFr.pack(side="top")
    can = Canvas(cFr, width=WIDTH, height=HEIGHT)
    can.pack()
    cFr = Frame(mw)
    cFr.pack(side="left")
    bClear = Button(cFr, text="backward", command=backward)
    bClear.pack(side="left")
    bClear = Button(cFr, text="forward", command=forward)
    bClear.pack(side="left")
    eFr = Frame(mw)
    eFr.pack(side="right")
    bExit = Button(eFr, text="Quit", command=(lambda root=mw: quit(root)))
    bExit.pack()
    draw()
    
    # start
    mw.mainloop()
    
