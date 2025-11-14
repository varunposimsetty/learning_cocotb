import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge, FallingEdge, ClockCycles
from cocotb.binary import BinaryValue
import random 

async def reset_dut(dut, duration_ns = 20):
    """
    Reset Function pulls the reset low for duration_ns ns
    """
    cocotb.log.info("="* 60)
    cocotb.log.info("Starting Reset Sequence")
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

async def generate_clock(dut,clock_period=10):
    """
    Generating a clock with a clock period of clock_period
    """
    clock = Clock(dut.CLK,clock_period,"ns")
    clock.start_soon(clock.start())

#async def check_sys_state(dut)

@cocotb.test()
async def ifc_or_test(dut):
    cocotb.log.info("*"*60)
    period = 5
    generate_clock(dut,period)
    cocotb.log.info("Started toggling the clock at a clock period of {period} ns")
    cocotb.log.info("*"*60)
    await reset_dut(dut,10)
    #cocotb.log.info("Test 1 : Basic Test")
    #await Timer(5,"ns")
    #await FallingEdge(dut.CLK)
    cocotb.log.info("RST_N value is %s",dut.RST_N.value)
    #dut.RST_N.value = 0
    cocotb.log.info("y_rdy is %s", dut.y_rdy.value)
    assert dut.y_rdy.value == 0

    