#!/usr/bin/env python3

import re


class Parser:
    """
    Parser, is a class that provides helper functions to parse the Hack syntax. More specifically, it provides matching
    methods
    """

    @staticmethod
    def clean_line(line):
        """
        :return: line with whitespace and comments removed
        """
        line = re.sub('//.*', "", line)  # remove comments in current line
        line = re.sub(r"\s+", "", line)  # remove all whitespace in current line
        return line

    @staticmethod
    def is_a_instruction(line):
        """
        Composite of all is_a_instruction methods to identify if the code line is an A instruction
        :return: either an object or null
        """
        return Parser.is_a_instruction_is_address(line) or Parser.is_a_instruction_is_variable(line)

    @staticmethod
    def is_a_instruction_is_address(line):
        """
        The a_instruction address has the syntax @num, e.g. @21
        :return: a regex Match object
        """
        return re.match("@[0-9]+", line)

    @staticmethod
    def is_a_instruction_is_variable(line):
        """
        The a_instruction variable has the syntax @string, e.g. @LOOP
        :return: a regex Match object
        """
        return re.match("@[A-Za-z0-9_.$]+", line)

    @staticmethod
    def parse_a_instruction_address(line):
        """
        Parses the address of an a_instruction
        :return: a regex Group object
        """
        assert Parser.is_a_instruction_is_address(line)
        addr = re.search(r"([0-9]+)", line)
        return addr[0]

    @staticmethod
    def parse_a_instruction_variable(line):
        """
        Parses the variable of an A instruction
        :return: a regex group object
        """
        assert Parser.is_a_instruction_is_variable(line)
        var = re.findall(r"([A-Za-z0-9_.$]+)", line)
        return var[0]

    @staticmethod
    def is_label_instruction(line):
        """
        The a_instruction label has the syntax (STRING), e.g. (LOOP)
        :return: a regex Match object
        """
        return re.match("\(([A-Za-z0-9_.$]+)\)", line)

    @staticmethod
    def parse_label_instruction(line):
        """
        Parses the variable of an A instruction
        :return: a regex group object
        """
        assert Parser.is_label_instruction(line)
        label = re.findall(r"([A-Za-z0-9_.$]+)", line)
        return label[0]

    @staticmethod
    def is_c_instruction(line):
        """
        TODO
        """
        re.match(r"", line)
        return True

    @staticmethod
    def parse_c_instruction_comp(line):
        """
        Parses the comp method of a C instruction
        :param line:
        :return:
        """
        lines = line.split("=")
        line = lines[len(lines) - 1]
        lines = line.split(";")
        line = lines[0]
        return line
        # comp = re.findall(r"([D|M|A|+|\-|0|1|!|&]+)", line)
        # if not comp:
        #     raise Exception(f"Comp line not found in command \"{line}\"")
        # return str(comp[0])

    @staticmethod
    def parse_c_instruction_dest(line):
        """
        :return:
        """
        lines = line.split("=")
        if len(lines) > 1:
            line = lines[0]
            return line
            # dest = re.findall(r"(M|D|MD|A|AM|AD|AMD)", line)
            # return str(dest[0])
        else:
            return None

    @staticmethod
    def parse_c_instruction_jump(line):
        """
        Parses the jump method of a C instruction.
        :return: a regex group object, or none
        """
        lines = line.split(";")
        if len(lines) > 1:
            line = lines[1]
            jump = re.findall(r"(JGT|JEQ|JGE|JLT|JNE|JLE|JMP)", line)
            return jump[0]
        else:
            return None

    @staticmethod
    def valid_out_line_length(line):
        """
        Checks if the write out line string is 16 characters long (16 bits)
        :return: boolean
        """
        return len(line) == 16
