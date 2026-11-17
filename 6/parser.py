"""
nand2tetris project 6, the Hack assembler.
stough F26

This is the Parser module specified in Ch. 6 
without the ability to handle symbols.
"""

from enum import Enum

class InstructionType(Enum):
    A_INSTRUCTION = 1
    C_INSTRUCTION = 2
    L_INSTRUCTION = 3
    NO_TYPE = 4

class Parser(object):
    def __init__(self, input_file):
        self.lines = []
        self.cur = -1
        self.inputfile = input_file
        self.preprocessFile()
        self.curtype: InstructionType = InstructionType.NO_TYPE
        self.curdest = None
        self.cursymbol = None
        self.curcomp = None
        self.curjump = None

    def hasMoreLines(self):
        # self.lines is a list of strings, one per line, with whitespace and comments removed
        return self.cur < len(self.lines)-1

    def advance(self):
        # if we have more line, then update self.cur and interpret the line, otherwise do nothing
        self.cur += 1
        self.interpretLine()

    def instructionType(self):
        return self.curtype

    def curLine(self):
        assert self.cur > 0 and self.cur < len(self.lines), 'No current line to report'
        return str(self.lines[self.cur])
    
    def symbol(self):
        '''
        Returnes the symbol or decimal as a string: (xxx) or @xxx returns xxx
        '''
        assert self.curtype is InstructionType.A_INSTRUCTION or \
            self.curtype is InstructionType.L_INSTRUCTION, \
            f'symbol only for A or L type, not {self.lines[self.cur]}'
        return self.cursymbol

    def dest(self):
        '''
        Returns the destination part of a C-instruction as a string.
        ADM, 8 possibilities: None, M, D, DM, A, AM, AD, AMD
        '''
        assert self.curtype is InstructionType.C_INSTRUCTION, \
            f'dest only for C-type, not {self.lines[self.cur]}'
        return self.curdest

    def comp(self):
        '''
        Returns one of 28 posibilities for the computation part, to the right of the '='
        and to the left of the ';'. eg 'D=D+1;JLE' returns 'D+1'
        '''
        assert self.curtype is InstructionType.C_INSTRUCTION, \
            f'comp only for C-type, not {self.lines[self.cur]}'
        return self.curcomp

    def jump(self):
        '''
        Returns the jump part of a C-instruction as a string. 8 posibilities, whatever
        is to the right of the ';' in a C-instruction. eg 'D=D+1;JLE' returns 'JLE'
        '''
        assert self.curtype is InstructionType.C_INSTRUCTION, \
            f'jump only for C-type, not {self.lines[self.cur]}'
        return self.curjump

    def preprocessFile(self):
        '''
        Preprocess the input file, removing comments and whitespace, and storing
        the lines in self.lines.
        '''
        try:
            all_lines = open(self.inputfile, 'r').read().split('\n')
        except FileNotFoundError:
            print(f'Read Error: could not read {self.inputfile}.')
        except Exception as e:
            print(f'Unexpected Error: {e}')
        # filter the lines:
        for line in all_lines:
            line = line.lstrip().rstrip()
            if line == '' or line[0] == '/':
                continue
            self.lines.append(line)

    def interpretLine(self):
        '''
        Interpret the current line. That is, determine all the cursymbol, 
        curdest, curcomp, and curjump values. Also set the curtype.
        '''
        line = str(self.lines[self.cur])
        if line[0] == '@':
            self.curtype = InstructionType.A_INSTRUCTION
            self.cursymbol = line[1:]
            # set curcomp, curdest, and curjump to None or '0's as appropriate
            self.curdest = '000'
            self.curjump = '000'
            self.curcomp = '0000000'

        elif line[0] == '(':
            self.curtype = InstructionType.L_INSTRUCTION
            self.cursymbol = line[1:-1] # strip the parens
            # set curcomp, curdest, and curjump to None or '0's as appropriate
            self.curdest = '000'
            self.curjump = '000'
            self.curcomp = 7*'0'

        else:
            # the harder one here. Set the type to C, the symbol to None.
            self.curtype = InstructionType.C_INSTRUCTION
            self.cursymbol = None
            # Set the curcomp, curdest, and curjump values. The line is of the form:
            # dest=comp;jump, where dest and jump are optional. If dest is missing.
            # You can check if '=' is in the line, by   if '=' in line: do stuff
            if '=' in line:
                dest, remainder = line.split('=', 1)
            else:
                dest = '000'
                remainder = line

            if ';' in remainder:
                comp, jump = remainder.split(';', 1)
            else:
                comp = remainder
                jump = '000'

            self.curdest = dest
            self.curcomp = comp
            self.curjump = jump