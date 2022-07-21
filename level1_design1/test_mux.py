# See LICENSE.vyoma for details

import cocotb
from cocotb.triggers import Timer

@cocotb.test()
async def test_mux(dut):
    """Test for inp12 output"""

    s = 12
    i12 = 3

    #input driving
    dut.sel.value = 12
    dut.inp12.value = 3

    await Timer (2, units='ns')

    assert dut.out.value == inp12, "Mux result is incorrect: {s} + {i12} != {out}, expected value = {out12}".format (
        s = (dut.sel.value), i12 = (dut.inp12.value), op=int(dut.out.value), op=i12)
    )



    cocotb.log.info('##### CTB: Develop your test here ########')
