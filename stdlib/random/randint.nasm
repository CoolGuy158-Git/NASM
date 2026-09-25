; Pseudo Random Number Generator Made by: https://github.com/CoolGuy158-Git
; Basically a copy of the normal PRNG but made to have a specific range.
; Seed is gonna be stored in Z105, output is gonna be in Z106 and Z107 is going to be used in checking if num is over the specified range, Z108 is for storing the og seed, Z109 is used for subtracting
; Put the specific range in Z107
; Meaning it does 1-Specified Range

; OG num must not go above specified range so that when multiplied to 2 won't go over 500
; do x = (x*2)+3

MOV Z105 Z106
; Copy values of seed to Z106
MOV Z105 Z108
; Copy values of seed to Z108 for later checking

MUL Z106 2
ADD Z106 3

CMP Z106 Z107
IFLR
SSLOT Z106 Z107


; Compare og seed to the result, if equal add 1, this makes it slightly longer before eventually looping
CMP Z108 Z106
INEQ
ADD Z106 1

MOV Z106 Z105
; The newly generated thing is also gonna be the new seed
; Now return to main file
RETURN