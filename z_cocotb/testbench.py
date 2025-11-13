
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge

async def run_reset_routine(dut):
    for _ in range(2):
        await RisingEdge(dut.clk)
    dut.reset.value = 0


@cocotb.test()
async def basic_count(dut):
    cocotb.start_soon(Clock(dut.clk,1,"ns").start())
    cocotb.start_soon(run_reset_routine(dut))
    dut.reset.value=1
    for cnt in range(50):
        await RisingEdge(dut.clk)
        dut_cnt = dut.count.value
        predicted_value = cnt%16
        #assert predicted_value == dut_cnt, "Failed"
        print(type(dut_cnt))
        #if (cnt > 2) :
        #    print(dut_cnt.signed_integer)
        



"""
from cocotb.binary import BinaryRepresentation, BinaryValue

bv1 = BinaryValue(10,8,True,BinaryRepresentation.TWOS_COMPLEMENT)
print(bv1.value)
bv2 = BinaryValue("XzZx0100",8,True,BinaryRepresentation.TWOS_COMPLEMENT)
print(bv2.binstr)
bv = BinaryValue(n_bits=10,bigEndian=False,binaryRepresentation=BinaryRepresentation.TWOS_COMPLEMENT)
bv.integer = -128
print(bv)


from cocotb.types import Bit,Logic,LogicArray
from cocotb.types.range import Range

a = Logic('1')
print(str(a))

a_arr = LogicArray("01Xz")
print(a_arr.binstr)

b_arr = LogicArray([0,True,"X"])
print(b_arr)

y = LogicArray("1001",Range(0,'to',3))
z = LogicArray("0100",Range(3, 'downto', 0))
print(y[0])
print(z[0])
print(z.binstr)
"""