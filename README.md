# Level 1 Design 1 (31:1 MUX) Design Verification
The verification environment is setup using Vyoma's UpTickPro provided for the hackathon.

![Screenshot from 2022-07-30 06-06-34](https://user-images.githubusercontent.com/109406155/181872425-22329b4c-5ecd-47e6-b38c-f848a9a58316.png)

# Verification Environment
The [CoCoTb](https://www.cocotb.org/) based Python test is developed as explained. The test drives inputs to the Design Under Test (MUX module here) which takes in a total of 31 2-bit inputs to be selected from in the MUX and a 5-bit input to provide the select line and the output gives a 2-bit number as selected from the input.

# Test Case Scenario 1
The values are assigned to the input port per test case using
```
dut.sel.value = 12    // A 5-bit number
dut.i12.value = 2     // A 2-bit number
```

The assert statement is used for comparing the MUX's output to the expected value.

The following error is seen:
```
 assert dut.out.value == i12, "Mux result is incorrect: select value = {s} obtained value = {op}, expected value = {out12}".format (s = (dut.sel.value), i12 = (dut.inp12.value), op=int(dut.out.value), out12=i12)
                  AssertionError: Mux result is incorrect: select value = 01100 obtained value = 0, expected value = 2
```
### Test Scenario **(Important)**
- Test Inputs: sel=12, i12=2
- Expected Output: 2
- Observed Output in the DUT dut.out.value=0

Output mismatches for the above inputs proving that there is a design bug

### Design Bug
Based on the above test input and analysing the design, we see the following

```
      5'b01011: out = inp11;
      5'b01101: out = inp12;    // The same select line is given for both inp12 and inp13.
      5'b01101: out = inp13;    // Hence the final output for 5'b01101 / 13 is the value of inp13 and the output for select 12 is coming to zero.
```
For the MUX design, the logic should be ``5'b01100: out = inp12`` instead of ``5'b01101: out = inp12`` as in the design code.

# Test Case Scenario 2
The values are assigned to the input port per test case using
```
dut.sel.value = 30    // A 5-bit number
dut.i12.value = 2     // A 2-bit number
```

The assert statement is used for comparing the MUX's output to the expected value.

The following error is seen:
```
 assert dut.out.value == i30, "Mux result is incorrect: select value = {s} obtained value = {op}, expected value = {out30}".format (s = (dut.sel.value), i30 = (dut.inp30.value), op=int(dut.out.value), out30=i30)
                   AssertionError: Mux result is incorrect: select value = 11110, obtained value = 0, expected value = 2
```
### Test Scenario **(Important)**
- Test Inputs: sel=30, i30=2
- Expected Output: 2
- Observed Output in the DUT dut.out.value=0

Output mismatches for the above inputs proving that there is a design bug

### Design Bug
Based on the above test input and analysing the design, we see the following

```
      5'b11100: out = inp28;
      5'b11101: out = inp29;   // The select line for 30 is not present.
      default: out = 0;
```
For the MUX design, the line ``5'b11110: out = inp30;`` should be included before default and after ``5'b11101: out = inp29;``.

### Design Fix
Updating the design and re-running the test makes the test pass.

![Screenshot from 2022-07-30 10-59-39](https://user-images.githubusercontent.com/109406155/181876235-d526ba53-a57a-4391-8437-ad788a40d588.png)

The bug free design is checked in as leve1_design1_bug_free\mux_bug_free.v

_________________________________________________________________________________________________________________________________________________________

# Level 1 Design 2 (1011: Sequence Detector) Verification Environment
The [CoCoTb](https://www.cocotb.org/) based Python test is developed as explained. The test drives inputs to the Design Under Test (1011 Sequnce Detector module here) which takes inp_bit, clock and reset bit input. The output gives a high when sequence is detected after reset is low from high.

# Test Case Scenario 1

- Test Sequence:   1 0 1 1 0 1 1
- Expected Output: 0 0 0 1 0 0 1
- Observed Output: 0 0 0 1 0 0 0
- dut.reset.value = \<declared as part of provided code sample\>
- dut.clk.value = \<declared as part of provided code sample\>

The Sequence detector must be overlapping as well as in this case, the fourth bit resembles the LSB of the first 4 bit sequence and also the MSB followed by the next three bit sequence forming a 4-bit sequence. Hence the detector needs to be high twince during the bitstream as shown in the Expected output. In contradiction, the obtained output does not match with the desired output. This causes a bug which is exposed in the code. 

The assert statement is used for comparing the sequence detector output to the expected value. Implementing the assert satatement, the following error is seen:
```
assert seq_seen_out == output, f"The output sequence is incorrent. It is not overlaping: Obtained Output = "+seq_seen_str+", Expected Output = "+output_str
                  AssertionError: The output sequence is incorrent. It is not overlaping: Obtained Output = 0001000, Expected Output = 0001001
```
Output mismatches for the above inputs proving that there is a design bug

### Design Bug
Based on the above test input and analysing the design, we see the following

```
      SEQ_101:
      begin
        if(inp_bit == 1)
          next_state = SEQ_1011;
        else
          next_state = IDLE;  // Bug_line1
      end
      SEQ_1011:
      begin
        next_state = IDLE;    // Bug_line2
      end
```
For the sequence detector to be overlapping, The control must be moved to 2nd bit of the sequence in the case of line 'bug1' because if 0 is observed after 101, it can be an overlapping case where the sequence starts from the 3rd bit, i.e., '1' in the sequence. Again this is a similar condition which causes an error in the case of line 'bug2', because after 1011 is detected, the control is unconditionally moved to the absolute beginning, ignoring the case that the LSB of the current detected sequence may also be the MSB of another sequence that follows.

In the above section of code, the following line must be replaced in place of the bug line:
	
Bug line 1 fix:

```
next_state = SEQ_10;
```

Bug line 2 fix:

```
if(inp_bit == 1)
  next_state = IDLE;
else
  next_state = SEQ_10;
```

# Test Case Scenario 2

- Test Sequence:   1 1 1 0 1 1
- Expected Output: 0 0 0 0 0 1
- Observed Output: 0 0 0 0 0 0
- dut.reset.value = \<declared as part of provided code sample\>
- dut.clk.value = \<declared as part of provided code sample\>

The Sequence detector must be overlapping as well as in this case, the fourth bit resembles the LSB of the first 4 bit sequence and also the MSB followed by the next three bit sequence forming a 4-bit sequence. Hence the detector needs to be high twince during the bitstream as shown in the Expected output. In contradiction, the obtained output does not match with the desired output. This causes a bug which is exposed in the code. 

The assert statement is used for comparing the sequence detector output to the expected value. Implementing the assert satatement, the following error is seen:
```
assert seq_seen_out == output, f"The output sequence is incorrent. It is not overlaping: Obtained Output = "+seq_seen_str+", Expected Output = "+output_str
                  AssertionError: The output sequence is incorrent. It is not overlaping: Obtained Output = 000000, Expected Output = 000001
```
Output mismatches for the above inputs proving that there is a design bug

### Design Bug
Based on the above test input and analysing the design, we see the following

```
      SEQ_1:
      begin
        if(inp_bit == 1)
          next_state = IDLE;   // Bug_line1
        else
          next_state = SEQ_10;
      end
```
For the sequence detector to be overlapping, in the case of Bug_line1, the control must be moved to the same state (SEQ_1), because that high bit can be the MSB of another sequence that follows.

In the above section of code, the following line must be replaced in place of the bug line:
	
Bug line 1 fix:

```
next_state = SEQ_1;
```

### Design Fix
Updating the design and re-running the test makes the test pass.

![Screenshot from 2022-07-30 10-45-35](https://user-images.githubusercontent.com/109406155/181875859-03d0a263-65d8-4a71-8df7-d10a05a26698.png)

The bug free design is checked in as level1_design2_bug_free\seq_detect_1011_bug_free.v
_________________________________________________________________________________________________________________________________________________________

# Level 3 Design (4-bit adder using Mixed Modelling) Verification Environment
The [CoCoTb](https://www.cocotb.org/) based Python test is developed as explained. The test drives inputs to the Design Under Test (4-bit adder module here) which takes 2 4-bit numbers 'a' and 'b' and a 1-bit carry input to a full adder which is connected in series to the consecutive full adders. The output gives a 5-bit sum.

# Test Case Scenario 1
The values are assigned to the input port using
```
dut.a.value = 10   // 4-bit number
dut.b.value = 6     // 4-bit number
dut.cin.value = 1   // 1-bit carry
```

The assert statement is used for comparing the adder's output to the expected value.

The following error is seen:
```
assert dut.sum.value == a+b+cin, f"Adder result is incorrect: Obtained Output = {dut.sum.value}, Expected Output = "+str(a+b+cin)
                  AssertionError: Adder result is incorrect: Obtained Output = 01101 (13), Expected Output = 17
```
### Test Scenario **(Important)**
- Test Inputs: a=10, b=6, cin=1
- Expected Output: 10001 (17)
- Observed Output in the DUT dut.out.value = 01101 (13)

Output mismatches for the above inputs proving that there is a design bug

### Design Bug
Based on the above test input and analysing the design, we see the following

```
      ha ha1(s,c1,a,b), ha2(sum,c2,s,cin);
	     and(cout,c2,c1);
```
In the Full adder module, the final carry output is formed by the OR gate, but in the design, it is declared as AND gate. This causes the carry bit to not be reflected in any one full adder which produces a carry bit. In a full adder, the carry bit is not high if any one of the carry bit of the individual half adder is low. Hence, this case does not produce failed case in any of the addition combination.  Therefore, it is required to give fixed value to expose the bug instead of randomized case.

For the Adder design, the logic should be ``or(cout,c2,c1);`` instead of ``and(cout,c2,c1);`` as in the 'fa' mudule in the design code.

### Design Fix
Updating the design and re-running the test makes the test pass.

![Screenshot from 2022-07-30 11-17-52](https://user-images.githubusercontent.com/109406155/181876721-5606d5ab-a2da-4f50-9c4e-f0d5dc5cdd08.png)

The bug free design is checked in as level1_design_bug_free\Adder_bug_free.v
