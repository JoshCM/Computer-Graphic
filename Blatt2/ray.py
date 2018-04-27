from vector import Vector
from point import Point


class Ray:
	def __init__(self, origin, direction):
		self.origin = origin
		self.direction = direction.normalize()

	def __repr__(self):
		return repr(origin)+repr(direction)

	def pointAtParameter(self, t):
		if t < 0:
			raise ValueError("Strahl darf nur nach vorne gehen!")
		pap = self.origin.array + self.direction.scale(t).array
		return Point(pap[0],pap[1],pap[2])

	def __repr__(self):
		return repr(self.origin)+repr(self.direction)

def main():
	p = Point(0,0,0)
	v = Vector(0,0,1)
	r = Ray(p,v)
	print(r)

if __name__ == '__main__':
	main()

