# NASM
###### *"Looks low level but is higher level than python"*

---

## What is this???

Not to be mistaken for [The Net Wide Assembler](https://www.nasm.us/)

NASM (Not ASM) is an interpreted language which looks like ASM and implements a custom virtual CPU architecture.

###### *"What a python dev thinks low level programming looks like"*
It is complete with virtual memory slots (A1-Z10000), representing 260 KB in the virtual CPU architecture 

It also has registers (CA1-CZ100), representing 2.6 KB in the virtual CPU architecture.

<small>(Not the actual Python memory usage this assumes each slot = 1 byte.)</small>

It's ISA contains 21 instructions.

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
        IFEQ - Jumps 1 line forward if last CMP is equal
        INEQ - Jumps 1 line forward if last CMP is not equal
        IFGR - Jumps 1 line forward if in the last CMP first value is greater than second
        IFLR - Jumps 1 line forward if in the last CMP first value is lesser than second
        CALL - Calls a file and makes interpreter read that file
        Return - Returns to the original root file
    Labels:
        LOOP - Defines a named location that BNC/BEQ can bounce to
    ```

For reference look at test.nasm

To run the test file simply:

```bash 
python interpreter.py test.nasm
```

---

## Contributing

- Report bugs if you find any!
- Or even better, FIX IT AND PR!!!
- Also like add more ISA but keep it simple perhaps even just modifications of existing one, and keep it feeling low level
- Create custom modules hehe

## NOTES

- Keep Z100-Z999 unallocated for stdlibs and/or other modules
- Also make sure seed inputted in random is 1-491 anything higher will yea segfault (eventually)