#!/bin/python
#
# File: helloworld.py
# Date: 2016-04-02
# Author: Andreas Mueller
#
# Description: Helloworld examples in MyHDL.
#

from sys import argv, exit
from myhdl import Signal, delay, instance, always, now, Simulation, toVHDL

def ClkDriver(clk):
    """A clock driver."""

    halfPeriod = delay(5)

    @always(halfPeriod)
    def driveClk():
        clk.next = not clk

    return driveClk


def GenericClkDriver(clk, period=10):
    """A generic clock driver with configurable period."""

    lowTime = int(period/2)
    highTime = period - lowTime

    @instance
    def driveClk():
        clk.next = 0
        while True:
            yield delay(lowTime)
            clk.next = 1
            yield delay(highTime)
            clk.next = 0

    return driveClk


def HelloWorld(clk):
    """MyHDL HelloWorld program."""

    #interval = delay(10);

    @always(clk.posedge)
    def sayHello():
        print("{0} Hello World!".format(now()))

    return sayHello


def GenericHello(clk, to="World"):
    """Generic MyHDL Hello program."""

    @always(clk.posedge)
    def sayHello():
        print("{0} Hello {1}!".format(now(), to))

    return sayHello


def greetings():
    clk1 = Signal(0)
    clk2 = Signal(0)

    clkdriver1 = GenericClkDriver(clk1) # Positional and default association.
    clkdriver2 = GenericClkDriver(clk=clk2, period=17) # Named association.
    hello1 = HelloWorld(clk=clk1) # Named and default association.
    hello2 = GenericHello(to="MyHDL", clk=clk2) # Named association.

    return [clkdriver1, clkdriver2, hello1, hello2]


if __name__ == "__main__":

  if len(argv) < 2:
    print("Usage: python helloworld.py {1,2,3}")
    exit()

  # The following conditional is required to avoid "Only one simulation instance
  # allowed" errors from MyHDL.
  if argv[1] ==  "1":
    clk1 = Signal(bool(0))
    clkdriver_inst1 = ClkDriver(clk1)
    helloworld_inst1 = HelloWorld(clk1)
    sim1 = Simulation(clkdriver_inst1, helloworld_inst1)
    sim1.run(50)
  elif argv[1] == "2":
    clk2 = Signal(0)
    clkdriver_inst2 = GenericClkDriver(clk2)
    helloworld_inst2 = GenericHello(clk2, "you there")
    sim2 = Simulation(clkdriver_inst2, helloworld_inst2)
    sim2.run(50)
  elif argv[1] == "3":
    greet = greetings()
    sim3 = Simulation(greet)
    sim3.run(50)

