module counter(
    input logic clk,
    input logic reset,
    input logic enable,
    output logic[3:0] count
);

initial begin 
    $dumpfile("counter_waves.vcd");
    $dumpvars;
end 

always_ff @(posedge clk or posedge reset) begin 
    if(reset) begin 
        count <= 0;
    end else begin 
        if(enable) begin 
            count <= count + 1;
        end 
    end 
end 
endmodule