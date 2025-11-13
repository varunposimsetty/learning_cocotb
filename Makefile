SIM ?= icarus
TOPLEVEL_LANG ?= verilog

#VERILOG_SOURCES = $(PWD)/z_cocotb/dut.sv
#VERILOG_SOURCES += $(PWD)/wrapper/or_test.v
TOPLEVEL = dut
export PYTHONPATH := $(PWD)/z_cocotb:$(PYTHONPATH)
dut: 
	$(MAKE) sim MODULE=testbench TOPLEVEL=dut
include $(shell cocotb-config --makefiles)/Makefile.sim
clean::
	rm -rf __pycache__ test/__pycache__
	rm -f modelsim.ini transcript *.xml
