#!/bin/python
#
# File:   dff.py
# Date:   2016-05-24
# Author: Andreas Mueller
#
# Description: MyHDL description of a D-Flipflop.
#


from myhdl import always_seq, Signal, ResetSignal, intbv, toVerilog, toVHDL


#@block
def dff(clk, rst, ce, d, q):
  """D-Flipflop."""

  @always_seq(clk.posedge, rst)
  def logic():
    if ce:
      q.next = d

  return logic


clk = Signal(bool(0))
rst = ResetSignal(0, active=1, async=True)
ce = Signal(bool(0))
d = Signal(bool(0))
q = Signal(bool(0))
#REG_WIDTH = 1
#d = Signal(intbv(0)[REG_WIDTH:])
#q = Signal(intbv(0)[REG_WIDTH:])

dff_toVerilog = toVerilog(dff, clk, rst, ce, d, q)
dff_toVHDL = toVHDL(dff, clk, rst, ce, d, q)
