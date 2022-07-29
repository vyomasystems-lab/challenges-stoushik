# See LICENSE.vyoma for details

# SPDX-License-Identifier: CC0-1.0

import os
import random
from pathlib import Path

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge

@cocotb.test()
async def test_seq_bug1(dut):
    """Test for seq detection 1011011"""

    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock

    # reset
    dut.reset.value = 1
    await FallingEdge(dut.clk)  
    dut.reset.value = 0
    await FallingEdge(dut.clk)

    sequence = [1,0,1,1,0,1,1]
    output = [0,0,0,1,0,0,1]
    seq_seen_out = []
    
    print("\nInput sequence: ",end='   ')
    for i in sequence:
        print(i,end=' ')

    print("\nDesired seq_seen: ",end=' ')
    for i in output:
        print(i,end=' ')

    print("\nseq_seen Sequence: ",end='')
    
    for i in sequence:
        dut.inp_bit.value=i
        await FallingEdge(dut.clk)
        print(dut.seq_seen.value, end=' ')
        seq_seen_out.append(dut.seq_seen.value)

    print('\n')

    seq_seen_str = ""
    output_str = ""
    for i in seq_seen_out:
        seq_seen_str = seq_seen_str + str(i)
    for i in output:
        output_str = output_str + str(i)

    assert seq_seen_out == output, f"The output sequence is incorrent. It is not overlaping: Obtained Output = "+seq_seen_str+", Expected Output = "+output_str

    print('\n')


@cocotb.test()
async def test_seq_bug2(dut):
    """Test for seq detection 111011"""

    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock

    # reset
    dut.reset.value = 1
    await FallingEdge(dut.clk)  
    dut.reset.value = 0
    await FallingEdge(dut.clk)

    sequence = [1,1,1,0,1,1]
    output = [0,0,0,0,0,1]
    seq_seen_out = []
    
    print("\nInput sequence: ",end='   ')
    for i in sequence:
        print(i,end=' ')

    print("\nDesired seq_seen: ",end=' ')
    for i in output:
        print(i,end=' ')

    print("\nseq_seen Sequence: ",end='')
    
    for i in sequence:
        dut.inp_bit.value=i
        await FallingEdge(dut.clk)
        print(dut.seq_seen.value, end=' ')
        seq_seen_out.append(dut.seq_seen.value)

    print('\n')

    seq_seen_str = ""
    output_str = ""
    for i in seq_seen_out:
        seq_seen_str = seq_seen_str + str(i)
    for i in output:
        output_str = output_str + str(i)

    assert seq_seen_out == output, f"The output sequence is incorrent. It is not overlaping: Obtained Output = "+seq_seen_str+", Expected Output = "+output_str

    print('\n')