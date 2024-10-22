runCK12:
	cl /EHsc main.cpp

compile:
	cl /LD /EHsc /I. /FeKeyUtils.dll KeyUtils.cpp

runPyK12:
	py fourq.test.py
