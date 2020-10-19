#!/usr/bin/env python3

import sys
from typing import List

from SymbolTable import SymbolTable
from Parser import Parser
from Code import Code


class Assembler:
    """
    The Assembler class contains the main logic of the Hack Assembler.
    """

    def __init__(self):
        self.symbol_address = 16
        self.symbol_table = SymbolTable()  # Initialise the default symbol table

    def assemble(self, asm_infile):
        """
        The Assemble method of the assembler is where all of the magic happens. It contains four abstracted methods
        to simply read the text file, conduct a first pass to parse all labels in the file, conduct a second pass to
        translate A- and C- instructions to 16-bit binary code, then output to a '.hack' text file.
        :return:
        """
        file: List[str] = self.read_file(asm_infile)
        self.first_pass(file)
        file = self.second_pass(file)
        self.write_file(file, asm_infile)
        print("The assembly was a success, thank you for using the Hack Assembler.")

    def first_pass(self, file):
        """
        In the first pass, the entire program is scanned. For each Label 'L instruction' (xxx), add the pair
        (xxx, line_num) to the symbol table.
        :param: the input 'file' to be parsed (actually a List of strings).
        """
        line_num = 0
        for line in file:
            line = Parser.clean_line(line)  # Strip comments and whitespace
            if not line:  # If line is empty, then it is not an instruction
                continue
            if Parser.is_label_instruction(line):
                self.label_instruction_to_symbol_table(line, line_num)
                continue  # To skip the line_num increment
            line_num += 1  # Line number is only counted if line is A-/C-instruction (not blank or a label)

    def second_pass(self, file):
        """
        In the second pass, the assembler iterates through all the script and parses only A and C instructions.

        For each line:
        - If it is an A instruction variable, the program try to append the variable/symbol:address pair to the
        SymbolTable. The program then indexes into SymbolTable to get the address of the Symbol.
        - If it is an A instruction address, the program simply gets the address of the Symbol.
        - If it is a C instruction, the program parses the 'a' op code, comp, dest, and jump codes of the instruction.

        Each line is then appended to a list 'out_lines' containing a list of strings of machine code (binary numbers).

        :file:
        :return: list of strings of 16-bit binary numbers sequentially representing the A- and C- instructions.
        """
        out_lines = []

        line_num = 0
        for line in file:
            line = Parser.clean_line(line)
            out_line = ""

            if not line:
                continue

            if Parser.is_label_instruction(line):
                continue

            if Parser.is_a_instruction(line):
                self.a_instruction_to_symbol_table(line)
                out_line = self.a_instruction_to_binary(line, out_line)

            elif Parser.is_c_instruction(line):
                out_line = self.c_instruction_to_binary(line, out_line)

            else:
                raise Exception(f"Line \"{line}\": Parser has not identified an A or C instruction")

            line_num += 1
            out_line += "\n"
            out_lines.append(out_line)

        return out_lines

    def a_instruction_to_symbol_table(self, line):
        """
        Parses an A instruction (e.g. @21 or @LOOP). If it is an address, ignore. If it is a variable, add variable
        and corresponding symbol address (maintained in self Assembly instance) to the self SymbolTable dictionary.
        :param line: A instruction line to be parsed and appended to SymbolTable
        :return: a Bool value representing whether the append to SymbolTable was a success.
        """
        if Parser.is_a_instruction_is_address(line):
            return True

        elif Parser.is_a_instruction_is_variable(line):
            variable_string = Parser.parse_a_instruction_variable(line)
            symbol_added = self.symbol_table.add_symbol(variable_string, self.symbol_address)
            if symbol_added:
                self.symbol_address += 1
            if self.symbol_table.get_address(variable_string):
                return True
            else:
                return False
        else:
            raise Exception("A instruction identified, but cannot parse address or variable.")

    def label_instruction_to_symbol_table(self, line, line_num):
        label_string = Parser.parse_label_instruction(line)
        self.symbol_table.add_symbol(label_string, line_num)

    def a_instruction_to_binary(self, line, out_line):
        """
        Converts a line of A instruction to a 16-bit binary string
        :param line: A instruction line to be converted
        :param out_line: the output 16-bit binary string to be returned
        :return: a 16-bit binary string representing the original assembly language A instruction
        """

        out_line += "0"  # A instructions begin with "0" and end with a 15-bit address.

        if Parser.is_a_instruction_is_address(line):
            address_string = Parser.parse_a_instruction_address(line)
            address_int = int(address_string)
            address_binary = self.to_binary_number(address_int, 15)

        elif Parser.is_a_instruction_is_variable(line):
            variable_string = Parser.parse_a_instruction_variable(line)
            address_int = self.symbol_table.get_address(variable_string)
            address_binary = self.to_binary_number(address_int, 15)

        else:
            raise Exception("A instruction identified, but cannot identify address or variable")

        out_line += address_binary

        return out_line

    def c_instruction_to_binary(self, line, out_line):
        """
        Converts a line of C instruction to a 16-bit binary string
        :param line: C instruction line to be converted
        :param out_line: the output 16-bit binary string to be returned
        :return: a 16-bit binary string representing the original assembly language C instruction
        """

        out_line += "111"  # C instructions begin with "111" in binary, then end with 'a' op code, comp, dest, jump.

        comp_code = Parser.parse_c_instruction_comp(line)
        comp_binary = Code.decode_comp_code(comp_code)

        dest_code = Parser.parse_c_instruction_dest(line)
        dest_int = Code.decode_dest_code(dest_code)
        dest_binary = self.to_binary_number(dest_int, 3)

        jump_code = Parser.parse_c_instruction_jump(line)
        jump_int = Code.decode_jump_code(jump_code)
        jump_binary = self.to_binary_number(jump_int, 3)

        out_line += comp_binary + dest_binary + jump_binary

        return out_line

    def to_binary_number(self, integer: int, bits: int) -> str:
        """
        Converts an integer to binary
        :param integer: Int to be turned to binary
        :param bits: Number of bits in binary number
        :return: a string of an x-bit binary number representing the integer
        """
        binary = bin(integer)[2:]
        binary_fill = binary.zfill(bits)
        return str(binary_fill)

    def update_symbol_table(self, symbol, address=None):
        """
        Updates symbol table with a Symbol:Address key:value pair. If the address is not given, it will take the
        object instance's symbol_address counter (self.symbol_address
        :param symbol: Symbol to be added to Symbol Table e.g. (LOOP), @LOOP
        :param address: 
        :return:
        """
        if not address:
            address = self.symbol_address
        symbol_added = self.symbol_table.add_symbol(symbol, address)
        self.symbol_address += 1
        return symbol_added

    def read_file(self, filename) -> List[str]:
        """
        :param filename: filename of the text file to be read
        :return: a list of strings for each line in the file.
        """
        file = open(filename, "r")
        lines = file.readlines()
        file.close()
        return lines

    def write_file(self, lines, in_filename, out_filename="", out_dir="out_hack/"):
        """
        :param lines: a list of lines to be written to a text file
        :param in_filename: if out_filename is not defined, in_filename is used to generate the out_filename
        :param out_filename: out_filename is an optional
        :param out_dir: out directory for which to write output .hack file to
        :return:
        """
        if not out_filename:
            out_filename = self.get_out_filename(in_filename, out_dir)
        if not out_filename.endswith(".hack"):
            raise Exception(f"Output filename {out_filename} must be a '.hack' file")
        outfile = open(out_filename, "w")
        outfile.writelines("%s" % i for i in lines)
        outfile.close()

    def get_out_filename(self, in_filename: str, out_dir: str):
        """
        :param in_filename: take the in_filename and auto-generate the out_filename with .hack extension
        :param out_dir: out directory for which to write output .hack file to
        :return: string of the out_filename
        """
        if in_filename.endswith(".asm"):
            in_filename = in_filename.replace(".asm", "")
        if "/" in in_filename:  # If filename contains a path
            filepath = in_filename.split("/")
            in_filename = filepath[-1]
        out_filename = out_dir + in_filename + ".hack"
        return out_filename


if __name__ == '__main__':

    if len(sys.argv) != 2:
        print("PROGRAM NOT RUN. Usage: python Assembler.py Program.asm")
        exit()

    asm_file = sys.argv[1]
    hack_assembler = Assembler()
    hack_assembler.assemble(asm_file)
