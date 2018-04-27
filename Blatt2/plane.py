from point import Point
from vector import Vector
from ray import Ray

class Plane:
	def __init__(self,point,normal,color=(0,0,0)):
		self.point = point
		self.normal = normal.normalize()
		self.color = Vector(color[0],color[1],color[2])

	def intersectionParameter(self,ray):
		op = Vector(ray.origin,self.point)
		a = op.dot(self.normal)
		b = ray.direction.dot(self.normal)
		if b and -a/b >=0:
			return -a/b
		else:
			None

	def normalAt(self,p):
		return self.normal




def main():
	p = Plane(Point(0,0,0),Vector(0,0,1))
	r = Ray(Point(0,0,-1),Vector(0,0,1))
	a = p.intersectionParameter(r)
	print("intersectionParameter:"+str(a))

if __name__ == '__main__':
	main()

