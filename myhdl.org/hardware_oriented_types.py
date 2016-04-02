#!/bin/python
#
# File: hardware_oriented_types.py
# Date: 2016-04-01
# Author: Andreas Mueller
#
# Description: Demonstrate some hardware oriented types of MyHDL.
#

from myhdl import *

# Create an unconstrained intbv variable.
myInt1 = intbv(5)
print("min, max and len of myInt1")
print(myInt1.min)
print(myInt1.max)
print(len(myInt1))

# Create a intbv variable with initial value 0, minumum value 0 and maximum value 255.
myInt2 = intbv(val=0, min=0, max=255)
print("min, max and len of myInt2")
print(myInt2.min)
print(myInt2.max)
print(len(myInt2))

# Alternative, more HDL-like, syntax to define a intbv variable with restricted range.
myInt3 = intbv(0)[31:]
print("min, max and len of myInt3")
print(myInt3.min)
print(myInt3.max)
print(len(myInt3))
