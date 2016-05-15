module dut_bin2gray;

  reg [`WIDTH-1:0] B;
  wire [`WIDTH-1:0] G;

  initial begin
    $from_myhdl(B);
    $to_myhdl(G);
  end

  bin2gray dut (
    .B(B),
    .G(G)
  );
  defparam dut.WIDTH = `WIDTH;

endmodule
