PYTHON	= python3
PICKER 	= picker
NAME	= Adder


run:
	pytest --toffee-report -sv .

dut:
	$(PICKER) export --autobuild=true InstrUncache.sv -w InstrUncache.fst --sname InstrUncache --tdir picker_out_instruncache --lang python -e -c --sim verilator

clean:
	rm -rf UT_InstrUncache picker_out_instruncache reports
