#!/bin/python
#
# File:   ram.py
# Date:   2016-05-24
# Author: Andreas Mueller
#
# Description: MyHDL description of a simple single-port RAM.
#


from myhdl import always, always_seq, Signal, intbv, toVerilog, toVHDL


# Add block decorator in MyHDL 1.0.
#@block
def ram(clk, we, addr, di, do):
  """RAM."""

  content = [0 for i in range(addr.min, addr.max)]

  @always(clk.posedge)
  def logic():
    if we:
      content[int(addr)] = di

    do.next = content[int(addr)]

  return logic


WORD_WIDTH = 16
ADDR_WIDTH = 8
clk = Signal(bool(0))
#rst = ResetSignal(bool(0))
we = Signal(bool(0))
addr = Signal(intbv(0)[ADDR_WIDTH:])
di = Signal(intbv(0)[WORD_WIDTH:])
do = Signal(intbv(0)[WORD_WIDTH:])

ram_toVerilog = toVerilog(ram, clk, we, addr, di, do)
ram_toVHDL = toVHDL(ram, clk, we, addr, di, do)
