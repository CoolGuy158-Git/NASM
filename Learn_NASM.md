# NASM Tutorial
###### *<small>Read the ```; Comments``` for info</small>*

---

## How to write your first 'Hello World'

### Important instructions:

- SET - Sets a register/memory slot to a given value or character
- PRINT - Prints whatever is contained in a register/memory slot

### Writing the program
```nasm
; Start off by placing each individual memory slots to a specific string
; Each slot can hold 1 character
; For programs like these use memory slot because they are moderately fast but plentiful, and you don't need persistent storage
SET A1 "H"
SET A2 "E"
SET A3 "L"
SET A4 "L"
SET A5 "O"
SET A6 " "
; This is the space
SET A7 "W"
SET A8 "O"
SET A9 "R"
SET A10 "L"
SET A11 "D"
; Now print everything, there isnt a newline set so it will just combine all the letters together
PRINT A1
PRINT A2
PRINT A3
PRINT A4
PRINT A5
PRINT A6
PRINT A7
PRINT A8
PRINT A9
PRINT A10
PRINT A11
```
Additionally, if you want to be more efficient and use less memory use this kind of structure:
```nasm
SET A1 "H"
PRINT A1
; Now just overwrite A1
SET A1 "E"
PRINT A1
; Continue till you get the desired Hello World Message
```

---

## Overview

From here on out we'll just have a basic overview on each instruction and their basic usage.

### ADD

This adds a number to the value currently stored in a slot. It can also be used like SET when adding strings to memory slots.
```nasm
ADD A1 1
ADD A1 1
PRINT A1
```
Output:
```
2
```

### SUB

This subtracts the value of what's in a slot and a number. 
```nasm
SET A1 3
SUB A1 1
SUB A1 1
PRINT A1
```
Output:
```
1
```

### MOV

This copies the value from a slot to another
```nasm
SET A1 2
SET A2 1
PRINT A2 [NLNS]
; NLNS stands for new line
MOV A2 A1
; This overwrites what was in A2 with the value of whats in A1
PRINT A2
```
Output:
```
1
2
```

---

## Notes and convention

- Do not use mem slot Z100-Z999 as stdlibs and other modules may use them
- Make sure the seed inputted into the psuedo random number generator is within 1-491
- The only instructions that can read/write directly to HDD is SET, PRINT, and MOV, otherwise you'd have to MOV the value from HDD to memory