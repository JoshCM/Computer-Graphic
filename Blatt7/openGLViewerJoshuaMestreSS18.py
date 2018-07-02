from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from OpenGL.arrays import vbo
import numpy as np
import sys
import math
import os

EXIT = -1
FIRST = 0
WIDTH = 500 
HEIGHT = 500

FACES = []
VERTICIES = []
NORM = []
POINTS = []
MITTELPUNKT = None
VBO = "Hallo"
ZOOM = 0
rotStartP = 0
transStartP = 0
actOri = np.matrix([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]])
angle = 0
doRotation = False
doTranslate = False
xtrans = ytrans = 0
scaleFactor = 0
axis = np.array([.0,.0,.0])
ortho = True
ObjectColor = (1.0,1.0,1.0,1.0)
lightPos = [0.0,-1000.0,100.0]
shadow = False
objMin = []


def init(width, height):
    global ObjectColor,lightPos
    """ Initialize an OpenGL window """
    glClearColor(0.0, 0.0, 1.0, 1.0)  # background color
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_NORMALIZE)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0,GL_POSITION,lightPos)
    
    #glEnable(GL_CULL_FACE)
    #glPolygonMode(GL_FRONT, GL_LINE)

    glMaterialfv(GL_FRONT_AND_BACK,GL_AMBIENT_AND_DIFFUSE,ObjectColor)
    glMatrixMode(GL_PROJECTION)  # switch to projection matrix
    glLoadIdentity()  # set to 1
    glOrtho(-1.5, 1.5, -1.5, 1.5, 0.1, 100.0)  # multiply with new p-matrix
    glMatrixMode(GL_MODELVIEW)  # switch to modelview matrix

def rotate(angle,axis):
    c,mc = math.cos(angle),1-math.cos(angle)
    s = math.sin(angle)
    l = math.sqrt(np.dot(axis,axis))
    if l == 0:
        l = 1.0
    x,y,z = axis/l
    r = np.matrix([[x*x*mc+c, x*y*mc-z*s, x*z*mc+y*s, 0],[x*y*mc+z*s, y*y*mc+c, y*z*mc-x*s, 0],[x*z*mc-y*s, y*z*mc+x*s, z*z*mc+c, 0],[0 ,0 , 0, 1]])
    return r.transpose()

def display():
    """ Render all objects"""
    global VBO,MITTELPUNKT,scaleFactor,axis,angle,doRotation,ortho,xtrans,ytrans,ztrans,shadow,lightPos

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # clear screen
    glMaterialfv(GL_FRONT_AND_BACK,GL_AMBIENT_AND_DIFFUSE,ObjectColor)

    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    
    VBO.bind()
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)

    if shadow:
        shadowMatrix = [1.0, 0, 0, 0, 0, 1.0, 0, -1.0/lightPos[1], 0, 0, 1.0, 0, 0, 0, 0, 0]

        glPushMatrix() # save state
        glTranslatef(0.0,objMin[1],0.0)#basis des objects auf der y ebene
        glTranslatef(lightPos[0],lightPos[1],lightPos[2]) # translate back
        glMultMatrixf(shadowMatrix) # project object
        glTranslatef(-lightPos[0], -lightPos[1], -lightPos[2]) # move light to origin
        glTranslatef(0.0,-objMin[1],0.0)#basis des objects auf der y ebene
        glColor3fv([0.0,0.0,0.0])
        glDisable(GL_LIGHTING)
        glDisable(GL_DEPTH_TEST)
        glDrawArrays(GL_TRIANGLES, 0, len(POINTS))
        glEnable(GL_LIGHTING)
        glEnable(GL_DEPTH_TEST)
        glPopMatrix()
        glVertexPointer(3, GL_FLOAT, 24, VBO)
        glNormalPointer(GL_FLOAT, 24, VBO+12)
        


    # Set camera
    glLoadIdentity()
    gluLookAt(0,0,4, 0,0,0, 0,1,0)

    # Interaction
    glTranslate(float(xtrans)/(WIDTH/2.0),float(ytrans)/(HEIGHT/2.0),0)
    glMultMatrixf((actOri*rotate(angle,axis)).tolist())
    
    # Normilization
    glScale(scaleFactor, scaleFactor, scaleFactor)
    glTranslate(-MITTELPUNKT[0], -MITTELPUNKT[1], -MITTELPUNKT[2])
    
    # call OpenGL draw
    glVertexPointer(3, GL_FLOAT, 24, VBO)
    glNormalPointer(GL_FLOAT, 24, VBO+12)
    glDrawArrays(GL_TRIANGLES, 0, len(POINTS))

    VBO.unbind()
    glDisableClientState(GL_VERTEX_ARRAY)
    glDisableClientState(GL_NORMAL_ARRAY)
    glutSwapBuffers()  # swap buffer


def reshape(width, height):
    """ adjust projection matrix to window size"""
    global WIDTH,HEIGHT

    WIDTH = width
    HEIGHT = height
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    if ortho: 
        if width <= height:
            glOrtho(-1.5, 1.5,
                    -1.5*height/width, 1.5*height/width,
                    0.1, 100.0)
        else:
            glOrtho(-1.5*width/height, 1.5*width/height,
                    -1.5, 1.5,
                    0.1, 100.0)

    else:
        gluPerspective(45,float(WIDTH)/HEIGHT,0.1,100)
   
    glMatrixMode(GL_MODELVIEW)
    
def keyPressed(key, x, y):
    """ handle keypress events """
    global ortho,ObjectColor,scaleFactor,shadow

    if key == chr(27):  # chr(27) = ESCAPE
        sys.exit()

    if key == "o":
        ortho = True
        reshape(WIDTH, HEIGHT)
    elif key == "p":
        ortho = False
        reshape(WIDTH, HEIGHT)
    elif key == "S":
        glClearColor(0.0,0.0,0.0,1.0)
    elif key == "s":
        ObjectColor = (0.0,0.0,0.0,1.0)
    elif key == "W":
        glClearColor(1.0,1.0,1.0,1.0)
    elif key == "w":
        ObjectColor = (1.0,1.0,1.0,1.0)
    elif key == "R":
        glClearColor(1.0,0.0,0.0,1.0)
    elif key == "r":
        ObjectColor = (1.0,0.0,0.0,1.0)
    elif key == "G":
        glClearColor(0.0,1.0,0.0,1.0)
    elif key == "g":
        ObjectColor = (0.0,1.0,0.0,1.0)
    elif key == "B":
        glClearColor(0.0,0.0,1.0,1.0)
    elif key == "b":
        ObjectColor = (0.0,0.0,1.0,1.0)
    elif key == "z":
        scaleFactor *= 1.1
    elif key == "Z":
        scaleFactor *= 0.9
    elif key == "h":
        shadow = not shadow

    glutPostRedisplay()

def projectOnSpher(x,y,r):
    global WIDTH, HEIGHT,xtrans,ytrans

    x,y = x-WIDTH/2.0, HEIGHT/2.0-y
    a = min(r*r,x**2+y**2)
    z = math.sqrt(r*r -a)
    l = math.sqrt(x**2+y**2+z**2)
    return np.array([x/l, y/l, z/l])

def mouse(button, state, x, y):
    global rotStartP, actOri, angle, doRotation,doTranslate,transStartP
    r = min(WIDTH,HEIGHT)/2.0
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            doRotation = True
            rotStartP = projectOnSpher(x,y,r)
        if state == GLUT_UP:
            doRotation = False
            actOri = actOri*rotate(angle,axis)
            angle = 0
    if button == GLUT_RIGHT_BUTTON:
        if state == GLUT_DOWN:
            doTranslate = True
            #transStartP = np.array([x-WIDTH/2.0, HEIGHT/2.0-y])
        if state == GLUT_UP:
            doTranslate = False

def mouseMotion(x, y):
    """ handle mouse motion """
    global angle, axis,scaleFactor,rotStartP,doTranslate,xtrans,ytrans,transStartP
    if doRotation:
        r = min(WIDTH,HEIGHT)/2.0
        moveP = projectOnSpher(x,y,r)
        dot = np.dot(rotStartP,moveP)
        if dot > 1:
            dot = 1
        elif dot < -1:
            dot = -1 
        angle = math.acos(dot)
        axis = np.cross(rotStartP,moveP)
    if doTranslate:
        xtrans = x-WIDTH/2.0
        ytrans = HEIGHT/2.0-y
    glutPostRedisplay()  

def menu_func(value):
    """ handle menue selection """
    print "menue entry ", value, "choosen..."
    if value == EXIT:
        sys.exit()
    glutPostRedisplay()

def calcNorms():
    global FACES, VERTICIES,NORM

    for i in range(len(VERTICIES)):
        NORM.append(np.array([0,0,0],'f'))

    for ele in FACES:
        index = [int(ele[0].split("/")[0])-1,int(ele[1].split("/")[0])-1,int(ele[2].split("/")[0])-1]
        vert1 = np.array(VERTICIES[index[0]],'f')
        vert2 = np.array(VERTICIES[index[1]],'f')
        vert3 = np.array(VERTICIES[index[2]],'f')

        vec1 = (vert2-vert1)
        vec2 = (vert3-vert1)

        norm = np.cross(vec1,vec2)

        for i in index:
            NORM[i] += norm
    
    for i in range(len(NORM)):
        ele = NORM[i]
        norm = np.linalg.norm(ele)
        if norm != 0.0:
            NORM[i] = (ele/norm).tolist()
        else:
            ele = [0.0,0.0,0.0]
    





def main():
    global VBO,MITTELPUNKT,scaleFactor,NORM,objMin
    with open(sys.argv[1]) as file:
        for line in file.readlines():
            if line.startswith("vn"):
                vn = [float(x) for x in line.split()[1:]]
                NORM.append(vn)
            elif line.startswith("v"):
                v = [float(x) for x in line.split()[1:]]
                VERTICIES.append(v)
            elif line.startswith("f"):
                f = [x for x in line.split()[1:]]
                FACES.append(f)

    calcedNorm = False
    if len(NORM) == 0:
        calcNorms()
        calcedNorm = True
    
    for ele in FACES:
        for e in ele:
            if calcedNorm:
                POINTS.append(VERTICIES[int(e.split("/")[0])-1] + NORM[int(e.split("/")[0])-1])
            else:
                POINTS.append(VERTICIES[int(e.split("/")[0])-1] + NORM[int(e.split("/")[2])-1])

    objMax = [max(POINTS, key=lambda x: x[0])[0], max(POINTS, key=lambda x: x[1])[1], max(POINTS, key=lambda x: x[2])[2]]
    objMin = [min(POINTS, key=lambda x: x[0])[0], min(POINTS, key=lambda x: x[1])[1], min(POINTS, key=lambda x: x[2])[2]]
    MITTELPUNKT = [(mi+ma)/2.0 for mi, ma in zip(objMax, objMin)]
    scaleFactor = 2/max([(ma-mi) for ma, mi in zip(objMax, objMin)])

    VBO = vbo.VBO(np.array(POINTS, 'f'))

    # Hack for Mac OS X
    cwd = os.getcwd()
    glutInit(sys.argv)
    os.chdir(cwd)

    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(WIDTH, HEIGHT)
    glutCreateWindow("beschissener Kack")

    glutDisplayFunc(display)  # register display function
    glutReshapeFunc(reshape)  # register reshape function
    glutKeyboardFunc(keyPressed)  # register keyboard function
    glutMouseFunc(mouse)  # register mouse function
    glutMotionFunc(mouseMotion)  # register motion function
    #glutCreateMenu(menu_func)  # register menue function

    #glutAddMenuEntry("First Entry", FIRST)  # Add a menu entry
    #glutAddMenuEntry("EXIT", EXIT)  # Add another menu entry
    #glutAttachMenu(GLUT_MIDDLE_BUTTON)  # Attach mouse button to menue
    init(500, 500)  # initialize OpenGL state

    glutMainLoop()  # start even processing


if __name__ == "__main__":
    main()
