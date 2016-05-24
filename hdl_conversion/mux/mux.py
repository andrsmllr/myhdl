#!/bin/python
#
# File:   mux.py
# Date:   2016-05-24
# Author: Andreas Mueller
#
# Description: MyHDL description of a multiplexor.
#


from myhdl import always_comb, intbv, Signal, toVerilog, toVHDL


# Add block decorator for MyHDL 1.0.
#@block
def mux(s, da, db, q):
  """A multiplexor."""

  @always_comb
  def logic():
    if s:
      q.next = da
    else:
      q.next = db

  return logic


s = Signal(bool(0))
da = Signal(bool(0))
db = Signal(bool(0))
q = Signal(bool(0))

mux_toVerilog = toVerilog(mux, s, da, db, q)
mux_toVHDL = toVHDL(mux, s, da, db, q)
