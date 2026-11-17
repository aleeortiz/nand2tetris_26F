"""
Hack Assembler, without the symbol table. 
Stough, F26

The idea is to use the Parser to parse each relevant line,
and use the Code to translate binary.
"""

from parser import Parser, InstructionType
from code import Code
from SymbolTable import SymbolTable
import os
import sys

def assembleNoL(filename):
    parse = Parser(filename)
    code = Code()

    print(f'{filename} has {len(parse.lines)} code lines.\n')

    outlines = []
    while parse.hasMoreLines():
        # Process the line, and append some binary string to outlines.
        ### THIS IS WHERE YOU WILL DO THE WORK. and get ride of the above 'pass' statement when you do.
        parse.advance()

        #set instruction type
        instruction_type = parse.instructionType()

        #translate A instruction
        if instruction_type == InstructionType.A_INSTRUCTION:
            address = int(parse.symbol())
            binary = '0' + format(address, '015b')
            outlines.append(binary)

        #translate C instruction
        elif instruction_type == InstructionType.C_INSTRUCTION:
            comp_bits = code.comp(parse.comp())
            dest_bits = code.dest(parse.dest())
            jump_bits = code.jump(parse.jump())

            binary = '111' + comp_bits + dest_bits + jump_bits
            outlines.append(binary)

        elif instruction_type == InstructionType.L_INSTRUCTION:
            continue

    basename, ext = os.path.splitext(filename)
    outfilename = basename + '.hack'
    with open(outfilename, 'w') as outfile:
        for line in outlines:
            outfile.write(line + '\n')
    print(f'Wrote {len(outlines)} lines to {outfilename}.\n')
        






if __name__ == '__main__':
    assembleNoL(sys.argv[1])