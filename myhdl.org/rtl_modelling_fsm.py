#!/bin/python
#
# File: rtl_modelling_fsm.py
# Date: 2016-04-17
# Author: Andreas Mueller
#
# Description: Recommended finite state machine RTL modelling constructs of MyHDL.
#

from myhdl import * # Signal, Simulation, delay, always_comb
from random import randrange


ACTIVE_LOW = 0
FRAME_SIZE = 8
t_State = enum('SEARCH', 'CONFIRM', 'SYNC')

def FramerCtrl(SOF, state, syncFlag, clk, rst):
  """Framing control FSM."""

  index = Signal(0)

  @always_seq(clk.posedge, reset=rst)
  def FSM():
    index.next = (index + 1) % FRAME_SIZE
    SOF.next = 0

    if state == t_State.SEARCH:
      index.next = 1
      if syncFlag:
        state.next = t_State.CONFIRM
    elif state == t_State.CONFIRM:
      if index == 0:
        if syncFlag:
          state.next = t_State.SYNC
        else:
          state.next = t_State.SEARCH
    elif state == t_State.SYNC:
      if index == 0:
        if not syncFlag:
          state.next = t_State.SEARCH
      SOF.next = (index == FRAME_SIZE - 1)
    else:
      raise ValueError("Undefined state.")

  return FSM


def testbench():
  SOF = Signal(bool(0))
  syncFlag = Signal(bool(0))
  clk = Signal(bool(0))
  rst = ResetSignal(1, active=ACTIVE_LOW, async=True)
  state = Signal(t_State.SEARCH)

  framectrl = FramerCtrl(SOF, state, syncFlag, clk, rst)

  @always(delay(10))
  def clkgen():
    clk.next = not clk

  @instance
  def stimulus():
    for i in range(3):
      yield clk.posedge
    for n in (12, 8, 8, 4):
      syncFlag.next = 1
      yield clk.posedge
      syncFlag.next = 0
      for i in range(n-1):
        yield clk.posedge
    raise StopSimulation

  @always_seq(clk.posedge, reset=rst)
  def outputPrinter():
    print("{} {} {}".format(syncFlag, SOF, state))

  return framectrl, clkgen, stimulus, outputPrinter


tb_fsm = traceSignals(testbench)
sim = Simulation(tb_fsm)
sim.run()
