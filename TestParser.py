import unittest

from Parser import Parser

class TestParserClass(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.label_1 = "(LOOP)"
        cls.label_2 = "(INFINITE_LOOP)"
        cls.label_3 = "(LOOP_123)"

        cls.address_1 = "@21"
        cls.address_2 = "@0"
        cls.address_3 = "@900"

        cls.variable_1 = "@START"
        cls.variable_2 = "@end"
        cls.variable_3 = "@INFINITE_LOOP"
        cls.variable_4 = "@LOOP_123"

        cls.c_instruction_full_1 = "D=M;JMP"
        cls.c_instruction_full_2 = "MD=D-1;JNE"
        cls.c_instruction_full_3 = "AMD=D|M;JLT"
        cls.c_instruction_full_4 = "AM=A;JGE"
        cls.c_instruction_full_5 = "D=A-D;JEQ"
        cls.c_instruction_full_6 = "AD=D&M;JLE"
        cls.c_instruction_full_7 = "A=!D;JGT"
        cls.c_instruction_full_8 = "A=A+1;JGT"

        cls.c_instruction_comp_only_1 = "0"
        cls.c_instruction_comp_only_2 = "-1"
        cls.c_instruction_comp_only_3 = "!D"
        cls.c_instruction_comp_only_4 = "!M"
        cls.c_instruction_comp_only_5 = "-M"
        cls.c_instruction_comp_only_6 = "A+1"
        cls.c_instruction_comp_only_7 = "M"

        cls.c_instruction_comp_and_jump = "0;JMP"

        cls.c_instruction_dest_and_comp_1 = "D=M"
        cls.c_instruction_dest_and_comp_2 = "MD=M-1"

    def test_parse_label_instruction(self):

        parse_label_1 = Parser.parse_label_instruction(self.label_1)
        parse_label_2 = Parser.parse_label_instruction(self.label_2)
        parse_label_3 = Parser.parse_label_instruction(self.label_3)

        self.assertEqual(parse_label_1, "LOOP")
        self.assertEqual(parse_label_2, "INFINITE_LOOP")
        self.assertEqual(parse_label_3, "LOOP_123")

        with self.assertRaises(AssertionError):
            Parser.parse_label_instruction(self.address_1)
            Parser.parse_label_instruction(self.address_2)
            Parser.parse_label_instruction(self.address_3)

            Parser.parse_label_instruction(self.variable_1)
            Parser.parse_label_instruction(self.variable_2)
            Parser.parse_label_instruction(self.variable_3)
            Parser.parse_label_instruction(self.variable_4)

    def test_parse_c_instruction_comp(self):

        comp_1 = Parser.parse_c_instruction_comp(self.c_instruction_full_1)
        comp_2 = Parser.parse_c_instruction_comp(self.c_instruction_full_2)
        comp_3 = Parser.parse_c_instruction_comp(self.c_instruction_full_3)
        comp_4 = Parser.parse_c_instruction_comp(self.c_instruction_full_4)
        comp_5 = Parser.parse_c_instruction_comp(self.c_instruction_full_5)
        comp_6 = Parser.parse_c_instruction_comp(self.c_instruction_full_6)
        comp_7 = Parser.parse_c_instruction_comp(self.c_instruction_full_7)
        comp_8 = Parser.parse_c_instruction_comp(self.c_instruction_full_8)

        self.assertEqual(comp_1, "M")
        self.assertEqual(comp_2, "D-1")
        self.assertEqual(comp_3, "D|M")
        self.assertEqual(comp_4, "A")
        self.assertEqual(comp_5, "A-D")
        self.assertEqual(comp_6, "D&M")
        self.assertEqual(comp_7, "!D")
        self.assertEqual(comp_8, "A+1")

        comp_only_1 = Parser.parse_c_instruction_comp(self.c_instruction_comp_only_1)
        comp_only_2 = Parser.parse_c_instruction_comp(self.c_instruction_comp_only_2)
        comp_only_3 = Parser.parse_c_instruction_comp(self.c_instruction_comp_only_3)
        comp_only_4 = Parser.parse_c_instruction_comp(self.c_instruction_comp_only_4)
        comp_only_5 = Parser.parse_c_instruction_comp(self.c_instruction_comp_only_5)
        comp_only_6 = Parser.parse_c_instruction_comp(self.c_instruction_comp_only_6)
        comp_only_7 = Parser.parse_c_instruction_comp(self.c_instruction_comp_only_7)

        self.assertEqual(comp_only_1, "0")
        self.assertEqual(comp_only_2, "-1")
        self.assertEqual(comp_only_3, "!D")
        self.assertEqual(comp_only_4, "!M")
        self.assertEqual(comp_only_5, "-M")
        self.assertEqual(comp_only_6, "A+1")
        self.assertEqual(comp_only_7, "M")

        comp_and_dest_1 = Parser.parse_c_instruction_comp(self.)



if __name__ == "__main__":
    unittest.main()