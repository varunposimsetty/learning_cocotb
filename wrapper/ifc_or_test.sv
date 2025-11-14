module ifc_or_test(
    input  logic CLK,
    input  logic RST_N,
    input  logic a_data,
    input  logic a_en,
    input  logic b_data,
    input  logic b_en,
    input  logic y_en,
    output logic a_rdy,
    output logic b_rdy,
    output logic y_data,
    output logic y_rdy
);


ifc_or_gate dut (
    .CLK(CLK),
    .RST_N(RST_N),
    .a_data(a_data),
    .a_en(a_en),
    .b_data(b_data),
    .b_en(b_en),
    .y_en(y_en),
    .a_rdy(a_rdy),
    .b_rdy(b_rdy),
    .y_data(y_data),
    .y_rdy(y_rdy)
);

initial begin
        $dumpfile("ifc_waves.vcd");
        $dumpvars;
end

endmodule