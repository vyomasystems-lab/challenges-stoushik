# See LICENSE.vyoma for details

import cocotb
from cocotb.triggers import Timer
import random

@cocotb.test()
async def Fixed_Adder_test(dut):

    a = 10
    b = 6
    cin = 1

    #input driving
    dut.a.value = a
    dut.b.value = b
    dut.cin.value = cin

    await Timer (2, units='ns')

    assert dut.sum.value == a+b+cin, f"Adder result is incorrect: Obtained Output = {dut.sum.value}, Expected Output = "+str(a+b+cin)
