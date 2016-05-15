#!/bin/python
#
# File: conversion_to_hdl.py
# Date: 2016-05-15
# Author: Andreas Mueller
#
# Description: Example for the conversion from MyHDL to Verilog and VHDL.
#

from myhdl import *


def GenericCounter(clk_i, rst_i, ena_i, incr_i, count_o, MIN=None, MAX=None):
  """A generic up-down counter."""

  MIN = MIN or count_o.min
  MAX = MAX or count_o.max

  count = Signal(intbv(val=0, min=MIN, max=MAX))

  @always_seq(clk_i.posedge, reset=rst_i)
  def logic():
    if rst_i:
      count.next = 0
    elif ena_i:
      if incr_i:
        if count.val == MAX:
          count.next = MIN
        else:
          count.next = count.val + 1
      else:
        if count.val == MIN:
          count.next = MAX
        else:
          count.next = count.val - 1

  @always_comb
  def output():
    count_o.next = count

  return logic, output


if __name__ == "__main__":
  COUNT_MIN = -5
  COUNT_MAX = 11
  clk_i = Signal(bool(0))
  rst_i = ResetSignal(val=0, active=1, async=False)
  ena_i = Signal(bool(0))
  incr_i = Signal(bool(0))
  count_o = Signal(intbv(min=COUNT_MIN, max=COUNT_MAX))

  genCntr1 = toVHDL(GenericCounter, clk_i=clk_i, rst_i=rst_i, ena_i=ena_i, incr_i=incr_i, count_o=count_o)
  genCntr2 = toVerilog(GenericCounter, clk_i=clk_i, rst_i=rst_i, ena_i=ena_i, incr_i=incr_i, count_o=count_o)
