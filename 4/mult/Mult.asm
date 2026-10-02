// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
// The algorithm is based on repetitive addition.

// Initialize R2 at O
    @R2
    M=0

// set to finish if R0 or R1 equals 0
    @R0
    D=M
    @END
    D;JEQ

    @R1
    D=M
    @END
    D;JEQ

// set up a counter to add up to R0 many times
    @R0
    D=M
    @counter
    M=D

// Make a loop of repeated additions
(LOOP)
//check is counter is 0
    @counter
    D=M
    @END
    D;JEQ

// add R1 to R2
    @R1
    D=M
    @R2
    M=D+M

    @counter
    M=M-1

    @LOOP
    0;JMP

(END)
    @END
    M;JMP
