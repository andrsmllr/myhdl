#!/bin/python
#
# File: rtl_modelling_comb.py
# Date: 2016-04-17
# Author: Andreas Mueller
#
# Description: Recommended combinatorial RTL modelling constructs of MyHDL.
#

from myhdl import * # Signal, Simulation, delay, always_comb
from random import randrange


def Mux(d1, d2, q, s):
  """Multiplexer example using the combinatorial logic template of myhdl.org."""

  @always_comb
  def muxLogic():
    if s == 1:
      q.next = d2;
    else:
      q.next = d1;

  return muxLogic


def test():
  print("d1 d2 q s")
  for i in range(8):
    d1.next, d2.next, s.next = randrange(8), randrange(8), randrange(2)
    yield delay(10)
    print("b{0} b{1} b{2} b{3}".format(bin(d1, 3), bin(d2, 3), bin(q, 3), bin(s, 1)))


d1, d2, q, s = [Signal(intbv(0)) for i in range(4)]
mux1 = Mux(d1, d2, q, s)
test1 = test()
sim = Simulation(mux1, test1)
sim.run()
