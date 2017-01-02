// File: dds.v
// Generated by MyHDL 1.0dev
// Date: Sun May 22 16:56:33 2016


`timescale 1ns/10ps

module dds (
    clk_i,
    rst_i,
    ena_i,
    phase_i,
    phase_load_i,
    phase_incr_i,
    di_o,
    dq_o
);
// Parameterizable DDS solution.

input clk_i;
input rst_i;
input ena_i;
input [11:0] phase_i;
input phase_load_i;
input [11:0] phase_incr_i;
output [9:0] di_o;
reg [9:0] di_o;
output [9:0] dq_o;
reg [9:0] dq_o;

reg [11:0] phase_acc;
wire [9:0] di;
wire [9:0] dq;




