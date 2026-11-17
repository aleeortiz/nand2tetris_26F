

class SymbolTable():
    def __init__(self) -> None:
        self.symT = {}
        self.initsymT()
    
    def addEntry(self, symbol, address):
        self.symT[symbol] = address
    
    def contain(self, symbol):
        return symbol in self.symT
    
    def getAddress(self, symbol):
        assert symbol in self.symT, f'Error No Symbol{symbol}'
        return self.symT[symbol]
    
    def initsymT(self):
        self.symT.update({f'R{i}':i for i in range(16)})
        self.symT['SCREEN'] = 16384
        
    