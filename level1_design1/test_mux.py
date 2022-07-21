# See LICENSE.vyoma for details

import cocotb
from cocotb.triggers import Timer

@cocotb.test()
async def test_mux_select_12(dut):
    """Test for inp12 output"""

    s = 12
    i12 = 2

    #input driving
    dut.sel.value = s
    dut.inp12.value = i12

    await Timer (2, units='ns')

    assert dut.out.value == i12, "Mux result is incorrect: select value = {s} obtained value = {op}, expected value = {out12}".format (s = (dut.sel.value), i12 = (dut.inp12.value), op=int(dut.out.value), out12=i12)

@cocotb.test()
async def test_mux_select_13(dut):
    """Test for inp13 output"""

    s = 13
    i13 = 2

    #input driving
    dut.sel.value = s
    dut.inp13.value = i13

    await Timer (2, units='ns')

    assert dut.out.value == i13, "Mux result is incorrect: select value = {s} obtained value = {op}, expected value = {out13}".format (s = (dut.sel.value), i13 = (dut.inp13.value), op=int(dut.out.value), out13=i13)

@cocotb.test()
async def test_mux_select_30(dut):
    """Test for inp30 output"""

    s = 30
    i30 = 2

    #input driving
    dut.sel.value = s
    dut.inp30.value = i30

    await Timer (2, units='ns')

    assert dut.out.value == i30, "Mux result is incorrect: select value = {s}, obtained value = {op}, expected value = {out30}".format (s = 30, i30 = (dut.inp30.value), op=int(dut.out.value), out30=i30)
