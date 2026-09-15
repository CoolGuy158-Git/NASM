; Pseudo Random Number Generator Made by: https://github.com/CoolGuy158-Git
; A NASM stdlib for generating random numbers from 1-500 (Well max is 500 can't guarantee it will actually hit 500, depends on your seed)
; Seed is gonna be stored in Z100, output is gonna be in Z101 and Z102 is going to be used in checking if num is over 248
; Make sure to leave those memory slots unallocated for when you need randomness
; Also make sure seed inputted is 1-491 anything higher will yea segfault

; OG num must not go above 248 so that when multiplied to 2 won't go over 500
SET Z102 248

; do x = (x*2)+3

MOV Z100 Z101
; Copy values of seed to Z101

CMP Z101 Z102
IFLR
SUB Z101 247
; Z101 is 248 or higher, subtract by 247 to keep the thing within range so we wont get segfault
; Now theoretically user could input something much much higher so that even when subtracted its still higher than 248 but come on its their fault

MUL Z101 2
ADD Z101 3
MOV Z101 Z100
; The newly generated thing is also gonna be the new seed
; Now return to main file
RETURN