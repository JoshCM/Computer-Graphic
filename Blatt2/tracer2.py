from sphere import Sphere
from camera import Camera
from point import Point
from vector import Vector
from ray import Ray
from plane import Plane
from triangle import Triangle
from texture import CheckboardTexture
from PIL import Image

WIDTH = 400
HEIGHT = 400
BACKGROUND_COLOR = Vector(0,0,0)
LIGHTSOURCE = Point(30,30,10)
LIGHTCOLOR = Vector(255,255,255)
TEXTURE = CheckboardTexture()
C = Camera(Point(0,1.8,10),Point(0,3,0),Vector(0,1,0),45,WIDTH,HEIGHT)

s = Sphere(Point(-1.5,1.5,0),1.2,(255,0,0))
s2 = Sphere(Point(1.5,1.5,0),1.2,(0,255,0))
s3 = Sphere(Point(0,4,0),1.2,(0,0,255))
tri = Triangle(s.center,s2.center,s3.center,(255,255,0))
p = Plane(Point(0,-1,0),Vector(0,2,0),(100,100,100))
OBJECTS = [s,s2,s3,tri,p]
IMG = Image.new('RGB',(WIDTH,HEIGHT),"black")
MAXLEVEL = 5
SHADOWFACTOR = 0.3
	
def main():
	pixels = IMG.load()
	for x in range(WIDTH):
		for y in range(HEIGHT):
			ray = C.calcRay(x,HEIGHT-y)
			color = traceRay(0,ray)
			pixels[x,y] = (int(color.array[0]),int(color.array[1]),int(color.array[2]))
	IMG.show()

def traceRay(level,ray):
	hitPoint = intersect(level,ray)
	if hitPoint:
		return shade(level,hitPoint)
	return BACKGROUND_COLOR

def intersect(level,ray):
	maxdist = float("inf")
	print(level)
	if level == MAXLEVEL:
		return None
	else:
		hitpointData = None
		for object in OBJECTS:
				hitdist = object.intersectionParameter(ray)
				if hitdist:
					if hitdist < maxdist and hitdist > 0.01:
						maxdist = hitdist
						hitpoint = ray.pointAtParameter(hitdist)
						hitpointData = (object,hitpoint,hitdist,ray)
		return hitpointData

def shade(level, hitpointData):
	directColor = computeDirectLight(hitpointData)

	reflectedRay = computeReflectedRay(hitpointData)
	reflectedColor = traceRay(level+1,reflectedRay)

	return directColor + reflectedColor*0.2

def computeDirectLight(hitpointData):
	object = hitpointData[0]
	ray = hitpointData[3]
	l = Vector(LIGHTSOURCE,hitpointData[1]).normalize()
	n = hitpointData[0].normalAt(hitpointData[1])
	r = (n * 2 * n.dot(l) - l).normalize()
	hitdist = hitpointData[2]
	z = Vector(hitdist,hitdist,hitdist)
	s = shadow(Ray(hitpointData[1],l))
	if s:
		SHADOWFACTOR = 0.3
	else:
		SHADOWFACTOR = 1

	if type(object) is Plane:
		return ((TEXTURE.baseColorAt(hitpointData[1])-z) * 0.5 + LIGHTCOLOR *0.5*l.dot(n) + LIGHTCOLOR *0.2*(r.dot(ray.direction.negated()))**32)*SHADOWFACTOR
	else:
		return ((object.color-z) * 0.5 + LIGHTCOLOR *0.5*l.dot(n) + LIGHTCOLOR *0.2*(r.dot(ray.direction.negated()))**32)*SHADOWFACTOR
		

def shadow(ray):
	for object in OBJECTS:
		hitdist = object.intersectionParameter(ray)
		if hitdist:
			if hitdist > 0.01:
				return Vector(0,0,0)
	return None

def computeReflectedRay(hitpointData):
	n = hitpointData[0].normalAt(hitpointData[1])
	d = hitpointData[3].direction
	dr = d-n*2*n.dot(d)
	return Ray(hitpointData[1],dr)

if __name__ == '__main__':
	main()










