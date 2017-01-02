module tb_dds;

reg clk_i;
reg rst_i;
reg ena_i;
reg [10:0] phase_i;
reg phase_load_i;
reg [10:0] phase_incr_i;
wire [8:0] di_o;
wire [8:0] dq_o;

initial begin
    $from_myhdl(
        clk_i,
        rst_i,
        ena_i,
        phase_i,
        phase_load_i,
        phase_incr_i
    );
    $to_myhdl(
        di_o,
        dq_o
    );
end

dds dut(
    clk_i,
    rst_i,
    ena_i,
    phase_i,
    phase_load_i,
    phase_incr_i,
    di_o,
    dq_o
);

endmodule
