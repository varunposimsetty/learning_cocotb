import cocotb
from cocotb.triggers import Timer, RisingEdge
from cocotb_bus.drivers import BusDriver

def callback(actual_avlue) :
    assert actual_value - expected_value
@cocotb.test()
async def or_test(dut):
    global expected_value
    a=(0,0,1,1)
    b=(0,1,0,1)
    y=(0,1,1,1)
    dut.RST_N.value = 1
    await Timer(1,"ns")
    dut.RST_N.value = 0
    await Timer(1,"ns")
    await RisingEdge(dut.CLK)
    dut.RST_N.value = 1
    adrv=InputDriver(dut,'a',dut.CLK)
    bdrv=InputDriver(dut,'b',dut.CLK)
    OutputDriver(dut,'y',dut.CLK,cb_fn)


    for i in range(4):
        adrv(a[i])
        bdrv(b[i])
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
        self.bus.en.value = 0
        await NextTimeStep()
        
class OutputDriver(BusDriver):
    _signams=['rdy','en','data']
    def __init__(self,dut,name,clk,sb_callback):
        BusDriver.__init__(self,dut,name,clk)
        self.bus.en.value = 0
        self.clk=clk
        self.sb_callback = sb_callback

    async def driver_send(self,value,sync=True):
        if self.bus.rdy.value != 1:
            await RisingEdge(self.bus.rdy)
        self.bus.en =1
        #self.bus.data.value = value
        await ReadOnly()
        self.callback(self.bus.data.value)
        await RisingEdge(self.clk)
        self.bus.en.value = 0
        await NextTimeStep()