import unittest

from Assembler.Code import Code


class TestParserClass(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.var = "Hello World"


if __name__ == "__main__":
    unittest.main()
