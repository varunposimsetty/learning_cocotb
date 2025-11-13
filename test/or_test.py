import cocotb
from cocotb.triggers import Timer, RisingEdge
from cocotb_bus.drivers import BusDriver

@cocotb.test()
async def or_test(dut):
    a=(0,0,1,1)
    b=(0,1,0,1)
    y=(0,1,1,1)

    for i in range(4):
        dut.a.value = a[i]
        dut.b.value = b[i]
        await Timer(1,"ns")
        assert dut.y.value == y[i] , f"Error at iteration {i}"

class InputDriver(BusDriver):
    _signams=['rdy','en','data']
    def __init__(self,dut,name,clk):
        BusDriver.__init__(self,dut,name,clk)
        self.bus.en.value = 0
        self.clk=clk

    async def driver_send(self,value,sync=True):
        if self.bus.rdy.value != 1:
            await RisingEdge(self.bus.rdy)
        self.bus.en =1
        self.bus.data.value = value
        await ReadOnly()
        await RisingEdge(self.clk)
        self.bus.en = 0
            
