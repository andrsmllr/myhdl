#!/bin/python
#
# File:   dds.py
# Date:   2016-05-22
# Author: Andreas Mueller
#
# Description: MyHDL description of a generic DDS solution.
#

import myhdl as hdl
from myhdl import intbv, always, always_comb, always_seq, instance
from math import sin

@hdl.block
def dds(clk_i, rst_i, ena_i, phase_i, phase_load_i, phase_incr_i, di_o, dq_o, WIDTH_PHASE_ACC, WIDTH_WAVE_ROM, WAVE_FUNC):
  """Parameterizable DDS solution."""

  phase_acc = hdl.Signal(intbv(0)[WIDTH_PHASE_ACC:])
  di = hdl.Signal(intbv(0)[WIDTH_WAVE_ROM:])
  dq = hdl.Signal(intbv(0)[WIDTH_WAVE_ROM:])

  wave_rom_content = []

  @always_comb
  def dds_wave_rom():
    """Read the waveform look-up table."""
    di.next = wave_rom_content[int(phase_acc.val)]
    dq.next = wave_rom_content[int(phase_acc.val + 2**WIDTH_PHASE_ACC/4)]

  @always_seq(clk_i.posedge, reset=rst_i)
  def dds_phase_acc():
    """Calculate the phase accumulator."""
    if ena_i:
      if phase_load_i:
        phase_acc.next = phase_i.val
      else:
        phase_acc.next = phase_acc.val + phase_incr_i.val

  @always_seq(clk_i.posedge, reset=rst_i)
  def dds_logic():
    """Create DDS output."""
    if ena_i:
      di_o.next = di
      dq_o.next = dq

#  dds_wave_rom_inst = dds_wave_rom(di, dq)
#  dds_phase_acc_inst = dds_phase_acc()
#  dds_logic_inst = dds_logic()

#  return dds_wave_rom_inst, dds_phase_acc_inst, dds_logic_inst
  return dds_wave_rom, dds_phase_acc, dds_logic


WIDTH_PHASE_ACC = 12
WIDTH_WAVE_ROM = 10
WAVE_FUNC = sin
clk = hdl.Signal(bool(0))
rst = hdl.ResetSignal(val=1, active=1, async=False)
ena = hdl.Signal(bool(0))
phase = hdl.Signal(intbv(0)[WIDTH_PHASE_ACC:])
phase_load = hdl.Signal(bool(0))
phase_incr = hdl.Signal(intbv(0)[WIDTH_PHASE_ACC:])
di = hdl.Signal(intbv(0)[WIDTH_WAVE_ROM:])
dq = hdl.Signal(intbv(0)[WIDTH_WAVE_ROM:])

dds_top = dds(clk, rst, ena, phase, phase_load, phase_incr, di, dq, WIDTH_PHASE_ACC, WIDTH_WAVE_ROM, WAVE_FUNC)
#dds_top = hdl.toVerilog(dds, clk, rst, ena, phase, phase_load, phase_incr, di, dq, WIDTH_PHASE_ACC, WIDTH_WAVE_ROM, WAVE_FUNC)
dds_top.convert(hdl="Verilog")
dds_top.convert(hdl="VHDL")
