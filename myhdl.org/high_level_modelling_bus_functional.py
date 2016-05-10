#!/bin/python
#
# File: high_level_modelling_bus_functional.py
# Date: 2016-05-09
# Author: Andreas Mueller
#
# Description: High level bus functional modelling with MyHDL.
#

import sys
from myhdl import *


T_9600 = int(1e9/9600)


def time():
  print("(time = {t})".format(t=now()))

def uart_tx(tx, data, duration=T_9600):
  """Simple UART transmitter procedure.
  tx       -- serial output data.
  data     -- input data byte to be transmitted.
  duration -- transmit bit duration.
  """

  print("-- Transmitting {0} -- ".format(hex(data)))
  print("TX: start bit")
  tx.next = 0
  yield delay(duration)

  for i in range(8):
    print("TX: {0}".format(bin(data[i])))
    tx.next = data[i]
    yield delay(duration)

  print("TX: stop bit")
  tx.next = 1
  yield delay(duration)


MAX_TIMEOUT = sys.maxint


def uart_rx(rx, data, duration=T_9600, timeout=MAX_TIMEOUT):
  """Simple UART receiver procedure.
  rx -- serial input data.
  data -- data received.
  duration -- receive bit duration
  """

  # Wait for start bit until timeout.
  yield rx.negedge, delay(timeout)
  if rx == 1:
    raise StopSimulation("RX timeout error")

  # Sample in middle of the bit duration.
  yield delay(duration/2)
  print("RX: start bit")

  for i in range(8):
    yield delay(duration)
    print("RX: {0}".format(bin(rx)))
    data[i] = rx

  yield delay(duration)
  print("RX: stop bit")
  # print("-- Received {0} --".format(hex(data)))
  print("-- Received 0x{0:02x} --".format(int(data)))


testvals = (0xC5, 0x3A, 0x4B)


def stimulus():
  tx = Signal(1)
  for val in testvals:
    txData = intbv(val)
    yield uart_tx(tx, txData)


def test():
  tx = Signal(1)
  rx = tx
  rxData = intbv(0)
  for val in testvals:
    txData = intbv(val)
    yield uart_rx(rx, rxData), uart_tx(tx, txData)


def testTimeout():
  tx = Signal(1)
  rx = Signal(1)
  rxData = intbv(0)
  for val in testvals:
    txData = intbv(val)
    yield uart_rx(rx, rxData, timeout=4*T_9600-1), uart_tx(tx, txData)


T_10200 = int(1e9/10200)


def testNoJoin():
  tx = Signal(1)
  rx = tx
  rxData = intbv(0)
  for val in testvals:
    txData = intbv(val)
    yield uart_rx(rx, rxData), uart_tx(tx, txData, duration=T_10200)


def testJoin():
  tx = Signal(1)
  rx = tx
  rxData = intbv(0)
  for val in testvals:
    txData = intbv(val)
    yield join(uart_rx(rx, rxData), uart_tx(tx, txData, duration=T_10200))
    print("Next byte")


sim1 = Simulation(stimulus())
sim2 = Simulation(test())
sim3 = Simulation(testTimeout())
sim4 = Simulation(testNoJoin())
sim5 = Simulation(testJoin())

#print("---- sim1 ----")
#sim1.run()

#print("---- sim2 ----")
#sim2.run()

#print("---- sim3 ----")
#sim3.run()

#print("---- sim4 ----")
#join(sim4.run())

print("---- sim5 ----")
sim5.run()


# Testing the join() function.

def fun1():
  print("Entered fun1")
  yield delay(100)
  print("Still in fun1")
  yield delay(1)
  print("Leaving fun1")

def fun2():
  print("Entered fun2")
  yield delay(10)
  print("Still in fun2")
  yield delay(10)
  print("Leaving fun2")

def testJoinFun():
  print("Start")
  yield join(fun1(), fun2())
  print("Done")

#sim0 = Simulation(testJoinFun())
#sim0.run()
