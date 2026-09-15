# NASM
###### *"Looks low level but is higher level than python"*

---

## What is this???

Not to be mistaken for [The Net Wide Assembler](https://www.nasm.us/)

NASM (Not ASM) is an interpreted language which looks like ASM and implements a custom virtual CPU architecture.

###### *"What a python dev thinks low level programming looks like"*
It is complete with virtual memory slots (A1-Z10000), representing 260 KB in the virtual CPU architecture 

It also has registers (CA1-CZ100), representing 2.6 KB in the virtual CPU architecture.

It has HDD too (HA1-HZ53773), it is the persistent storage, it represents 5.3mb in the virtual CPU architecture.

<small>(Not the actual Python memory usage this assumes each slot = 1 byte.)</small>

It's ISA contains 23 instructions.

---

## How to use???
    ```txt
    Memory is defined as such:
        A1, B1, C1
        A2, B2, C2
        etc.
    Registers are defined as such:
        CA1, CB1, CC1,
        CA2, CB2, CC2,
        etc.
    HDD slots are defined as such:
        HA1, HB1, HB1, 
        HA2, HB2, HC2,
        etc.
    Instructions:
        SET - Sets a register/memory slot to a given value or character
        ADD - Adds a number to a register/memory slot or sets it to 1 char string
        SUB - Subtracts a number from a register/memory slot
        MUL - Multiplies a number to a register/memory slot
        ASLOT - Adds two numbers from first and second register/memory slot and stores it one first
        SSLOT - Subtracts two numbers from first and second register/memory slot and stores it one first
        MSLOT - Multiplies two numbers from first and second register/memory slot and stores it one first
        INP - Takes in user input and stores EACH character into a specified register/memory slot
        PRINT - Prints whatever is contained in a register/memory slot
        MOV - Copy values from one register/memory slot to another
        CMP - Compares values from two register/memory slots
        BNC - Bounces to a LOOP defined by the LOOP **Loop_Name** label
        BEQ - Bounce but conditional, basically bounce if last CMP was equal
        SIFEQ - Stop if equal, stops a loop if last CMP is equal
        SIFNEQ - Stop if not equal, stops a loop if last CMP is not equal
        IFEQ - Jumps by a defined number of lines or 1 line forward if last CMP is equal
        INEQ - Jumps by a defined number of lines or 1 line line forward if last CMP is not equal
        IFGR - Jumps by a defined number of lines or 1 line line forward if in the last CMP first value is greater than second
        IFLR - Jumps by a defined number of lines or 1 line line forward if in the last CMP first value is lesser than second
        CALL - Calls a file and makes interpreter read that file
        RETURN - Returns to the original root file
        COSLOT - Clears all occupied slots on HDD
        CFSLOT - Clears specific slots on HDD
    Labels:
        LOOP - Defines a named location that BNC/BEQ can bounce to
    ```
For more info click [here](Learn_NASM.md)

For reference look at the [test file](test.nasm)

To run the test file simply:

```bash 
python interpreter.py test.nasm
```

## NOTES

- Keep Z100-Z999 unallocated for stdlibs and/or other modules
- Also make sure seed inputted in random is 1-491 anything higher will yea segfault (eventually)
- The only thing's that can read/write directly to HDD is SET, PRINT, and MOV, otherwise you'd have to move the thing into memory first before use
- Run [hdd genertor](extras/hdd_gen.py) before using the interpreter

## Links

- Tutorial: [Learn](Learn_NASM.md)
- Contributing: [Contributor](CONTRIBUTING.md)
- Installing and setup: [Installation](INSTALLATION.md)
