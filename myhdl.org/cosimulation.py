#!/bin/python
#
# File: cosimulation.py
# Date: 2016-05-13
# Author: Andreas Mueller
#
# Description: Cosimulation using Icarus Verilog in MyHDL.
#

from myhdl import *
import unittest
from unittest import TestCase
import os


cmd = "iverilog -o bin2gray -D WIDTH={0} bin2gray.v dut_bin2gray.v"

def bin2gray(B, G, WIDTH):
  os.system(cmd.format(WIDTH))
  return Cosimulation("vvp -m /home/andreas/git_others/myhdl/cosimulation/icarus/myhdl.vpi bin2gray", B=B, G=G)


# Testbench copied from bin2gray.py.
def bin2gray_tb(WIDTH):
    """Testbench for bin2gray."""

    bin_i = Signal(intbv(0))
    gray_o = Signal(intbv(0))

    bin2gray_dut = bin2gray(B=bin_i, G=gray_o, WIDTH=WIDTH)

    @instance
    def stimulus():
        for i in range(2**WIDTH):
            bin_i.next = intbv(i)
            yield delay(10)
            print("bin_i {0} | gray_o {1}".format(bin(bin_i, WIDTH), bin(gray_o, WIDTH)))

    return bin2gray_dut, stimulus


if __name__ == "__main__":
  sim = Simulation(bin2gray_tb(4))
  sim.run()
