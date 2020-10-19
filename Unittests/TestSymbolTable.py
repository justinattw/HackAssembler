import unittest

from Assembler.SymbolTable import SymbolTable


class TestParserClass(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.symbol_table = SymbolTable()
        cls.symbol_table_2 = SymbolTable()
        cls.symbol_table_3 = SymbolTable()

    def test_init_symbol_table(self):
        """
        Assert that the SymbolTable is initialised with 23 default symbols.
        """
        self.assertEqual(len(self.symbol_table), 23)

    def test_contains_method_with_existent_symbol_returns_true(self):
        """
        Testing that the SymbolTable().contains method will verify that a Symbol is an existent Key in the SymbolTable
        dictionary.
        """
        # Assert that symbols that are initialised symbols are in the SymbolTable
        self.assertTrue(self.symbol_table.contains("R0"))
        self.assertTrue(self.symbol_table.contains("R1"))
        self.assertTrue(self.symbol_table.contains("R2"))
        self.assertTrue(self.symbol_table.contains("R3"))
        self.assertTrue(self.symbol_table.contains("R4"))
        self.assertTrue(self.symbol_table.contains("R5"))
        self.assertTrue(self.symbol_table.contains("R6"))
        self.assertTrue(self.symbol_table.contains("R7"))
        self.assertTrue(self.symbol_table.contains("R8"))
        self.assertTrue(self.symbol_table.contains("R9"))
        self.assertTrue(self.symbol_table.contains("R10"))
        self.assertTrue(self.symbol_table.contains("R11"))
        self.assertTrue(self.symbol_table.contains("R12"))
        self.assertTrue(self.symbol_table.contains("R13"))
        self.assertTrue(self.symbol_table.contains("R14"))
        self.assertTrue(self.symbol_table.contains("R15"))
        self.assertTrue(self.symbol_table.contains("SCREEN"))
        self.assertTrue(self.symbol_table.contains("KBD"))
        self.assertTrue(self.symbol_table.contains("SP"))
        self.assertTrue(self.symbol_table.contains("LCL"))
        self.assertTrue(self.symbol_table.contains("ARG"))
        self.assertTrue(self.symbol_table.contains("THIS"))
        self.assertTrue(self.symbol_table.contains("THAT"))

    def test_contains_method_with_non_existent_symbol_returns_false(self):
        """
        Testing that the SymbolTable().contains method will verify that a Symbol is an existent Key in the SymbolTable
        dictionary.
        """
        # Assert that symbols that are not initialised symbols/ have not been added to the symbol table are not in
        # the symbol table
        self.assertFalse(self.symbol_table.contains("nonExistentSymbol"))
        self.assertFalse(self.symbol_table.contains("R00"))
        self.assertFalse(self.symbol_table.contains("fakeSymbol"))
        self.assertFalse(self.symbol_table.contains("sys.init"))

    def test_add_symbol_method(self):
        """
        Testing that the SymbolTable().contains method will verify that a Symbol is an existent Key in the SymbolTable
        dictionary.
        """
        # Assert that the pre-determined symbols are initialised with the symbol table
        pass





if __name__ == "__main__":
    unittest.main()
