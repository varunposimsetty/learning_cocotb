SIM ?= icarus
TOPLEVEL_LANG ?= verilog

VERILOG_SOURCES += $(PWD)/hdl/counter.sv
TOPLEVEL = counter  #name of the HDL module
MODULE = counter_test # name of the Python file  
TESTCASE = test_enable_control
export PYTHONPATH := $(PWD)/test:$(PYTHONPATH)

counter: 
	$(MAKE) sim MODULE=counter_test TESTCASE=test_enable_control TOPLEVEL=counter
include $(shell cocotb-config --makefiles)/Makefile.sim
clean::
	rm -rf __pycache__ test/__pycache__
	rm -f modelsim.ini transcript *.xml
