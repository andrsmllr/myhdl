#!/bin/python
#
# File: rtl_modelling_seq.py
# Date: 2016-04-17
# Author: Andreas Mueller
#
# Description: Recommended sequential RTL modelling constructs of MyHDL.
#

from myhdl import * # Signal, Simulation, delay, always_comb
from random import randrange


ACTIVE_LOW, INACTIVE_HIGH = 0, 1

def Inc(cnt, ena, clk, rst, n):
  """Increment with enable."""

  @always_seq(clk.posedge, reset=rst)
  def incLogic():
    if ena:
      cnt.next = (cnt + 1) % n

  @always(clk.posedge, rst.negedge)
  def incLogicAlt():
    if ena:
      cnt.next = (cnt + 1) % n

  return incLogic
  # return incLogicAlt


def testbench():
  cnt, ena, clk = [Signal(intbv(0)) for i in range(3)]
  rst = ResetSignal(0, active=ACTIVE_LOW, async=True)

  nbits = 3
  inc1 = Inc(cnt, ena, clk, rst, n=2**nbits)

  HALF_PERIOD = delay(10)

  @always(HALF_PERIOD)
  def clkGen():
    clk.next = not clk

  @instance
  def stimulus():
    rst.next = ACTIVE_LOW
    yield clk.negedge
    rst.next = INACTIVE_HIGH
    for i in range(12):
      ena.next = min(1, randrange(3))
      yield clk.negedge
    raise StopSimulation

  @instance
  def monitor():
    print("time rst cnt ena")
    # yield clk.posedge
    while 1:
      yield clk.posedge
      yield delay(1)
      print("{0} {1} {2} {3}".format(now(), bin(rst, 1), bin(cnt, nbits), bin(ena, 1)))

  return inc1, clkGen, stimulus, monitor


tb = testbench()
sim = Simulation(tb)
sim.run()
