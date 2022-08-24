#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------
# point2D.py
# An "abstract" class defining a 2D point
#
# Author: Jorge Londoño
#-----------------------------------------------------------------------

import math

class Point2D:
    """Class representing points in the plane
    """

    def distance(self, other:'Point2D') -> float:
        """Computes the distance to other Point2D
        """
        return math.sqrt( (self.getX()-other.getX())**2 + (self.getY()-other.getY())**2 )
    
    def __abs__(self) -> float:
        """Returns the distance to the origin (magnitude)
        
        Not defined, must be implemented in subclasses
        """
        return None
    
    def angle(self) -> float:
        """Returns the angle to the x axis
        
        Not defined, must be implemented in subclasses
        """
        return None
    
    def getX(self) -> float:
        """Returns the x component
        
        Not defined, must be implemented in subclasses
        """
        return None

    def getY(self) -> float:
        """Returns the y component
        
        Not defined, must be implemented in subclasses
        """
        return None
    
    def __eq__(self, other:'Point2D') -> bool:
        """Returns True if self==other (or very close to)
        """
        if self.distance(other)<1E-15:
            return True
        return False