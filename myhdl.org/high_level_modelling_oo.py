#!/bin/python
#
# File: high_level_modelling_oo.py
# Date: 2016-05-09
# Author: Andreas Mueller
#
# Description: Object oriented high level modelling with MyHDL.
#

from myhdl import *


def trigger(event):
  event.next = not event


class queue:
  def __init__(self):
    self.l = []
    self.sync = Signal(0)
    self.item = None
  def put(self, item):
    self.l.append(item)
    trigger(self.sync)
  def get(self):
    if not self.l:
      yield self.sync
    self.item = self.l.pop(0)


q = queue()


def Producer(q):
  yield delay(120)
  for i in range(5):
    print("{0}: PUT item {1}".format(now(), i))
    q.put(i)
    yield delay(max(5, 45-10*i))

def Consumer(q):
  yield delay(100)
  while 1:
    print("{0}: TRY to get item".format(now()))
    yield q.get()
    print("{0}: GOT item {1}".format(now(), q.item))
    yield delay(30)

def main():
  P = Producer(q)
  C = Consumer(q)
  return P, C


sim = Simulation(main())
sim.run()

