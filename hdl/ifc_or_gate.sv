//Bluespec ready-valid interface
module ifc_or_gate(
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
logic reg_a,reg_b,reg_y;
typedef enum logic[1:0] { IDLE, WAITING_FOR_B, COMPUTE, OUTPUT_READY } state_t;
state_t state_reg = IDLE;

always_ff @(posedge CLK) begin 
    if(!RST_N) begin 
        reg_a <= 0;
        reg_b <= 0;
        reg_y <= 0;
        state_reg <= IDLE;
        a_rdy <= 0;
        b_rdy <= 0;
        y_rdy <= 0;
    end else begin 
        if(state_reg == IDLE) begin
            y_rdy <= 0;
            a_rdy <= 1; 
            if(a_en) begin 
                reg_a <= a_data;
                state_reg <= WAITING_FOR_B;
            end  
        end else if (state_reg == WAITING_FOR_B) begin 
            b_rdy <= 1;
            a_rdy <= 0;
            if(b_en) begin 
                reg_b <= b_data;
                state_reg <= COMPUTE;
            end 
        end else if (state_reg == COMPUTE) begin 
            b_rdy <= 0;
            reg_y <= reg_a | reg_b;
            state_reg <= OUTPUT_READY;
        end else if (state_reg == OUTPUT_READY) begin 
            y_rdy <= 1;
            y_data <= reg_y;
            if(y_en) begin 
                state_reg <= IDLE;
            end 
        end 
    end 
end 
endmodule