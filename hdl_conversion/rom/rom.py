#!/bin/python
#
# File:   rom.py
# Date:   2016-05-24
# Author: Andreas Mueller
#
# Description: MyHDL description of a ROM.
#


import myhdl as hdl
from myhdl import always, Signal, intbv, toVerilog, toVHDL
import math


# Add block decorator for MyHDL 1.0.
#@block
def rom(clk, addr, data, content):
  """A ROM."""

  @always(clk, addr)
  def logic():
    data.next = content[int(addr.val)]

  return logic


ADDR_BITS = 8
DATA_BITS = 8
content = tuple([
  int(2**DATA_BITS*(math.sin(2*math.pi*i/(2**ADDR_BITS))+1))
  for i in range(2**ADDR_BITS)
])
clk = Signal(bool(0))
addr = Signal(intbv(0)[ADDR_BITS:])
data = Signal(intbv(0)[DATA_BITS:0])

# Add code below for MyHDL 0.9.
rom_toVerilog = toVerilog(rom, clk, addr, data, content)
rom_toVHDL = toVHDL(rom, clk, addr, data, content)

# Add code below for MyHDL 1.0.
#myRom = rom(clk, addr, data, content)
#toVerilog(myRom)
#toVHDL(myRom)
