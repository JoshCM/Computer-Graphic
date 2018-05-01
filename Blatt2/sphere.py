from point import Point
from vector import Vector
from ray import Ray

import math

class Sphere:
	def __init__(self,center,radius,color = (0,0,0), texture = None):
		self.center = center
		self.radius = radius
		self.color = Vector(color[0],color[1],color[2])
		self.texture = texture

	def intersectionParameter(self,ray):
		co = Vector(self.center,ray.origin)
		v = co.dot(ray.direction)
		discriminant = v*v - co.dot(co) +self.radius*self.radius
		if discriminant < 0:
			return None
		else:
			ip = v-math.sqrt(discriminant)
			if ip >= 0:
				return ip

	def normalAt(self,p):
		return Vector(p,self.center).normalize()

	def colorAt(self,p):
		return self.color


def main():
	p =Point(1,2,3)
	v = Vector(0,0,1)
	r = Ray(p,v)
	s = Sphere(Point(1,1,1),2)
	print(s.intersectionParameter(r))


if __name__ == '__main__':
	main()
