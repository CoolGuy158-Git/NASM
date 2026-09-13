"""
NASM
---
Not Assembly,
A simple interpreter for an ASM like lang.
"Looks low level but is higher level than python".

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
"""

import sys
import time
import psutil
import threading
import keyboard

# Config
memory_amount = 10000
print_info = True

ticks_per_sec = 0
if print_info:
    # Get approx clock speed for info
    def get_info():
        global ticks_per_sec
        current_clock_speed = psutil.cpu_freq().current
        ticks_per_sec = current_clock_speed * 1_000_000

    threading.Thread(target=get_info).start()
try:
    filename = sys.argv[1]
except IndexError:
    filename = input("Input file name: ")
file = open(filename, "r")

# Create the virtual memory: A1-Z10000
memory = {
    f"{letter}{number}": ""
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for number in range(1, memory_amount + 1)
}
start = time.time()
line_number = 0
# Read source code and remove newlines
lines = [line.strip("\n") for line in file.readlines()]
labels = {} # And all the majors at labels, rebooting soon as I am able, every other day im wondering, whats a human being gotta be like, whats a way to just be competent, these sweet instincts ruin my life.
last_cmp = False
bnc_counts = {}
beq_counts = {}
while line_number < len(lines):
    try:
        line = lines[line_number]
        if not line.strip():
            line_number += 1
            continue
        # Add
        if line.startswith("ADD"):
            # Memory can only contain one char strings or 1 digit nums cuz i said so
            if len(line.split(maxsplit=2)[2].strip('"')) == 1:
                if line.split(maxsplit=2)[2].startswith('"') and line.split(maxsplit=2)[2].endswith('"'):
                    memory[line.split()[1].rstrip(",")] = line.split(maxsplit=2)[2].strip('"')
                else:
                    try:
                        product = int(memory[line.split()[1].rstrip(",")] or 0) + int(line.split(maxsplit=2)[2].strip('"'))
                        if product > 9:
                            print(f"\nERROR IN LINE {line_number}\n'{line}'\nMemory slots can only hold one character strings and one digit integers.")
                        else:
                            memory[line.split()[1].rstrip(",")] = product
                    except ValueError:
                        print(f"\nERROR IN LINE {line_number}\n'{line}'\nStrings must be enclosed in double quotes.")
            else:
                print(f"\nERROR IN LINE {line_number}\n'{line}'\nMemory slots can only hold one character strings and one digit integers.") # Dude istg one digit integers we're a bug then I realized they made sense sooo it's a feature now!
        # Subtract
        elif line.startswith("SUB"):
            if len(line.split(maxsplit=2)[2].strip('"')) == 1:
                if line.split()[2].startswith('"') and line.split()[2].endswith('"'):
                    print(f"\nERROR IN LINE {line_number}\n'{line}'\nCannot subtract strings")
                else:
                    try:
                        product = int(memory[line.split()[1].rstrip(",")] or 0) - int(line.split()[2].strip('"'))
                        # Prevent values outside 0-9
                        if product > 9 or product < 0:
                            print(f"\nERROR IN LINE {line_number}\n'{line}'\nMemory slots can only hold one character strings and one digit integers.")
                        else:
                            memory[line.split()[1].rstrip(",")] = product
                    except ValueError:
                        print(f"\nERROR IN LINE {line_number}\n'{line}'\nStrings must be enclosed in double quotes.")
            else:
                print(f"\nERROR IN LINE {line_number}\n'{line}'\nMemory slots can only hold one character strings and one digit integers.")
        # Inputs
        elif line.startswith("INP"):
            # Detect every keypress instead of input so that the input wont get echoed so it feels LOWLEVELLLL
            allowed = r"""1234567890-=qwertyuiopasdfghjklzxcvbnm,[];'./{}:">?!@#$%^&*()_+`~\|"""
            # Tried it and it gave shiftAshift so here's whitelist
            slots = line.split()[1:]
            for slot in slots:
                while True: # Wait till each slot gets a valid char
                    key = keyboard.read_event()
                    if key.event_type == keyboard.KEY_DOWN and key.name in allowed:
                        memory[slot.rstrip(",")] = key.name
                        break
        # Print
        elif line.startswith("PRINT"):
            print(str(memory[line.split()[1]]).replace("\\n", ""), end="")
            if len(line.split()) > 2:
                if line.split()[2].endswith("[NLNS]"):
                    print()
        # Move aka copy
        elif line.startswith("MOV"):
            from_hehe = line.split()[1].rstrip(",")
            to = line.split()[2].rstrip(",")
            memory[to] = memory[from_hehe]
        # Bounce or jump(If you're one of those ASM guys)
        elif line.startswith("BNC"):
            parts = line.split()
            label = parts[1].rstrip(",")
            if len(parts) > 2:
                count = int(parts[2])
                if line_number not in bnc_counts:
                    bnc_counts[line_number] = count
                if bnc_counts[line_number] > 0:
                    bnc_counts[line_number] -= 1
                    line_number = labels[label]
            else:
                line_number = labels[label]
        # Compare
        elif line.startswith("CMP"):
            a = memory[line.split()[1].rstrip(",")]
            b = memory[line.split()[2]]

            last_cmp = a == b

        # BEQ conditional bouncer
        elif line.startswith("BEQ"):
            parts = line.split()
            label = parts[1].rstrip(",")
            if last_cmp:
                if len(parts) > 2:
                    count = int(parts[2])
                    if line_number not in beq_counts:
                        beq_counts[line_number] = count
                    if beq_counts[line_number] > 0:
                        beq_counts[line_number] -= 1
                        line_number = labels[label]
                else:
                    line_number = labels[label]
        # Comments
        elif line.startswith(";"):
            line_number += 1
            continue

        # Them loop label
        elif line.startswith("LOOP"):
            labels[line.split()[1].rstrip(":")] = line_number

        else:
            unknown = line.split()[0].strip('"')
            print(f"\nERROR IN LINE {line_number}\n'{line}'\nUnknown instruction: '{unknown}'")

        line_number += 1
    except Exception as e:
        print(f"\n\n\nOH NO!")
        print("I'm sorry :(")
        print("The interpreter encountered an error.") # Because the programmer is so bad at coding D:
        print("Please make an issue in github :), or even better fix it and PR :D")
        print("Error:")
        print(e)
if print_info:
    end = time.time()
    elapsed = end - start
    ticks = elapsed * ticks_per_sec
    print(f"\n\nTotal run time: {elapsed:.6f} seconds")
    print(f"Approx: {ticks:.6f} cpu clock cycles used in run time")
    if line_number > 0:
        ticks_per_line = ticks / line_number
        print(f"Approx: {ticks_per_line:.6f} cpu clock cycles used per line on average")
    else:
        print(f"Approx: 0 cpu clock cycles used per line on average:\n0 lines found")