import cocotb
from cocotb.triggers import Timer, RisingEdge, FallingEdge, ClockCycles, ReadOnly, Combine, with_timeout, First
from cocotb.clock import Clock
from cocotb.binary import BinaryValue
import pytest

async def reset_dut(dut,duration_ns = 20):
    """
    Applies reset for a specific duration disenables the counter
    """
    dut.reset.value = 1
    dut.enable.value = 0
    await Timer(duration_ns,'ns')
    dut.reset.value = 0
    
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

# Having an issue - no error occurs when run individually but for the whole test bench the testcase seems to fail
@cocotb.test()
async def test_sequential_counting(dut):
    cocotb.log.info("="*60)
    cocotb.log.info("Test 6")
    cocotb.log.info("="*60)
    cocotb.start_soon(Clock(dut.clk,10,'ns').start())
    await reset_dut(dut)

    dut.enable.value = 1
    #await RisingEdge(dut.clk)
    cocotb.log.info("Counter Enabled")
    cocotb.log.info("")

    cocotb.log.info("Verifiying the proper increment of the counter")

    for exp_count in range(10):
        await RisingEdge(dut.clk)
        actual_count = dut.count.value.integer

        cocotb.log.info(
            f"Cycle {exp_count}:"
            f"count {actual_count}"
            f"(0b{dut.count.value.binstr}),"
            f"0x{actual_count:X})"
        )

        assert actual_count == exp_count, f"Expected count is {exp_count} got {actual_count}"

    cocotb.log.info("")
    cocotb.log.info("Test Passed")

@cocotb.test()
async def test_value_format(dut):
    cocotb.log.info("="*60)
    cocotb.log.info("Test 7")
    cocotb.log.info("="*60)
    cocotb.start_soon(Clock(dut.clk,10,'ns').start())
    await reset_dut(dut)
    dut.enable.value = 1
    test_values = [0,5,10,15]
    cocotb.log.info("")
    cocotb.log.info("Raeding the count value in different formats")
    cocotb.log.info("")

    for target in test_values:
        while dut.count.value.integer < target:
            await RisingEdge(dut.clk)

            count_val = dut.count.value
            cocotb.log.info(f"When count reaches {target}:")
            cocotb.log.info(f"  .value  =  {count_val}")
            cocotb.log.info(f"  .integer  =  {count_val.integer}")
            cocotb.log.info(f"  .binstr  =  {count_val.binstr}")
            cocotb.log.info(f"  .hex()  =  {hex(count_val.integer)}")
            cocotb.log.info(f"  .signed_integer  =  {count_val.signed_integer}")

        cocotb.log.info("Test Passed")
                            
@cocotb.test()
async def test_enable_transactions(dut):
    cocotb.log.info("="*70)
    cocotb.log.info("Test Started 8")
    cocotb.log.info("="*70)
    cocotb.start_soon(Clock(dut.clk,10,'ns').start())
    await reset_dut(dut)
    cocotb.log.info("")
    dut.enable.value = 1
    while dut.count.value.integer < 15:
        await RisingEdge(dut.clk)
    cocotb.log.info(f"  At maximum: count = {dut.count.value.integer}")
    assert dut.count.value.integer == 15, "Should reach 15"
    await RisingEdge(dut.clk)
    count_after_overflow = dut.count.value.integer
    cocotb.log.info(f"  After overflow: count = {count_after_overflow}")
    assert count_after_overflow == 0, \
        f"Counter should overflow to 0, got {count_after_overflow}"
    cocotb.log.info("")


# Having an issue - no error occurs when run individually but for the whole test bench the testcase seems to fail
@cocotb.test()
async def assertion_check(dut):
    cocotb.log.info("="*60)
    cocotb.log.info("Start Test 9")
    cocotb.log.info("="*60)
    cocotb.start_soon(Clock(dut.clk,10,'ns').start())
    await reset_dut(dut)
    dut.enable.value = 0
    await wait_cycles(dut,10)
    dut.enable.value = 1

    for i in range(35):
        await RisingEdge(dut.clk)
        count = dut.count.value.integer
        assert 0 <= count < 16, \
            f"Count {count} out of range [0,15]"
        assert count == i%16, \
            f"Cycle {i} expected count = {i%16} got {count}"
        assert count >= 0 and count < 16,\
            f"count must be in the range[0,15], got {count}"
        if i>0 and i<16: 
            assert count == i, f"count should increment by 1 each clock cycle"
        cocotb.log.info(f"Cycle {i}: count={count} - All assertions Passed")

@cocotb.test()
async def test_clock_cycles(dut):
    cocotb.log.info("="*60)
    cocotb.log.info("Test 10")
    cocotb.log.info("="*60)
    cocotb.start_soon(Clock(dut.clk,10,'ns').start())
    await reset_dut(dut,10)
    dut.enable.value = 1
    await RisingEdge(dut.clk)
    await ClockCycles(dut.clk,10)
    count = dut.count.value.integer
    assert count == 10, f"Expected count is 10 got {count}"
    cocotb.log.info("Test Passed")

@cocotb.test(skip=False)
async def test_Read_only(dut):
    cocotb.log.info("="*60)
    cocotb.log.info("Starting Test 11")
    cocotb.log.info("="*60)
    cocotb.start_soon(Clock(dut.clk,10,'ns').start())
    await reset_dut(dut,10)
    dut.enable.value = 1
    for _ in range(5):
        await RisingEdge(dut.clk)
        await ReadOnly()
        # ReadOnly waits for signals to settle i.e. no more RTL events are scheduled for the timestep.
        count = dut.count.value.integer
        cocotb.log.info(f"Cycle {_ +1} : count = {count} Sampled after ready only")
        assert count == _ + 1
    cocotb.log.info("Test Passed")

@cocotb.test()
async def test_combine(dut):
    cocotb.log.info("="*60)
    cocotb.log.info("Test 12")
    cocotb.log.info("="*60)
    cocotb.start_soon(Clock(dut.clk,10,'ns').start())
    await reset_dut(dut)
    dut.enable.value = 1
    while True:
        await RisingEdge(dut.clk)
        if dut.count.value.integer == 5:
            break 

    cocotb.log.info(f"count has reached 5")
    cocotb.log.info("Test Passed")

@cocotb.test()
async def test_with_timeout(dut):
    cocotb.log.info("="*70)
    cocotb.log.info("Test 13")
    cocotb.log.info("="*70)
    cocotb.start_soon(Clock(dut.clk,10,'ns').start())
    await reset_dut(dut)
    dut.enable.value = 1

    try : 
        for _ in range(15):
            result = await(with_timeout(RisingEdge(dut.clk),200,'ns'))
            #cocotb.log.info(f"{result}")
        cocotb.log.info("Completed within Timeout")
        
    except cocotb.result.SimTimeoutError:
        cocotb.log.error("TimeErrorOccured")
        raise
    cocotb.log.info("Test Passed")
    
@cocotb.test()
async def test_first_trigger(dut):
    cocotb.log.info("="*60)
    cocotb.log.info("Test 14")
    cocotb.log.info("="*60)
    cocotb.start_soon(Clock(dut.clk,10,'ns').start())
    await reset_dut(dut)
    dut.enable.value = 1
    trigger1 = ClockCycles(dut.clk,5)
    await ClockCycles(dut.clk,4)
    count = dut.count.value.integer
    cocotb.log.info(f"Count = {count} (0b{bin(count)[2:].zfill(4)})")
    cocotb.log.info(f"Count when condition is met is {count}")
    assert count == 3
    await wait_cycles(dut)
    val = dut.count.value.integer
    cocotb.log.info("Bit operations:")
    cocotb.log.info(f"count value is {val} and (0b{bin(val)})")
    cocotb.log.info(f"  Bit 0: {val & 1}")
    cocotb.log.info(f"  Bit 1: {(val >> 1) & 1}")
    cocotb.log.info(f"  Bit 2: {(val >> 2) & 1}")
    cocotb.log.info(f"  Bit 3: {(val >> 3) & 1}")
    cocotb.log.info("Test Passed")

