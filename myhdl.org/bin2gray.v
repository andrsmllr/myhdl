module bin2gray(B, G,);

  parameter WIDTH = 8;
  input [WIDTH-1:0] B;
  output [WIDTH-1:0] G;
  reg [WIDTH-1:0] G;
  integer i;
  wire [WIDTH:0] extB;

  assign extB = {1'b0, B}; // zero-extend input.

  always @ (extB)
  begin
    for (i=0; i<WIDTH; i=i+1)
      G[i] <= extB[i+1] ^ extB[i];
  end

endmodule
