# Create a file named NASM.hdd on dir components
# The file contains [0000]
# Every 4 bytes = one NASM hdd cell
# mapping is:
# HA1 -> Cell 0
# HB1 -> Cell 1
# The total file size and the amount of mb the interpreter can actually use is 5mb
# We can use exactly 1,397,098
import time
import os

start = time.time()
cell_count = 26*53773
cell_size = 4

with open("../components/NASM.hdd", "wb") as file:
    file.truncate(cell_count * cell_size)
end = time.time()
elapsed = end - start
print(f"Done in {elapsed:.2f} seconds!")
size = os.path.getsize('../components/NASM.hdd')
print(f"File size: {size / 1024 / 1024:.2f} MB")