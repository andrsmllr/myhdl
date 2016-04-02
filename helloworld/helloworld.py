from myhdl import Signal, delay, instance, always, now, Simulation, toVHDL

def ClkDriver(clk):
    """A clock driver."""

    halfPeriod = delay(10)

    @always(halfPeriod)
    def driveClk():
        clk.next = not clk

    return driveClk


def GenericClkDriver(clk, period=20):
    """A generic clock driver."""

    lowTime = int(period/2)
    highTime = period - lowTime

    @instance
    def driveClk():
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


clk1 = Signal(bool(0))
clkdriver_inst1 = ClkDriver(clk1)
helloworld_inst1 = HelloWorld(clk1)
sim1 = Simulation(clkdriver_inst1, helloworld_inst1)
sim1.run(50)

clk2 = Signal(0)
clkdriver_inst2 = GenericClkDriver(clk2)
helloworld_inst2 = GenericHello(clk2, "you there")
sim2 = Simulation(clkdriver_inst2, helloworld_inst2)
sim2.run(50)

greet = greetings()
sim3 = Simulation(greet)
sim3.run(50)
