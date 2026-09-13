# NASM
###### *"Looks low level but is higher level than python"*

---

## What is this???

Not to be mistaken for [The Net Wide Assembler](https://www.nasm.us/)

NASM (Not ASM) is an interpreted language that looks like ASM.

###### *"What a python dev thinks low level programming looks like"*
It is complete with virtual memory slots (A1-Z10000)

It's ISA contains 9 instructions.

---

## How to use???
    ```txt
    Memory is defined as such:
        A1, B1, C1
        A2, B2, C2
        etc.

    instructions:
        ADD - Adds a number OR a 1 character string to a memory slot
        SUB - Subtracts a number from a memory slot
        INP - Takes in user input and stores EACH character into a specified memory slot
        PRINT - Prints whatever is contained in a memory slot
        MOV - Copy values from one memory slot to another
        CMP - Compares values from two memory slots
        BNC - Bounces to a LOOP defined by the LOOP **Loop_Name** label
        BEQ - Bounce but conditional, basically bounce if last CMP was equal
        LOOP - Defines a named location that BNC/BEQ can bounce to
    ```

For reference look at test.nasm

To run simply

```bash 
python interpreter.py file.nasm
```

---

## Contributing

- Report bugs if you find any!
- Or even better, FIX IT AND PR!!!
- Also like add more ISA but keep it simple perhaps even just modifications of existing one, and keep it feeling low level

