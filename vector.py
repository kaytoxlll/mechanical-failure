# Copyright (C) 2012 Bailey Mihajlich
# Licensed under the GNU GPL v.2
# See license.txt for licence information

"""Special credit for the code in this class goes to Will McGugan,
author of "Game Development with Python and Pygame", I just
rewrote it here to get a better understanding of vectors in
game mechanics, and to comment. Original Vector2 class published
under the New BSD License.
"""

import math
import pygame

class Vector(object):
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __str__(self):
        return "(%s, %s)"%(self.x, self.y)

    @classmethod
    def from_points(cls, p1, p2):
        """calling convention: vector = Vector.from_points(p1 ,p2)
        where x and y are tuple points: p1 = (x,y)
        cls = self (more or less)
        Returns a Vector
        """
        return cls(p2[0]-p1[0], p2[1]-p1[1])

    def as_tuple(self):
        """Returns the points as a Python sequence length 2
        """
        return (self.x, self.y)

    def get_magnitude(self):
        """Returns the length of the vector
        """
        return math.sqrt(self.x**2 + self.y**2)

    def normalize(self):
        """ Sets x and y to have a magniture of 1
        """
        magnitude = self.get_magnitude()
        if magnitude == 0:
            return self
        self.x /= magnitude
        self.y /= magnitude
        return self

    def __add__(self, rhs):
        """Adds two vectors, using operator overloading
        example: vec3 = vec1 + vec2
        Returns a Vector
        """
        return Vector(self.x + rhs.x, self.y + rhs.y)

    def __sub__(self, rhs):
        """Subtract two vectors (see 'add')
        """
        return Vector(self.x - rhs.x, self.y - rhs.y)

    def __neg__(self):
        """Returns the opposite vector: -(1,1) = (-1,-1)
        """
        return Vector(-self.x, -self.y)

    def __mul__(self, scalar):
        """Returns the vector multiplied by the single number
        """
        return Vector(self.x*scalar, self.y*scalar)

    def __div__(self, scalar):
        """Returns the vector divided by the scalar
        """
        return Vector(self.x/scalar, self.y/scalar)

#test
"""
vec1 = Vector(25, 10)
print "vec1 =", vec1
vec2 = Vector.from_points((25,10), (30,15))
print 'vec2 =', vec2
print 'vec1 magnitude =', vec1.get_magnitude()
vec1.normalize()
print 'vec1 normalized =', vec1
print 'vec1 + vec2 =', vec1+vec2
print 'vec2 - vec2 =', vec1-vec2
print '-vec1 =', -vec1
print 'vec1 * 10 =', vec1*10
print 'vec1 / 2 =', vec1/2
"""
