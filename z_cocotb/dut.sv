module dut(
    input logic clk,
    input logic reset,
    input logic [3:0] count
);

logic [3:0] counter;

initial begin 
    $dumpfile("dump.vcd");
    $dumpvars(1,dut);
end 

always_ff @(posedge clk) begin
    if(reset) begin
        counter <= 0;
    end else begin  
        counter <= counter + 1;  
    end     
end
assign count = counter;

endmodule