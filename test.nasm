; Test

LOOP hello:
ADD A1 1
PRINT A1 [NLNS]
; NLNS means new line aka NewLiNeS
BNC hello 5

; Lets try to improvise cuz we have no delay/sleep command cuz the developer was lazy
ADD A2 9
; Just do this random thing 200000 times
LOOP delay:
CMP A2 A3
BNC delay 2000000

ADD A2 "D"
PRINT A2
ADD A2 "O"
PRINT A2
ADD A2 "N"
PRINT A2
ADD A2 "E"
PRINT A2
ADD A2 "!"
PRINT A2 [NLNS]

; Get input

ADD A2 "I"
PRINT A2
ADD A2 "N"
PRINT A2
ADD A2 "P"
PRINT A2
ADD A2 "U"
PRINT A2
ADD A2 "T"
PRINT A2
ADD A2 " "
PRINT A2
ADD A2 "6"
PRINT A2
ADD A2 " "
PRINT A2
ADD A2 "C"
PRINT A2
ADD A2 "H"
PRINT A2
ADD A2 "A"
PRINT A2
ADD A2 "R"
PRINT A2
ADD A2 " "
PRINT A2
ADD A2 "W"
PRINT A2
ADD A2 "O"
PRINT A2
ADD A2 "R"
PRINT A2
ADD A2 "D"
PRINT A2 [NLNS]
INP A3, A4, A5, A6, A7
PRINT A3
PRINT A4
PRINT A5
PRINT A6
PRINT A7 [NLNS]

; Now try like printing while typing
ADD A2 "O"
PRINT A2
ADD A2 "N"
PRINT A2
ADD A2 "C"
PRINT A2
ADD A2 "E"
PRINT A2
ADD A2 " "
PRINT A2
ADD A2 "M"
PRINT A2
ADD A2 "O"
PRINT A2
ADD A2 "R"
PRINT A2
ADD A2 "E"

; Every input store in mem and print that
INP A3
PRINT A3
INP A4
PRINT A4
INP A5
PRINT A5
INP A6
PRINT A6
INP A7
PRINT A7