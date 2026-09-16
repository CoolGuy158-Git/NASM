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
"""

import sys
import time
import psutil
import threading
import keyboard
import traceback

# Config
memory_amount = 10000
register_amount = 100
print_info = True

hdd = open("components/NASM.hdd", "r+b")

# Special read, write and index for hdd cuz it special
# The only thing's that can read/write directly to HDD is SET, PRINT, and MOV, otherwise you'd have to move the thing into memory first before use
def hdd_index(address): # Turn the hdd bins into like readable for python
    letter = ord(address[1]) - ord('A')
    number = int(address[2:]) - 1
    return (number*26+letter)*4
def read_hdd(address):
    hdd.seek(hdd_index(address))
    data = hdd.read(4)
    if not data:
        print(f"\nFATAL:\n HDD slot {address} is empty") # Yea this is kinda a fatal of an error cuz yea can't really skip it and move on (can you?) and the whole thing just stops
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
            print("Program encountered a fatal error and was terminated")
        hdd.close()
        sys.exit(0)
    kind_of_data = data[0]
    value = int.from_bytes(data[1:], byteorder='little')
    if kind_of_data == 0:
        return ""
    elif kind_of_data == 1:
        return value
    elif kind_of_data == 2:
        return chr(value)
def write_hdd(address, value):
    hdd.seek(hdd_index(address))
    if value == "":
        data = b"\x00\x00\x00\x00"
    elif isinstance(value, int):
        if value<0 or value >999:
            print("\nERROR\nHDD slots can only hold one character strings and 3 digit integers.")
            return
        data = bytes([1]) + value.to_bytes(3, "little")
    elif isinstance(value, str) and len(value) == 1:
        data = bytes([2])+ord(value).to_bytes(3, "little")
    else:
        print("\nERROR\nHDD slots can only hold one character strings and 3 digit integers.")
        return
    hdd.write(data)

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
memory_amount = min(memory_amount, 10000)
memory = {
    f"{letter}{number}": ""
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for number in range(1, memory_amount + 1)
}
register_amount = min(register_amount, 100) # Max is CA1-CZ100
registry = {
    f"C{letter}{number}": ""
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for number in range(1, register_amount + 1)
}
start = time.time()
labels = {} # And all the majors at labels, rebooting soon as I am able, every other day im wondering, whats a human being gotta be like, whats a way to just be competent, these sweet instincts ruin my life.
# Read source code and remove newlines and comments
lines = []
for line in file.readlines():
    if not line.strip().startswith(";"):
        lines.append(line.strip("\n"))
for i, line in enumerate(lines):
    if line.startswith("LOOP"):
        labels[line.split()[1].rstrip(":")] = i  # Just get label here so that loops can jump backward and forward
line_number = 0
last_cmp = False
greater = False
bnc_counts = {}
beq_counts = {}
original_lines = lines
return_line = 0
stop_loop = False
while line_number < len(lines):
    try:
        line = lines[line_number]
        if not line.strip():
            line_number += 1
            continue
        # Add
        # Ik all of this sh## couldve been more readable but ehh ill just refactor/clean up later, i just wanna get this working
        # Yea uhm SET, ADD, SUB, MUL and those other arithmetic guys are basically just copy-pasted sooo XD
        if line.startswith("SET"):
            # Memory can only contain one char strings or 3 digit nums cuz i said so
            if line.split()[1].startswith("C"):
                # This is for the registers sooo no delay hehe
                if len(line.split(maxsplit=2)[2].strip('"')) == 1 if line.split(maxsplit=2)[2].startswith('"') and line.split(maxsplit=2)[2].endswith('"') else len(line.split(maxsplit=2)[2].strip('"')) <= 3: # yeah ik i couldve made this more readable but come one that would mean changing a lot of lines, im too lazy for that
                    if line.split(maxsplit=2)[2].startswith('"') and line.split(maxsplit=2)[2].endswith('"'):
                        registry[line.split()[1].rstrip(",")] = line.split(maxsplit=2)[2].strip('"') # Be thankful i added sum coma tolerance, it isnt even supposed to be used
                    else:
                        try:
                            product = int(line.split(maxsplit=2)[2].strip('"'))
                            if product > 999:
                                print(f"\nERROR \n'{line}'\nRegistry slots can only hold one character strings and 3 digit integers.")
                            else:
                                registry[line.split()[1].rstrip(",")] = product
                        except ValueError:
                            print(f"\nERROR \n'{line}'\nStrings must be enclosed in double quotes.")
                else:
                    print(f"\nERROR \n'{line}'\nRegistry slots can only hold one character strings and 3 digit integers.")  # Dude istg one digit integers we're a bug then I realized they made sense sooo it's a feature now!
            elif line.split()[1].startswith("H"):
                if line.split(maxsplit=2)[2].startswith('"') and line.split(maxsplit=2)[2].endswith('"'):
                    write_hdd(line.split()[1].rstrip(","), line.split(maxsplit=2)[2].strip('"')) # Be thankful i added sum coma tolerance, it isnt even supposed to be used
                else:
                    try:
                        product = int(line.split(maxsplit=2)[2].strip('"'))
                        write_hdd(line.split()[1].rstrip(","), product)
                    except ValueError:
                        print(f"\nERROR \n'{line}'\nStrings must be enclosed in double quotes.")
            else:
                time.sleep(0.0001) # Little delay to artificially simulate uhh yea yea
                if len(line.split(maxsplit=2)[2].strip('"')) == 1 if line.split(maxsplit=2)[2].startswith('"') and line.split(maxsplit=2)[2].endswith('"') else len(line.split(maxsplit=2)[2].strip('"')) <= 3:
                    if line.split(maxsplit=2)[2].startswith('"') and line.split(maxsplit=2)[2].endswith('"'):
                        memory[line.split()[1].rstrip(",")] = line.split(maxsplit=2)[2].strip('"')
                    else:
                        try:
                            product = int(line.split(maxsplit=2)[2].strip('"'))
                            if product > 999:
                                print(f"\nERROR \n'{line}'\nMemory slots can only hold one character strings and 3 digit integers.")
                            else:
                                memory[line.split()[1].rstrip(",")] = product
                        except ValueError:
                            print(f"\nERROR \n'{line}'\nStrings must be enclosed in double quotes.")
                else:
                    print(f"\nERROR \n'{line}'\nMemory slots can only hold one character strings and 3 digit integers.") # Dude istg one digit integers we're a bug then I realized they made sense sooo it's a feature now!

        elif line.startswith("ADD"):
            # Memory can only contain one char strings or 3 digit nums cuz i said so
            if line.split()[1].startswith("C"):
                # This is for the registers sooo no delay hehe
                if len(line.split(maxsplit=2)[2].strip('"')) == 1 if line.split(maxsplit=2)[2].startswith('"') and line.split(maxsplit=2)[2].endswith('"') else len(line.split(maxsplit=2)[2].strip('"')) <= 3: # yeah ik i couldve made this more readable but come one that would mean changing a lot of lines, im too lazy for that
                    if line.split(maxsplit=2)[2].startswith('"') and line.split(maxsplit=2)[2].endswith('"'):
                        registry[line.split()[1].rstrip(",")] = line.split(maxsplit=2)[2].strip('"') # Be thankful i added sum coma tolerance, it isnt even supposed to be used
                    else:
                        try:
                            product = int(registry[line.split()[1].rstrip(",")] or 0) + int(line.split(maxsplit=2)[2].strip('"'))
                            if product > 999:
                                print(f"\nERROR \n'{line}'\nRegistry slots can only hold one character strings and 3 digit integers.")
                            else:
                                registry[line.split()[1].rstrip(",")] = product
                        except ValueError:
                            print(f"\nERROR \n'{line}'\nStrings must be enclosed in double quotes.")
                else:
                    print(f"\nERROR \n'{line}'\nRegistry slots can only hold one character strings and 3 digit integers.")  # Dude istg one digit integers we're a bug then I realized they made sense sooo it's a feature now!
            else:
                time.sleep(0.0001) # Little delay to artificially simulate uhh yea yea
                if len(line.split(maxsplit=2)[2].strip('"')) == 1 if line.split(maxsplit=2)[2].startswith('"') and line.split(maxsplit=2)[2].endswith('"') else len(line.split(maxsplit=2)[2].strip('"')) <= 3:
                    if line.split(maxsplit=2)[2].startswith('"') and line.split(maxsplit=2)[2].endswith('"'):
                        memory[line.split()[1].rstrip(",")] = line.split(maxsplit=2)[2].strip('"')
                    else:
                        try:
                            product = int(memory[line.split()[1].rstrip(",")] or 0) + int(line.split(maxsplit=2)[2].strip('"'))
                            if product > 999:
                                print(f"\nERROR \n'{line}'\nMemory slots can only hold one character strings and 3 digit integers.")
                            else:
                                memory[line.split()[1].rstrip(",")] = product
                        except ValueError:
                            print(f"\nERROR \n'{line}'\nStrings must be enclosed in double quotes.")
                else:
                    print(f"\nERROR \n'{line}'\nMemory slots can only hold one character strings and 3 digit integers.") # Dude istg one digit integers we're a bug then I realized they made sense sooo it's a feature now!

        # Subtract
        elif line.startswith("SUB"):
            if line.split()[1].startswith("C"):
                if len(line.split(maxsplit=2)[2].strip('"')) == 1 if line.split(maxsplit=2)[2].startswith('"') and line.split(maxsplit=2)[2].endswith('"') else len(line.split(maxsplit=2)[2].strip('"')) <= 3:
                    if line.split()[2].startswith('"') and line.split()[2].endswith('"'):
                        print(f"\nERROR \n'{line}'\nCannot subtract strings")
                    else:
                        try:
                            product = int(registry[line.split()[1].rstrip(",")] or 0) - int(line.split()[2].strip('"'))
                            # Prevent values outside 0-999
                            if product > 999 or product < 0:
                                print(f"\nERROR \n'{line}'\nRegistry slots can only hold one character strings and 3 digit integers.")
                            else:
                                registry[line.split()[1].rstrip(",")] = product
                        except ValueError:
                            print(f"\nERROR \n'{line}'\nStrings must be enclosed in double quotes.")
                else:
                    print(f"\nERROR \n'{line}'\nRegistry slots can only hold one character strings and 3 digit integers.")
            else:
                time.sleep(0.0001)
                if len(line.split(maxsplit=2)[2].strip('"')) == 1 if line.split(maxsplit=2)[2].startswith('"') and line.split(maxsplit=2)[2].endswith('"') else len(line.split(maxsplit=2)[2].strip('"')) <= 3:
                    if line.split()[2].startswith('"') and line.split()[2].endswith('"'):
                        print(f"\nERROR \n'{line}'\nCannot subtract strings")
                    else:
                        try:
                            product = int(memory[line.split()[1].rstrip(",")] or 0) - int(line.split()[2].strip('"'))
                            # Prevent values outside 0-999
                            if product > 999 or product < 0:
                                print(f"\nERROR \n'{line}'\nMemory slots can only hold one character strings and 3 digit integers.")
                            else:
                                memory[line.split()[1].rstrip(",")] = product
                        except ValueError:
                            print(f"\nERROR \n'{line}'\nStrings must be enclosed in double quotes.")
                else:
                    print(f"\nERROR \n'{line}'\nMemory slots can only hold one character strings and 3 digit integers.")
        # Multiply
        elif line.startswith("MUL"):
            if line.split()[1].startswith("C"):
                if len(line.split(maxsplit=2)[2].strip('"')) == 1 if line.split(maxsplit=2)[2].startswith('"') and line.split(maxsplit=2)[2].endswith('"') else len(line.split(maxsplit=2)[2].strip('"')) <= 3:
                    if line.split()[2].startswith('"') and line.split()[2].endswith('"'):
                        print(f"\nERROR \n'{line}'\nCannot multiply strings")
                    else:
                        try:
                            product = int(registry[line.split()[1].rstrip(",")] or 0) * int(line.split()[2].strip('"'))
                            # Prevent values outside 0-999
                            if product > 999 or product < 0:
                                print(f"\nERROR \n'{line}'\nRegistry slots can only hold one character strings and 3 digit integers.")
                            else:
                                registry[line.split()[1].rstrip(",")] = product
                        except ValueError:
                            print(f"\nERROR \n'{line}'\nStrings must be enclosed in double quotes.")
                else:
                    print(f"\nERROR \n'{line}'\nRegistry slots can only hold one character strings and 3 digit integers.")
            else:
                time.sleep(0.0001)
                if len(line.split(maxsplit=2)[2].strip('"')) == 1 if line.split(maxsplit=2)[2].startswith('"') and line.split(maxsplit=2)[2].endswith('"') else len(line.split(maxsplit=2)[2].strip('"')) <= 3:
                    if line.split()[2].startswith('"') and line.split()[2].endswith('"'):
                        print(f"\nERROR \n'{line}'\nCannot multiply strings")
                    else:
                        try:
                            product = int(memory[line.split()[1].rstrip(",")] or 0) * int(line.split()[2].strip('"'))
                            # Prevent values outside 0-999
                            if product > 999 or product < 0:
                                print(f"\nERROR \n'{line}'\nMemory slots can only hold one character strings and 3 digit integers.")
                            else:
                                memory[line.split()[1].rstrip(",")] = product
                        except ValueError:
                            print(f"\nERROR \n'{line}'\nStrings must be enclosed in double quotes.")
                else:
                    print(f"\nERROR \n'{line}'\nMemory slots can only hold one character strings and 3 digit integers.")
        # ASLOT and SSLOT means ADDSLOT and SUBTRACTSLOT it lets you do:
        # ASLOT A1 A2
        # Basically add the value from A2 to A1
        # MSLOT is just multiply but yeayea
        elif line.startswith("ASLOT"):
            if line.split()[1].startswith("C"):
                if line.split()[2].startswith('"') and line.split()[2].endswith('"'):
                    print(f"\nERROR \n'{line}'\nCannot ADD/SUBTRACT registry slots with stings")
                else:
                    try:
                        from_hehehe = line.split()[2].strip(",")
                        value = registry[from_hehehe]
                        product = int(registry[line.split()[1].rstrip(",")] or 0) + int(value)
                        # Prevent values outside 0-999
                        if product > 999 or product < 0:
                            print(f"\nERROR \n'{line}'\nRegistry slots can only hold one character strings and 3 digit integers.")
                        else:
                            registry[line.split()[1].rstrip(",")] = product
                    except ValueError:
                        print(f"\nERROR \n'{line}'\nStrings must be enclosed in double quotes.")

            else:
                time.sleep(0.0001)
                if line.split()[2].startswith('"') and line.split()[2].endswith('"'):
                    print(f"\nERROR \n'{line}'\nCannot ADD/SUBTRACT memory slots with stings")
                else:
                    try:
                        from_hehehe = line.split()[2].strip(",")
                        value = memory[from_hehehe]
                        product = int(memory[line.split()[1].rstrip(",")] or 0) + int(value)
                        # Prevent values outside 0-999
                        if product > 999 or product < 0:
                            print(f"\nERROR \n'{line}'\nMemory slots can only hold one character strings and 3 digit integers.")
                        else:
                            memory[line.split()[1].rstrip(",")] = product
                    except ValueError:
                        print(f"\nERROR \n'{line}'\nStrings must be enclosed in double quotes.")

        elif line.startswith("SSLOT"):
            if line.split()[1].startswith("C"):
                if line.split()[2].startswith('"') and line.split()[2].endswith('"'):
                    print(f"\nERROR \n'{line}'\nCannot ADD/SUBTRACT registry slots with stings")
                else:
                    try:
                        from_hehehe = line.split()[2].strip(",")
                        value = registry[from_hehehe]
                        product = int(registry[line.split()[1].rstrip(",")] or 0) - int(value)
                        # Prevent values outside 0-999
                        if product > 999 or product < 0:
                            print(f"\nERROR \n'{line}'\nRegistry slots can only hold one character strings and 3 digit integers.")
                        else:
                            registry[line.split()[1].rstrip(",")] = product
                    except ValueError:
                        print(f"\nERROR \n'{line}'\nStrings must be enclosed in double quotes.")
            else:
                time.sleep(0.0001)
                if line.split()[2].startswith('"') and line.split()[2].endswith('"'):
                    print(f"\nERROR \n'{line}'\nCannot ADD/SUBTRACT memory slots with stings")
                else:
                    try:
                        from_hehehe = line.split()[2].strip(",")
                        value = memory[from_hehehe]
                        product = int(memory[line.split()[1].rstrip(",")] or 0) - int(value)
                        # Prevent values outside 0-999
                        if product > 999 or product < 0:
                            print(f"\nERROR \n'{line}'\nMemory slots can only hold one character strings and 3 digit integers.")
                        else:
                            memory[line.split()[1].rstrip(",")] = product
                    except ValueError:
                        print(f"\nERROR \n'{line}'\nStrings must be enclosed in double quotes.")
        elif line.startswith("MSLOT"):
            if line.split()[1].startswith("C"):
                if len(line.split(maxsplit=2)[2].strip('"')) == 1 if line.split(maxsplit=2)[2].startswith('"') and line.split(maxsplit=2)[2].endswith('"') else len(line.split(maxsplit=2)[2].strip('"')) <= 3:
                    if line.split()[2].startswith('"') and line.split()[2].endswith('"'):
                        print(f"\nERROR \n'{line}'\nCannot multiply strings")
                    else:
                        try:
                            from_hehehe = line.split()[2].strip(",")
                            value = registry[from_hehehe]
                            product = int(registry[line.split()[1].rstrip(",")] or 0) * int(value)
                            # Prevent values outside 0-999
                            if product > 999 or product < 0:
                                print(f"\nERROR \n'{line}'\nRegistry slots can only hold one character strings and 3 digit integers.")
                            else:
                                registry[line.split()[1].rstrip(",")] = product
                        except ValueError:
                            print(f"\nERROR \n'{line}'\nStrings must be enclosed in double quotes.")
                else:
                    print(f"\nERROR \n'{line}'\nRegistry slots can only hold one character strings and 3 digit integers.")
            else:
                time.sleep(0.0001)
                if len(line.split(maxsplit=2)[2].strip('"')) == 1 if line.split(maxsplit=2)[2].startswith('"') and line.split(maxsplit=2)[2].endswith('"') else len(line.split(maxsplit=2)[2].strip('"')) <= 3:
                    if line.split()[2].startswith('"') and line.split()[2].endswith('"'):
                        print(f"\nERROR \n'{line}'\nCannot multiply strings")
                    else:
                        try:
                            from_hehehe = line.split()[2].strip(",")
                            value = memory[from_hehehe]
                            product = int(memory[line.split()[1].rstrip(",")] or 0) * int(value)
                            # Prevent values outside 0-999
                            if product > 999 or product < 0:
                                print(f"\nERROR \n'{line}'\nMemory slots can only hold one character strings and 3 digit integers.")
                            else:
                                memory[line.split()[1].rstrip(",")] = product
                        except ValueError:
                            print(f"\nERROR \n'{line}'\nStrings must be enclosed in double quotes.")
                else:
                    print(f"\nERROR \n'{line}'\nMemory slots can only hold one character strings and 3 digit integers.")

        # Inputs
        elif line.startswith("INP"):
            # Detect every keypress instead of input so that the input wont get echoed so it feels LOWLEVELLLL
            # Uhh dont put input directly to HDD cuz idk it feels wrong
            allowed = r"""1234567890-=qwertyuiopasdfghjklzxcvbnm,[];'./{}:">?!@#$%^&*()_+`~\|"""
            # Tried it and it gave shiftAshift so here's whitelist
            slots = line.split()[1:]
            for slot in slots:
                while True: # Wait till each slot gets a valid char
                    key = keyboard.read_event()
                    if key.event_type == keyboard.KEY_DOWN and key.name in allowed:
                        slot = slot.rstrip(",")
                        if slot.startswith("C"): # Yippee support for registers!
                            registry[slot] = key.name
                        elif slot.startswith("H"):
                            print("ERROR! Unable to write keyboard inputs directly to HDD")
                        else:
                            time.sleep(0.00001) # VERY VERY small delay
                            memory[slot] = key.name
                        break
        # Print
        elif line.startswith("PRINT"):
            if line.split()[1].startswith("C"):
                print(str(registry[line.split()[1].rstrip(",")]).replace("\\n", ""), end="")
            elif line.split()[1].startswith("H"):
                print(str(read_hdd(line.split()[1].rstrip(","))).replace("\\n", ""), end="")
            else:
                time.sleep(0.00001)
                print(str(memory[line.split()[1].rstrip(",")]).replace("\\n", ""), end="")
            if len(line.split()) > 2:
                if line.split()[2].endswith("[NLNS]"):
                    print()
        # Move aka copy
        elif line.startswith("MOV"):
            from_hehe = line.split()[1].rstrip(",")
            to = line.split()[2].rstrip(",")
            if from_hehe.startswith("C"):
                value = registry[from_hehe]
            elif from_hehe.startswith("H"):
                value = read_hdd(from_hehe)
            else:
                time.sleep(0.00001)
                value = memory[from_hehe]
            if to.startswith("C"):
                registry[to] = value
            elif to.startswith("H"):
                write_hdd(to, value)
            else:
                time.sleep(0.00001)
                memory[to] = value
        # Bounce or jump(If you're one of those ASM guys)
        elif line.startswith("BNC"):
            if stop_loop:
                stop_loop = False
                pass
            else:
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
            # Compare also can't compare directly from HDD
            a_slot = line.split()[1].rstrip(",")
            b_slot = line.split()[2]
            if a_slot.startswith("C"):
                a = registry[a_slot]
            else:
                time.sleep(0.00001)
                a = memory[a_slot]
            if b_slot.startswith("C"):
                b = registry[b_slot]
            else:
                time.sleep(0.00001)
                b = memory[b_slot]
            a = a or 0
            b = b or 0
            last_cmp = a==b
            greater = a>b

        # BEQ conditional bouncer
        elif line.startswith("BEQ"):
            if stop_loop:
                stop_loop = False
                pass
            else:
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
        # Conditional STOPPER and SKIPPERS, stops the car(Or last loop for those who dont get it) if last cmp was equal
        # Stop any loop if equal
        elif line.startswith("SIFEQ"):
            if last_cmp:
                stop_loop = True
        # Stop any loop if NOT equal
        elif line.startswith("SIFNEQ"):
            if not last_cmp:
                stop_loop = True
        # Skip ahead 1 line by default if equal
        # You can also do IFEQ 5
        elif line.startswith("IFEQ"):
            if last_cmp:
                if len(line.split()) > 1:
                        line_number += int(line.split()[1]) + 1
                else:
                    line_number += 2 # Do 2 cuz it also skips the line_number+1 below
                continue
        # Skip ahead 1 line by default if NOT equal
        elif line.startswith("INEQ"):
            if not last_cmp:
                if len(line.split()) > 1:
                    line_number += int(line.split()[1]) + 1
                else:
                    line_number += 2
                continue
        # Skip ahead 1 line by default if first value is greater than second in last CMP
        elif line.startswith("IFGR"):
            if greater:
                if len(line.split()) > 1:
                    line_number += int(line.split()[1]) + 1
                else:
                    line_number += 2
                continue
        # Skip ahead 1 line by default if first value is lesser than second in last CMP
        elif line.startswith("IFLR"):
            if not greater and not last_cmp:
                if len(line.split()) > 1:
                    line_number += int(line.split()[1]) + 1
                else:
                    line_number += 2
                continue
        # Call and Return
        elif line.startswith("CALL"):
            """
            CALL is basically used to hand over to the other file, like the controls
            """
            original_lines = lines # Store the lines from og file first
            return_line = line_number

            with open(line.split()[1], "r") as f: # Then open and read new file
                lines = [x.strip("\n")for x in f.readlines()if not x.strip().startswith(";")]
            for i, line in enumerate(lines):
                if line.startswith("LOOP"):
                    labels[line.split()[1].rstrip(":")] = i  # Just get label here so that loops can jump backward and forward

            line_number = -1
        elif line.startswith("RETURN"):
            """
            RETURN basically returns to the og file.
            """
            lines = original_lines # When returning
            line_number = return_line # Just change line number to the return line to return there
        elif line.startswith("LOOP"):
            pass
        # Some hdd specific instructions
        elif line.startswith("COSLOT"): # Clears every occupied slot in HDD (Well technically, in reality it clears every slot, but who cares I called it CO for Clear Occupied)
            hdd.seek(0)
            hdd.write(b"\x00\x00\x00\x00" * 1397098)
        elif line.startswith("CFSLOT"): # Clear a specifc slot eg. CFSLOT HA1
            slot = line.split()[1].rstrip(",")
            if slot.startswith("H"):
                write_hdd(slot, "")
            else:
                print("\nERROR\nCFSLOT can only clear HDD slots.")
        else:
            unknown = line.split()[0].strip('"')
            print(f"\nERROR \n'{line}'\nUnknown instruction: '{unknown}'")

        line_number += 1
    except KeyError as e: # Catch if user tries to read/write on memory slots that don't exist
        print(f"\nSEGFAULT \n'{line}'\nMemory slot/register does not exist: {e.args[0]}")
        break
    except Exception as e:
        traceback_info = traceback.extract_tb(e.__traceback__)
        last = traceback_info[-1]
        print(f"\n\n\nOH NO!")
        print("I'm sorry :(")
        print("The interpreter encountered an error.") # Because the programmer is so bad at coding D:
        print("Please make an issue in github :), or even better fix it and PR :D")
        print("Error:")
        print(e)
        print("More information:")
        print(f"Line number: {last.lineno}")
        print(f"Line: {last.line}")
        break
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
hdd.close()
