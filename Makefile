SIM ?= icarus
TOPLEVEL_LANG ?= verilog

#VERILOG_SOURCES += $(PWD)/z_cocotb/dut.sv
VERILOG_SOURCES += $(PWD)/hdl/ifc_or_gate.sv
VERILOG_SOURCES += $(PWD)/wrapper/ifc_or_test.sv
#VERILOG_SOURCES += $(PWD)/hdl/or_gate.v
#VERILOG_SOURCES += $(PWD)/wrapper/or_test.v
TOPLEVEL = ifc_or_test
export PYTHONPATH := $(PWD)/test:$(PYTHONPATH)
#dut: 
#	$(MAKE) sim MODULE=testbench TOPLEVEL=dut
#include $(shell cocotb-config --makefiles)/Makefile.sim
or: 
	$(MAKE) sim MODULE=ifc_or_test_lecture TOPLEVEL=ifc_or_test
include $(shell cocotb-config --makefiles)/Makefile.sim
clean::
	rm -rf __pycache__ test/__pycache__
	rm -f modelsim.ini transcript *.xml *vcd *gtkw *.vvp *pyc 
