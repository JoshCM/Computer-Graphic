from vector import Vector
from point import Point

class CheckboardTexture:
	def __init__(self):
		self.baseColor = Vector(255,255,255)
		self.otherColor = Vector(0,0,0)
		self.checkSize = 1

	def baseColorAt(self,p):
		v = Vector(p,Point(0,0,0))
		v = v * (1.0/self.checkSize)
		if (int(abs(v.array[0])+0.5)+int(abs(v.array[1])+0.5)+int(abs(v.array[2])+0.5))%2:
			return self.otherColor
		return self.baseColor
