import numpy as np

class Point:
	def __init__(self,x,y,z):
		self.array = np.array([x,y,z])

	def __repr__(self):
		return repr(self.array)

	def __sub__(self, p2):
		return self.array - p2.array

def main():
	p1 = Point(1,2,3)
	p2 = Point(1,2,3)

	print(p1-p2)


if __name__ == '__main__':
	main()
