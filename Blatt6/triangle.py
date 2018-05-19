from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo
from numpy import array as npa
import sys,math

#points = [[-1,-0.5],[-0.75,0],[-0.5,-0.5],[-0.25,0],[0,-0.5],[0.25,0],[-0.25,0],[0,0.5],[0.25,0],[0.5,0.5],[0.75,0]]
points = [[-1,-0.5],[-0.75,0],[-0.5,-0.5],[-0.75,0],[-0.5,-0.5],[-0.25,0],[-0.5,-0.5],[-0.25,0],[0,-0.5],[-0.25,0],[0,-0.5],[0.25,0]]
vbo = vbo.VBO(npa(points,'f'))

def initGL(width,height):
    glClearColor(1.0,1.0,1.0,0.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1.5,1.5,-1.5,1.5,-1.0,1.0)
    glMatrixMode(GL_MODELVIEW)

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(.0,.0,.0)
    glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
    vbo.bind()
    glVertexPointerf(vbo)
    glEnableClientState(GL_VERTEX_ARRAY)
    glDrawArrays(GL_TRIANGLE_STRIP,0,len(points))
    vbo.unbind()
    glDisableClientState(GL_VERTEX_ARRAY)
    glFlush()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE|GLUT_RGB)
    glutInitWindowSize(500,500)
    glutCreateWindow("Hello World!")
    glutDisplayFunc(display)
    initGL(500,500)
    glutMainLoop()

if __name__ == '__main__':
    main()


