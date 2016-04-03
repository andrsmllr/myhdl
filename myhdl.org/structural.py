#!/bin/python
#
# File: structural.py
# Date: 2016-04-03
# Author: Andreas Mueller
#
# Description: Demonstration of structural design with MyHDL.
#

from myhdl import *
from random import randint


def comp1(clk, rst, di, do, INIT=0):
    """A simple component MyHDL module."""

    @always_seq(clk.posedge, rst)
    def logic():
        if rst:
            do.next = INIT
        else:
            do.next = do + di;

    return logic


def top(clk, rst, di, do, dataWidth=8, nComp1=4):
    """A top MyHDL module created from several component MyHDL  modules."""

    #clk = Signal(bool(0))
    #rst = Signal(bool(0))
    #data_i = [Signal(dataWidth) for k in range(nComp1)]
    #data_o = Signal(dataWidth)
    comps = [None for k in range(nComp1)]

    for k in range(nComp1):
        #comps[k] = comp1(clk, rst, data_i[k], data_o[k])
        comps[k] = comp1(clk, rst, di[k], do[k])

    return comps


def clkgen(clk):
    """A simple clock generator MyHDL module."""

    @instance
    def logic():
        while True:
            clk.next = 1
            yield delay(5)
            clk.next = 0
            yield delay(5)

    return logic


def rstgen(rst):
    """A simple reset generator MyHDL module."""

    @instance
    def logic():
        rst.next = 1
        yield delay(40)
        rst.next = 0
        yield delay(1000)

    return logic


def top_tb(dataWidth, nComp1):
    """A testbench for top."""

    clk = Signal(bool(0))
    rst = ResetSignal(bool(0), active=1, async=False)
    data_i = [Signal(dataWidth) for k in range(nComp1)]
    data_o = [Signal(dataWidth) for k in range(nComp1)]

    for k in range(nComp1):
        data_i[k] = intbv(randint(0,2**dataWidth-1))

    c = clkgen(clk=clk)
    r = rstgen(rst=rst)
    t = top(clk=clk, rst=rst, di=data_i, do=data_o, dataWidth=dataWidth, nComp1=nComp1)

    @instance
    def monitor():
        print("time | rst | " + ''.join(
          ["di[{0}] | do[{0}] | ".format(k) for k in range(nComp1)]
        ))
        while True:
            yield clk.posedge
            yield delay(0)
            print("{0} | {1} | ".format(now(), bin(rst)) + ''.join(
                ["{0} | {1} | ".format(bin(data_i[k]), bin(data_o[k])) for k in range(nComp1)]
            ))

    return c, r, t, monitor

# Run simulation.
tb = top_tb(8, 2)
sim = Simulation(tb)
sim.run(400)
