#!/usr/bin/env python3

class Code:

    # Static class attributes
    _jump_codes = ["null", "JGT", "JEQ", "JGE", "JLT", "JNE", "JLE", "JMP"]

    _dest_codes = ["null", "M", "D", "MD", "A", "AM", "AD", "AMD"]

    _comp_codes = {"0": "101010", "1": "111111", "-1": "111010", "D": "001100", "A": "110000", "M": "110000",
                   "!D": "001101", "!A": "110001", "!M": "110001", "-D": "001111", "-A": "110011", "-M": "110011",
                   "D+1": "011111", "A+1": "110111", "M+1": "110111", "D-1": "001110", "A-1": "110010", "M-1": "110010",
                   "D+A": "000010", "D+M": "000010", "D-A": "010011", "D-M": "010011", "A-D": "000111", "M-D": "000111",
                   "D&A": "000000", "D&M": "000000", "D|A": "010101", "D|M": "010101"}

    @staticmethod
    def decode_comp_code_a(code):
        if "M" in code:
            return "1"
        else:
            return "0"

    @staticmethod
    def decode_comp_code(code):
        a_code = Code.decode_comp_code_a(code)
        comp_code = Code._comp_codes[code]
        return a_code + comp_code

    @staticmethod
    def decode_jump_code(code):
        if not code:
            code = "null"
        assert code in Code._jump_codes
        return Code._jump_codes.index(code)

    @staticmethod
    def decode_dest_code(code):
        if not code:
            code = "null"
        assert code in Code._dest_codes
        return Code._dest_codes.index(code)



