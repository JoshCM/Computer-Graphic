from ray import Ray
from point import Point
from vector import Vector

class Triangle:
	def __init__(self,a,b,c,color = (0,0,0)):
		self.a = a
		self.b = b
		self.c = c
		self.u = Vector(self.b,self.a)
		self.v = Vector(self.c,self.a)
		self.color = Vector(color[0],color[1],color[2])

	def intersectionParameter(self,ray):
		w = Vector(ray.origin,self.a)
		dv = ray.direction.cross(self.v)
		dvu = dv.dot(self.u)
		if dvu == 0.0:
			return None
		wu = w.cross(self.u)
		r = dv.dot(w)/dvu
		s = wu.dot(ray.direction)/dvu
		if 0 <= r and r<=1 and 0<=s and r+s<=1:
			ip = wu.dot(self.v)/dvu
			if ip >= 0:
				return ip
		else:
			return None

	def normalAt(self,p):
			return self.u.cross(self.v).normalize()
