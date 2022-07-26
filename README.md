# Level 1 Design 1 (31:1 MUX) Design Verification
The verification environment is setup using Vyoma's UpTickPro provided for the hackathon.

![Screenshot from 2022-07-26 10-58-05](https://user-images.githubusercontent.com/109406155/180930212-b1ee7464-32ed-49cb-83dd-a119633f94a7.png)

# Verification Environment
The [CoCoTb](https://www.cocotb.org/) based Python test is developed as explained. The test drives inputs to the Design Under Test (adder module here) which takes in a total of 31 2-bit inputs to be selected from in the MUX and a 5-bit input to provide the select line and the output gives a 2-bit number as selected from the input.

# Test Case Scenario 1
The values are assigned to the input port per test case using
```
dut.sel.value = 12    // A 5-bit number
dut.i12.value = 2     // A 2-bit number
```

The assert statement is used for comparing the adder's outut to the expected value.

The following error is seen:
```
 assert dut.out.value == i12, "Mux result is incorrect: select value = {s} obtained value = {op}, expected value = {out12}".format (s = (dut.sel.value), i12 = (dut.inp12.value), op=int(dut.out.value), out12=i12)
                  AssertionError: Mux result is incorrect: select value = 01100 obtained value = 0, expected value = 2
```
### Test Scenario **(Important)**
- Test Inputs: sel=12 i12=2
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

### Design Fix
Updating the design and re-running the test makes the test pass.

![Screenshot from 2022-07-26 12-37-18](https://user-images.githubusercontent.com/109406155/180946125-c3f84a05-3515-4d45-b0b4-dd13b1e8d60e.png)

The bug free design is checked in as leve1_design1_bug_free\mux.v


# Test Case Scenario 2
The values are assigned to the input port per test case using
```
dut.sel.value = 30    // A 5-bit number
dut.i12.value = 2     // A 2-bit number
```

The assert statement is used for comparing the adder's outut to the expected value.

The following error is seen:
```
 assert dut.out.value == i30, "Mux result is incorrect: select value = {s} obtained value = {op}, expected value = {out30}".format (s = (dut.sel.value), i30 = (dut.inp30.value), op=int(dut.out.value), out30=i30)
                   AssertionError: Mux result is incorrect: select value = 11110, obtained value = 0, expected value = 2
```
### Test Scenario **(Important)**
- Test Inputs: sel=30 i30=2
- Expected Output: 2
- Observed Output in the DUT dut.out.value=0

Output mismatches for the above inputs proving that there is a design bug

### Design Bug
Based on the above test input and analysing the design, we see the following

```
      5'b11100: out = inp28;
      5'b11101: out = inp29;   // The same select line is present for inp30.
      default: out = 0;
```
For the MUX design, the line ``5'b11110: out = inp30;`` should be included before default.

### Design Fix
Updating the design and re-running the test makes the test pass.

![Screenshot from 2022-07-26 13-02-34](https://user-images.githubusercontent.com/109406155/180949784-ef36adcb-53db-4b44-adf7-f662a01023a8.png)

The bug free design is checked in as leve1_design1_bug_free\mux.v

_________________________________________________________________________________________________________________________________________________________

# Level 3 Design (4-bit adder using Full Adder and Half Adder modules) Design Verification
