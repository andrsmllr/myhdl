#!/bin/python
#
# File: counter.py
# Date: 2016-04-01
# Author: Andreas Mueller
#
# Description: Up counter with wrap around to demonstrate the modbv type.
#

from myhdl import *


def counter(clk, rst, count, WIDTH):
    """A synchronous up counter with WIDTH bits."""

    #count = modbv(0)[WIDTH:] # Local count variable not required, given as parameter.

    @always(clk.posedge, rst.posedge)
    def incrCount():
        if rst:
            count.next = 0
        else:
            count.next += 1

    return incrCount


def counter_tb(WIDTH):
    """Testbench for counter."""

    clk = Signal(intbv(0))
    rst = Signal(intbv(0))
    count = Signal(modbv(0)[WIDTH:])

    counter_dut = counter(clk, rst, count, WIDTH)

    @instance
    def clock():
        while True:
            clk.next = 1
            yield delay(10)
            clk.next = 0
            yield delay(10)

    @instance
    def stimulus():
        rst.next = 1
        yield delay(40)
        rst.next = 0
        yield delay(200)

    @instance
    def monitor():
        while True:
            yield clk.posedge
            #yield delay(1)
            print("{0} count : {1}".format(now(), bin(count, WIDTH)))

    return counter_dut, clock, stimulus, monitor


sim = Simulation(counter_tb(4))
sim.run(800)
