#!/bin/python
#
# File: high_level_modelling_mem.py
# Date: 2016-05-09
# Author: Andreas Mueller
#
# Description: High level modelling of memory with MyHDL.
#

import sys
from myhdl import *


class SparseMemoryError(Exception):
  pass


def sparseMemory(dout, din, addr, we, en, clk):
  """Sparse memory model based on a dictionary.
  Ports:
  dout -- data out
  din  -- data in
  addr -- address
  we   -- write enable
  en   -- interface enable
  clk  -- clock
  """

  memory = {}

  @always(clk.posedge)
  def access():
    if en:
      if we:
        memory[addr.val] = din.val
      else:
        try:
          dout.next = memory[addr.val]
        except KeyError:
          raise SparseMemoryError

  return access


class FifoError(Exception):
  pass


def fifo(dout, din, re, we, empty, full, clk, maxDepth=sys.maxint):
  """Synchronous FIFO model based on a list.
  Ports:
  dout -- data out
  din -- data in
  re -- read enable
  we -- write enable
  empty -- empty flag
  full -- full flag
  clk -- clock

  Parameters:
  maxDepth -- maximum FIFO depth, infinite by default
  """

  memory = []

  @always(clk.posedge)
  def access():
    if we:
      memory.insert(0, din.val)
    if re:
      try:
        dout.next = memort.pop()
      except IndexError:
        raise FifoError
    filling = len(memory)
    empty.next = (filling == 0)
    full.next = (filling == maxDepth)
    if filling > maxDepth:
      raise FifoError

  return access

