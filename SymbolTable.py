#!/usr/bin/env python3

class SymbolTable(dict):

    def __init__(self):
        """
        """
        super().__init__()
        self.update({"R0": 0, "R1": 1, "R2": 2, "R3": 3, "R4": 4, "R5": 5, "R6": 6, "R7": 7, "R8": 8, "R9": 9,
                     "R10": 10, "R11": 11, "R12": 12, "R13": 13, "R14": 14, "R15": 15,
                     "SCREEN": 0x4000, "KBD": 0x6000,
                     "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4
                     })

    def contains(self, symbol):
        return symbol in self

    def add_symbol(self, symbol, address):
        if self.contains(symbol):
            return False
        else:
            self.update({symbol: address})
            return True

    def get_address(self, symbol):
        return self[symbol]
