import cocotb
from cocotb.triggers import Timer, RisingEdge, FallingEdge, ClockCycles
from cocotb.clock import Clock

async def reset_dut(dut,duration_ns = 20):
    """
    Applies reset for a specific duration
    """
    dut.reset.value = 1
    await Timer(duration_ns,'ns')
    dut.reset.value = 0
    await RisingEdge(dut.clk)

async def wait_cycles(dut,num_cycles = 10):
    """
    Waiting for a specified number of clock cycles
    """
    await ClockCycles(dut.clk,num_cycles)
    
@cocotb.test()
async def test_reset_check(dut):
    cocotb.log.info("="*60)
    cocotb.log.info("Test 1 checking reset")
    cocotb.log.info("="*60)
    clock_period_ns = 10
    cocotb.log.info(f"Generating a clock with period = {clock_period_ns} ns")
    clock = Clock(dut.clk,clock_period_ns,'ns')
    cocotb.start_soon(clock.start())
    cocotb.log.info("")
    await reset_dut(dut,20)
    assert int(dut.count.value) == 0, f"counter value should be 0 as system holds reset"
    cocotb.log.info("Waiting for 100 ns")
    await Timer(100,"ns")
    count_value = dut.count.value
    cocotb.log.info(f"count.value = {count_value}")
    cocotb.log.info(f"cocotb.value.integer = {count_value.integer}")
    cocotb.log.info(f"count.value.binstr = {count_value.binstr}")
    assert int(dut.count.value) == 0, f"counter = 0 as enable is 0 counter doesn't increment"
    cocotb.log.info("Done with Test 1")

@cocotb.test()
async def test_counting(dut):
    cocotb.log.info("="*60)
    cocotb.log.info("Test 2 : Reset and Counting")
    cocotb.log.info("="*60)
    cocotb.start_soon(Clock(dut.clk,10,'ns').start())
    cocotb.log.info("clock started")
    cocotb.log.info("")
    await reset_dut(dut)

    dut.enable.value = 1
    cocotb.log.info("Counter enabled")
    cocotb.log.info("")

    for _ in range(10):
        await RisingEdge(dut.clk)
        count = dut.count.value.integer
        cocotb.log.info(f"The counter value is {count}")
    
    cocotb.log.info("")
    count_before_reset = dut.count.value.integer
    assert count > 0, f"Counter should have counted up"

    cocotb.log.info("Applying reset while the counter is operational")
    await reset_dut(dut,20)
    count_after_reset = dut.count.value.integer
    cocotb.log.info(f"Counter value after reset : {count_after_reset}")
    assert count_after_reset == 0,f"counter should be zero after reset got {count_after_reset}"
    cocotb.log.info("Done with Test 2")

@cocotb.test()
async def test_rising_and_falling_edges(dut):
    cocotb.log.info("="*60)
    cocotb.log.info("Test 3")
    cocotb.log.info("="*60)
    cocotb.start_soon(Clock(dut.clk,10,'ns').start())
    cocotb.log.info("clock started")
    cocotb.log.info("")
    await reset_dut(dut)
    dut.enable.value = 1
    cocotb.log.info("Counter Enabled")
    cocotb.log.info("")
    cocotb.log.info("Observing counter on Rising Edges i.e. right when the value changes")
    for _  in range(10):
        await RisingEdge(dut.clk)
        count = dut.count.value.integer
        cocotb.log.info(f"Rising edge { _ + 1}: count = {count} ")
    cocotb.log.info("")

    cocotb.log.info("Observing count on FallingEdge i.e. once the count value has stabilized")
    for _ in range(10):
        await FallingEdge(dut.clk)
        count = dut.count.value.integer
        cocotb.log.info(f"Falling Edger { _ + 1}: count = {count}")
    
    cocotb.log.info("")
    cocotb.log.info("Test 3 done")


@cocotb.test()
async def test_reset_timing(dut):
    cocotb.log.info("="*60)
    cocotb.log.info("Test 4")
    cocotb.start_soon(Clock(dut.clk,10,'ns').start())
    durations = [10,25,50,100,210,21,13,11]
    for duration in durations:
        cocotb.log.info(f"Testing reset with duration = {duration} ns")
        await reset_dut(dut,duration)

        assert dut.count.value.integer == 0, "Reset Failed"
        cocotb.log.info(f"Reset successful with duration of {duration} ns")
        cocotb.log.info("")
        dut.enable.value = 1
        await RisingEdge(dut.clk)
        await RisingEdge(dut.clk)
    cocotb.log.info("Test 4 done")
    cocotb.log.info("")

@cocotb.test()
async def test_enable_control(dut):
    cocotb.log.info("="*60)
    cocotb.log.info("Test 5")
    cocotb.log.info("="*60)
    cocotb.start_soon(Clock(dut.clk,10,'ns').start())
    cocotb.log.info("Clock Started")
    await reset_dut(dut)
    cocotb.log.info(f"Reset is {dut.reset.value}")
    cocotb.log.info("")
    cocotb.log.info("Disabling the counter")
    dut.enable.value = 0
    await RisingEdge(dut.clk)
    cocotb.log.info(f"Enable is  {dut.enable.value}")
    initial_count = dut.count.value.integer
    cocotb.log.info(f"Initial count = {initial_count}")
    await wait_cycles(dut,5)
    final_count = dut.count.value.integer
    cocotb.log.info(f"Value of count after 5 cycles is = {final_count}")
    assert initial_count == final_count, f"Counter value shouldn't change when disabled, It was {initial_count} and is {final_count}"
    cocotb.log.info("Counter correctly stays at 0 when disabled")
    dut.enable.value = 1
    await RisingEdge(dut.clk)
    cocotb.log.info(f"set the enable to {dut.enable.value}")
    count_before = dut.count.value.integer
    await wait_cycles(dut,10)
    count_after = dut.count.value.integer
    cocotb.log.info(f"count before = {count_before}")
    cocotb.log.info(f"count after = {count_after}")
    expected_increase = 10
    actual_increase = count_after - count_before
    assert actual_increase == expected_increase, f"The increase should be equal to {expected_increase}, but increased by {actual_increase}"
    cocotb.log.info(f"Counter correctly increased by {expected_increase}")
    cocotb.log.info("")
    cocotb.log.info("Test Passed")
    cocotb.log.info("")















    