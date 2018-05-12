from Tkinter import *
from Canvas import *
import sys
import random
from numpy import *

WIDTH  = 400 # width of canvas
HEIGHT = 400 # height of canvas

HPSIZE = 1 # double of point size (must be integer)
COLOR = "#0000FF" # blue

NOPOINTS = 1000

pointList = [] # list of points (used by Canvas.delete(...))
objectPoints = []

def quit(root=None):
    """ quit programm """
    if root==None:
        sys.exit(0)
    root._root().quit()
    root._root().destroy()

def draw(points):
    projectionMatrix = matrix([[1,0,0,0],[0,1,0,0],[0,0,0,0],[0,0,0,1]])
    tranformObject(projectionMatrix,points)
    
    for i in range(len(points)):
        x,y = points[i][0],HEIGHT-points[i][1]
        p = can.create_oval(x-HPSIZE,y-HPSIZE,x+HPSIZE,y+HPSIZE, fill = COLOR, outline = COLOR)
        pointList.insert(0,p)


def getMiddlePoint(bottomleft,topright):
    return bottomleft + (topright-bottomleft)* 0.5

def tranformObject(matrix,objectPoints):
    for i in range(len(objectPoints)):
        objectPoints[i] = (array)(matmul(matrix,objectPoints[i]))
        objectPoints[i] = objectPoints[i].flatten()

def getScalingFactor(topright):
    return 1/sorted([topright[0],topright[1],topright[2]],reverse = True)[0]

def getBoundingBox():
    xmin,ymin,zmin = float(objectPoints[0][0]),float(objectPoints[0][1]),float(objectPoints[0][2])
    xmax,ymax,zmax = float(objectPoints[0][0]),float(objectPoints[0][1]),float(objectPoints[0][2])

    for point in range(1,len(objectPoints)):
        x,y,z = float(objectPoints[point][0]),float(objectPoints[point][1]),float(objectPoints[point][2])

        if x < xmin or x > xmax:
            if x < xmin:
                xmin = x
            else:
                xmax = x
        if y < ymin or y > ymax:
            if y < ymin:
                ymin = y
            else:
                ymax = y
        if z < zmin or z > zmax:
            if z < zmin:
                zmin = z
            else:
                zmax = z

    return (array([xmin,ymin,zmin,]),array([xmax,ymax,zmax]))

def copyPoints(objectPoints):
    newList = []
    for ele in objectPoints:
        newList.append(array([ele[0],ele[1],ele[2],ele[3]]))
    return newList


def rotYp(clockwise = False):
    """ rotate counterclockwise around y axis """
    can.delete(*pointList)
    print(getBoundingBox())
    if not clockwise:
        alpha = math.pi/12
    else:
        alpha = 2*math.pi - math.pi/12
    cos = math.cos(alpha)
    sin = math.sin(alpha)
    
    trans1 = matrix([[1,0,0,-WIDTH/2],[0,1,0,-HEIGHT/2],[0,0,1,0],[0,0,0,1]])
    rot = matrix([[cos,0,sin,0],[0,1,0,0],[-sin,0,cos,0],[0,0,0,1]])
    trans2 = matrix([[1,0,0,WIDTH/2],[0,1,0,HEIGHT/2],[0,0,1,0],[0,0,0,1]])

    tranformObject(trans1,objectPoints)
    tranformObject(rot,objectPoints)
    tranformObject(trans2,objectPoints)
    print("--------------------------------------")
    print(getBoundingBox())
    draw(copyPoints(objectPoints))

def rotYn():
    """ rotate clockwise around y axis """
    rotYp(clockwise=True)


if __name__ == "__main__":
    #check parameters
    if len(sys.argv) != 2:
       print("Nicht die passende Anzahl an Argumenten!")
       sys.exit(-1)
    else:
        path = "Objects/"+sys.argv[1]
        with open(path) as pointfile:
            objectPoints = [array([float(x) for x in x.split()]) for x in pointfile.readlines()]
            objectPoints = [append(x,[float(1.0)]) for x in objectPoints]

    #Bounding Box berechnen
    boundingBox = getBoundingBox()

    #Mittelpunkt der Boundingbox
    middlepoint = getMiddlePoint(boundingBox[0],boundingBox[1])

    #Translation des Objekts zum Ursprung
    translationMatrix = matrix([[1,0,0,-middlepoint[0]],[0,1,0,-middlepoint[1]],[0,0,1,-middlepoint[2]],[0,0,0,1]])
    tranformObject(translationMatrix,objectPoints)

    #Erneute berechnung des Boundingbox und ermittlng des richtigen Scalierungsfactors 
    boundingBox = getBoundingBox()
    scalefactor = getScalingFactor(boundingBox[1])
    scalingMatrix = matrix([[scalefactor,0,0,0],[0,scalefactor,0,0],[0,0,scalefactor,0],[0,0,0,1]])
    tranformObject(scalingMatrix,objectPoints)
    boundingBox = getBoundingBox()

    scaleAndTranslate = matrix([[WIDTH/2,0,0,WIDTH/2],[0,WIDTH/2,0,HEIGHT/2],[0,0,WIDTH/2,0],[0,0,0,1]])
    tranformObject(scaleAndTranslate,objectPoints)

    



    # create main window
    mw = Tk()

    # create and position canvas and buttons
    cFr = Frame(mw, width=WIDTH, height=HEIGHT, relief="sunken", bd=1)
    cFr.pack(side="top")
    can = Canvas(cFr, width=WIDTH, height=HEIGHT)
    can.pack()
    bFr = Frame(mw)
    bFr.pack(side="left")
    bRotYn = Button(bFr, text="<-", command=rotYn)
    bRotYn.pack(side="left")
    bRotYp = Button(bFr, text="->", command=rotYp)
    bRotYp.pack(side="left")
    eFr = Frame(mw)
    eFr.pack(side="right")
    bExit = Button(eFr, text="Quit", command=(lambda root=mw: quit(root)))
    bExit.pack()


    # draw points
    draw(copyPoints(objectPoints))

    # start
    mw.mainloop()
    
