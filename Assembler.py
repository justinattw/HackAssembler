#!/usr/bin/env python3

import sys
from typing import List

from SymbolTable import SymbolTable
from Parser import Parser
from Code import Code


class Assembler:
    """
    """
    def __init__(self):
        self.symbol_address = 16
        self.symbol_table = SymbolTable()  # Initialise the default symbol table

    def assemble(self, asm_infile):
        """
        The Assemble method of the assembler is where all of the magic happens.
        :return:
        """
        file: List[str] = self.read_file(asm_infile)
        self.first_pass(file)
        file = self.second_pass(file)
        self.write_file(file, asm_infile)

    def first_pass(self, lines):
        """
        In the first pass, the entire program is scanned. For each Label 'L instruction' (xxx), add the pair
        (xxx, line_num) to the symbol table.
        """
        line_num = 0
        for line in lines:
            line = Parser.clean_line(line)

            if not line:
                continue

            if Parser.is_label_instruction(line):
                self.label_instruction_to_symbol_table(line, line_num)
                continue  # To skip the line_num increment

            line_num += 1

    def second_pass(self, file):
        """
        In the second pass, the assembler iterates through all the script and parses only A and C instructions.
        :return:
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
                out_line = self.a_instruction_to_binary(line, out_line, line_num)

            elif Parser.is_c_instruction(line):
                out_line = self.c_instruction_to_binary(line, out_line)

            else:
                raise Exception(f"Line \"{line}\": Parser has not identified an A or C instruction")

            line_num += 1
            out_line += "\n"
            out_lines.append(out_line)

        return out_lines

    def a_instruction_to_symbol_table(self, line):
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

    def a_instruction_to_binary(self, line, out_line, line_num):

        out_line += "0"

        if Parser.is_a_instruction_is_address(line):  # Syntax is
            address_string = Parser.parse_a_instruction_address(line)
            address_int = int(address_string)
            address_binary = self.to_binary_number(address_int, 15)

        elif Parser.is_a_instruction_is_variable(line):
            variable_string = Parser.parse_a_instruction_variable(line)
            print(f"{variable_string}: ", end="")
            address_int = self.symbol_table.get_address(variable_string)
            print(f"{address_int}: ", end="")
            address_binary = self.to_binary_number(address_int, 15)
            print(f"{address_binary}:")

        else:
            raise Exception("A instruction identified, but cannot identify address or variable")

        out_line += address_binary

        return out_line

    def c_instruction_to_binary(self, line, out_line):

        out_line += "111"

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
        binary = bin(integer)[2:]
        binary_fill = binary.zfill(bits)
        return str(binary_fill)

    def update_symbol_table(self, symbol, address=None):
        if not address:
            address = self.symbol_address
        symbol_added = self.symbol_table.add_symbol(symbol, address)
        self.symbol_address += 1
        return symbol_added

    def read_file(self, filename):
        file = open(filename, "r")
        lines = file.readlines()
        file.close()
        return lines

    def write_file(self, lines, in_filename, out_filename=""):
        if not out_filename:
            out_filename = self.get_out_filename(in_filename)
        outfile = open(out_filename, "w")
        outfile.writelines("%s" % i for i in lines)
        outfile.close()

    def get_out_filename(self, in_filename: str):
        if in_filename.endswith(".asm"):
            return in_filename.replace(".asm", ".hack")
        else:
            return in_filename


if __name__ == '__main__':

    if len(sys.argv) != 2:
        print("PROGRAM NOT RUN. Usage: python Assembler.py Program.asm")
        exit()

    asm_file = sys.argv[1]
    hack_assembler = Assembler()
    hack_assembler.assemble(asm_file)
