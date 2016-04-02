#!/bin/python
#
# File: calculateHec.py
# Date: 2016-04-01
# Author: Andreas Mueller
#
# Description: Example for bit slicing in MyHDL from myhdl.org.
#

from myhdl import intbv, concat, Simulation, instance, delay, now
from random import randint

COSET = 0x55

def calculateHec(header):
    """Return hec for an ATM header.

    The hec polynomial is 1 + x + x^2 + x^8.
    """

    hec = intbv(0)
    for bit in header[32:]:
        hec[8:] = concat(hec[7:2], # Note that slicing direction is downward, as opposed to standard Python.
            bit ^ hec[1] ^ hec[7],
            bit ^ hec[0] ^ hec[7],
            bit ^ hec[7]
            )

    return hec ^ COSET

def calculateHec_tb(nRuns):
    """Testbench for calculateHec."""

    @instance
    def stimulus():
        for i in range(nRuns):
            header = intbv(randint(0, 2**32-1), 0, 2**32)
            hec = calculateHec(header)
            yield delay(10)
            print("{0} header 0x{1:08X} | hec 0x{2:02X}".format(now(), int(header), int(hec)))

    return stimulus


sim = Simulation(calculateHec_tb(3))
sim.run()
