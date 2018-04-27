from sphere import Sphere
from camera import Camera
from point import Point
from vector import Vector
from ray import Ray
from plane import Plane
from triangle import Triangle
from texture import CheckboardTexture
import numpy as np
from PIL import Image


WIDTH = 400
HEIGHT = 400
BACKGROUND_COLOR = Vector(0,0,0)
SPHEREHITCOLOR = (100,100,100)
LIGHTSOURCE = Point(30,30,10)
LIGHTCOLOR = Vector(255,255,255)
TEXTURE = CheckboardTexture()

def main():
	c = Camera(Point(0,1.8,10),Point(0,3,0),Vector(0,1,0),45,WIDTH,HEIGHT)
	objects = []
	s = Sphere(Point(-1.5,1.5,0),1.2,(255,0,0))
	s2 = Sphere(Point(1.5,1.5,0),1.2,(0,255,0))
	s3 = Sphere(Point(0,4,0),1.2,(0,0,255))
	tri = Triangle(s.center,s2.center,s3.center,(255,255,0))
	p = Plane(Point(0,-1,0),Vector(0,2,0),(100,100,100))
	objects.append(tri)
	objects.append(p)
	objects.append(s)
	objects.append(s2)
	objects.append(s3)

	img = Image.new('RGB',(WIDTH,HEIGHT),"black")
	pixels = img.load()
	raycounter = 0

	for x in range(WIDTH):
		for y in range(HEIGHT):
			ray = c.calcRay(x,HEIGHT-y)
			maxdist = float("inf")
			color = BACKGROUND_COLOR
			for object in objects:
				hitdist = object.intersectionParameter(ray)
				if hitdist:
					if hitdist < maxdist:
						hitpoint = ray.pointAtParameter(hitdist)
						l = Vector(LIGHTSOURCE,hitpoint).normalize()
						n = object.normalAt(hitpoint)
						r = (n * 2 * n.dot(l) - l).normalize()
						maxdist = hitdist
						z = Vector(hitdist,hitdist,hitdist)
						shadow = shade(Ray(hitpoint,l),objects)
						if shadow != None:
							if type(object) is Plane:
								color = (TEXTURE.baseColorAt(hitpoint)-z)*0.5
							else:
								color = (object.color-z)*0.5
						else:
							if type(object) is Plane:
								color = (TEXTURE.baseColorAt(hitpoint)-z)*0.5 + LIGHTCOLOR*0.5*l.dot(n) + LIGHTCOLOR * 0.2 *(r.dot(ray.direction.negated()))**25
							else:
								color = (object.color-z)*0.5 + LIGHTCOLOR*0.5*l.dot(n) + LIGHTCOLOR * 0.2 *(r.dot(ray.direction.negated()))**25

			pixels[x,y] = (int(color.array[0]),int(color.array[1]),int(color.array[2]))

	img.show()
def shade(ray,objects):
	for object in objects:
		hitdist = object.intersectionParameter(ray)
		if hitdist:
			if hitdist > 0.01:
				return Vector(0,0,0)
	return None



if __name__ == '__main__':
	main()













