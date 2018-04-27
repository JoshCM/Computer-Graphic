from vector import Vector
from point import Point
from ray import Ray
import math

class Camera:
	def __init__(self,e,c,up,fov,wRes,hRes):
		self.e = e
		self.c = c
		self.f = Vector(c,e).normalize()
		self.s = self.f.cross(up).normalize()
		self.u = self.s.cross(self.f)
		self.up = up

		self.fov = fov
		self.alpha = fov/2.0

		self.wRes = wRes	
		self.hRes = hRes
		self.asprat = wRes/hRes

		self.height = 2* math.tan(self.alpha)
		self.width = self.asprat * self.height

		self.pwidth = self.width/(wRes-1)
		self.pheight = self.height/(hRes-1)

	def calcRay(self,x,y):
		xcomp = self.s.scale(x*self.pwidth - self.width/2)
		ycomp = self.u.scale(y*self.pheight - self.height/2)
		return Ray(self.e,self.f+xcomp+ycomp)

def main():
	c = Camera(Point(0,1.8,10),Point(0,3,0),Vector(0,1,0),45,400,400)
	print(c.f)
	print(c.u)
	print(c.s)
	print(c.height)
	print(c.width)
	print(c.pheight)
	print(c.pwidth)
	print(c.calcRay(0.0,0.0))
	print(c.calcRay(50, 50))
	print(c.calcRay(400.0,400.0))

if __name__ == '__main__':
	main()
