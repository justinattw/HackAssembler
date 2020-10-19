#!/usr/bin/env python3

class Code:
    """
    The Code class contains static attributes of the (Comp)utation, (Dest)ination, and Jump codes of the Hack language.
    More can be found under 'assets/'.
    """

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
        """
        The 'a' op code in the Hack computer determines whether to access the 'A' or the 'M' register, but not both.
        You can see this in the _comp_codes dictionary, where no Comp function includes both 'A' and 'M'.
        :param code: the Computation code to be parsed
        :return: the 'a' op code, '1' accesses the M-register, '0' accesses the A-register
        """
        if "M" in code:
            return "1"
        else:
            return "0"

    @staticmethod
    def decode_comp_code(code) -> str:
        """
        The (Comp)utation code specifies to the Hack computer which computation to perform. It chooses from a series of
        17 arithmetic operations, represented by 7-bit binary numbers (1-bit op code and 6-bit comp code).
        :param instruction: The Comp code to be converted to 7-bit binary
        :return: a string of a 7-bit binary number (1-bit op code and 6-bit comp code).
        """
        a_code = Code.decode_comp_code_a(code)
        comp_code = Code._comp_codes[code]
        return a_code + comp_code

    @staticmethod
    def decode_dest_code(code) -> int:
        """
        The Dest code specifies to Hack computer where the output of the CPU is stored (in the A, M, D, or two of/ all
        registers). There are 8 different combinations of where the output can be stored, represented by a 3-bit binary
         number. In this method, we simply return an integer representing the Dest option.
        :param code: The DEst code to be evaluated.
        :return: the integer (0 < x < 7) associated with the Dest code, to be converted to 3-bit binary outside of
        scope.
        """
        if not code:
            code = "null"
        assert code in Code._dest_codes
        return Code._dest_codes.index(code)

    @staticmethod
    def decode_jump_code(code) -> int:
        """
        The Jump code specifies to Hack computer criteria for the program to 'jump' to another instruction in the ROM
        (technically, jumping towards an address in the ROM). There are 8 different criteria for Jump, which can be
        represented by a 3-bit binary number. In this method, we simply return an integer represending the Jump option.
        :param code: The Jump code to be evaluated.
        :return: the integer (0 < x < 7) associated with the Jump code, to be converted to 3-bit binary outside of
        scope.
        """
        if not code:
            code = "null"
        assert code in Code._jump_codes
        return Code._jump_codes.index(code)
