import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge, FallingEdge, ClockCycles
from cocotb.binary import BinaryValue
import random 

# async def is used to define coroutines 

async def reset_dut(dut, duration_ns = 20):
    """
    Reset Function pulls the reset low for duration_ns ns with a default duration of 20 ns.
    """
    cocotb.log.info("="* 60)
    cocotb.log.info("Starting RESET")
    cocotb.log.info("="*60)
    dut.RST_N.value = 0
    await Timer(duration_ns,"ns")
    dut.RST_N.value = 1
    await RisingEdge(dut.CLK)
    cocotb.log.info("RESET Complete")

async def wait_cycle(dut,num_cycles=10):
    """
    Wait for num_cycles # of CLK cycles
    """
    await ClockCycles(dut.CLK,num_cycles)

def generate_clock(dut,clock_period=10):
    """
    Generating a clock with a clock period of clock_period ns 
    Returns the clock object
    """
    clock = Clock(dut.CLK,clock_period,"ns")
    cocotb.start_soon(clock.start())
    return clock 

async def check_sys_state(dut):
    actual_y_data = dut.y_data.value
    cocotb.log.info(f"a_data : {dut.a_data.value} b_data : {dut.b_data.value} y_data : {dut.y_data.value}")


@cocotb.test()
async def ifc_or_test(dut):
    cocotb.log.info("*"*60)
    # starting the clock
    period = 5
    clk = generate_clock(dut,period)
    cocotb.log.info(f"Started toggling the clock at a clock period of {period} ns")
    cocotb.log.info("*"*60)
    # Reset
    await reset_dut(dut,10)
    #cocotb.log.info("Test 1 : Basic Test")
    #await Timer(5,"ns")
    #await FallingEdge(dut.CLK)
    await wait_cycle(dut,5)
    cocotb.log.info(f"RST_N value is {dut.RST_N.value}")
    #dut.RST_N.value = 0
    cocotb.log.info("y_rdy is %s", dut.y_rdy.value)
    assert dut.y_rdy.value == 0
    dut.a_en.value = 1
    dut.a_data.value = 0
    await wait_cycle(dut,10)
    dut.b_en.value = 1
    dut.b_data.value = 1
    #await wait_cycle(dut,50)
    await RisingEdge(dut.y_rdy)
    cocotb.log.info(dut.y_data.value.binstr)
    await Timer(1,'ns')
    assert int(dut.y_data.value) == 1
    dut.y_en.value = 1
    await check_sys_state(dut)
    
    

    