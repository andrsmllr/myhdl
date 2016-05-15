#!/bin/python
#
# File: bin2gray.py
# Date: 2016-04-01
# Author: Andreas Mueller
#
# Description: Example for MyHDL bit indexing from myhdl.org.
#

from myhdl import Signal, delay, Simulation, always_comb, instance, intbv, bin

def bin2gray(bin_i, gray_o, WIDTH):
    """Binary to gray encoder."""

    @always_comb
    def logic():
        for i in range(WIDTH):
            gray_o.next[i] = bin_i[i+1] ^ bin_i[i]

    return logic


# Dummy module defining the interface used during unit testing.
def bin2gray_dummy(B, G, width):
  """NOT IMPLEMENTED YET."""
  yield None


# Incorrect implementation for unit testing demo.
def bin2gray_incorrect(B, G, width):
  """INCORRECT, DEMO ONLY."""
  @always_comb
  def logic():
    G.next = B[0]

  return logic


def bin2gray_tb(WIDTH):
    """Testbench for bin2gray."""

    bin_i = Signal(intbv(0))
    gray_o = Signal(intbv(0))

    bin2gray_dut = bin2gray(bin_i=bin_i, gray_o=gray_o, WIDTH=WIDTH)

    @instance
    def stimulus():
        for i in range(2**WIDTH):
            bin_i.next = intbv(i)
            yield delay(10)
            print("bin_i {0} | gray_o {1}".format(bin(bin_i, WIDTH), bin(gray_o, WIDTH)))

    return bin2gray_dut, stimulus

if __name__ == "__main__":
  sim = Simulation(bin2gray_tb(WIDTH=3))
  sim.run()
