; Pseudo Random Number Generator Made by: https://github.com/CoolGuy158-Git
; A NASM stdlib for generating random numbers from 1-999 (Well max is 999 can't guarantee it will actually hit 500, depends on your seed)
; Seed is gonna be stored in Z100, output is gonna be in Z101 and Z102 is going to be used in checking if num is over 248, Z103 is for storing the og seed
; Make sure to leave those memory slots unallocated for when you need randomness
; Also make sure seed inputted is 1-491 anything higher will yea segfault

; OG num must not go above 498 so that when multiplied to 2 won't go over 500
SET Z102 498

; do x = (x*2)+3

MOV Z100 Z101
; Copy values of seed to Z101
MOV Z100 Z103
; Copy values of seed to Z103 for later checking

CMP Z101 Z102
IFLR
SUB Z101 497
; Z101 is 498 or higher, subtract by 497 to keep the thing within range so we wont get segfault
; Now theoretically user could input something much much higher so that even when subtracted its still higher than 248 but come on its their fault

MUL Z101 2
SET Z102 900
; Now set this to 900 so that it only add if less than 900
CMP Z101 Z102
IFLR
ADD Z101 3

; Compare og seed to the result, if equal add 1, this makes it slightly longer before eventually looping
CMP Z103 Z101
INEQ
ADD Z101 1

MOV Z101 Z100
; The newly generated thing is also gonna be the new seed
; Now return to main file
RETURN