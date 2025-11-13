//Bluespec ready-valid interface
module or_gate(
    input  logic CLK,
    input  logic RST,
    input  logic a_data,
    input  logic a_en,
    output logic a_rdy,
    input  logic b_data,
    input  logic b_en,
    output logic b_rdy,
    output logic y_data,
    input  logic y_en,
    output logic y_ready

);

typedef enum logic[1:0] {IDLE,COMPUTE,OUTPUT} state_t;
state_t transaction := IDLE;
logic stored_a, stored_b;

always_ff @(posedge CLK) begin 
    if(RST) begin 
        
    end else begin 
        if(transaction == IDLE)begin 
            a_rdy <= 1;
            b_rdy <= 1;
            if(a_rdy && a_en) begin 
                stored_a <= a_data;
            end 
            if(b_rdy && b_en) begin 
                stored_b <= b_data;
            end 
        end 
    end

end



endmodule