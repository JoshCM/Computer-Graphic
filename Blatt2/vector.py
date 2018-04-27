import numpy as np
from point import Point


class Vector:
	def __init__(self,x,y,z = None):
		if z != None:
			self.array = np.array([x,y,z])
		else:
			self.array = x-y

	def normalize(self):
		len = np.linalg.norm(self.array)
		self.array = self.array/len
		return self

	def scale(self,t):
		v = self.array * t
		return Vector(v[0],v[1],v[2])

	def dot(self,v2):
		return np.dot(self.array,v2.array)

	def cross(self,v2):
		a = np.cross(self.array,v2.array)
		return Vector(a[0],a[1],a[2])

	def negated(self):
		x = 0-self.array[0]
		y = 0-self.array[1]
		z = 0-self.array[2]
		return Vector(x,y,z)

	def __sub__(self,v2):
		v = self.array - v2.array
		return Vector(v[0],v[1],v[2])

	def __add__(self,v2):
		v = self.array + v2.array
		return Vector(v[0],v[1],v[2])

	def __repr__(self):
		return repr(self.array)

	def __mul__(self,t):
		return self.scale(t)


def main():
	p1,p2,p3 = Point(0,1,0),Point(1,0,0),Point(0,0,1)
	v1 = Vector(p1,p2)
	print("\nv1:"+repr(v1.array))
	v2 = Vector(0,1,0)
	print("\nv2:"+repr(v2.array))
	v3 = Vector(0,0,1)
	print("\nv3:"+repr(v3.array))


	print("\nnormale(v1)")
	v1.normalize()
	print(v1.array)

	print("\nv4 = v2 X v3")
	v4 = v2.cross(v3)
	print(v4.array)

	print("\nSkalarProdukt")
	print(v2.dot(v3))

	print("\nnegated(v4)")
	print(v4.negated())

	
if __name__ == '__main__':
	main()





