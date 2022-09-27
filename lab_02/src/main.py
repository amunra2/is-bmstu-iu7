from re import A
from turtle import pos, position


class Rotor():
    alphabet: list
    alphabetMixed: list
    positionSymbol: str

    def __init__(self, alphabet: list, alphabetMixed: list, positionSymbol: str):
        self.alphabet = alphabet
        self.alphabetMixed = alphabetMixed
        self.positionSymbol = positionSymbol

    def getSymbolForward(self, symbol: str):
        foundPosition = (self.getSymbolPosition(self.alphabet, self.positionSymbol) + 
            self.getSymbolPosition(self.alphabet, symbol)) % (len(self.alphabet))
        foundSymbol = self.alphabetMixed[foundPosition]

        print(self.getSymbolPosition(self.alphabet, self.positionSymbol), " + ",
            self.getSymbolPosition(self.alphabet, symbol), " = ", foundPosition)

        return foundSymbol

    def getSymbolBack(self, symbol: str):
        foundPosition = (self.getSymbolPosition(self.alphabetMixed, symbol) -
            self.getSymbolPosition(self.alphabet, self.positionSymbol)) % (len(self.alphabet))
        foundSymbol = self.alphabet[foundPosition]

        print(self.getSymbolPosition(self.alphabetMixed, symbol), " - ",
            self.getSymbolPosition(self.alphabet, self.positionSymbol), " = ", foundPosition)

        return foundSymbol

    def getSymbolPosition(self, alphabet: list, symbol: str):
        curPos = -1

        for i in range(len(alphabet)):
            if (alphabet[i] == symbol):
                curPos = i
                break

        return curPos


class Reflector():
    alphabet: list
    alphabetMixed: list

    def __init__(self, alphabet: list, alphabetMixed: list):
        self.alphabet = alphabet
        self.alphabetMixed = alphabetMixed

    def reflect(self, symbol: str):
        mixedSymbol = self.alphabet[self.getSymbolPosition(self.alphabet, symbol)]
        return self.alphabet[self.getSymbolPosition(self.alphabetMixed, mixedSymbol)]

    def getSymbolPosition(self, alphabet: list, symbol: str):
        curPos = -1

        for i in range(len(alphabet)):
            if (alphabet[i] == symbol):
                curPos = i
                break

        return curPos


class Enigma():
    alphabet: list
    alphabetMixed1: list
    alphabetMixed2: list
    alphabetMixed3: list
    alphabetReflect: list
    positionSymbol1: str
    positionSymbol2: str
    positionSymbol3: str
    rotor1: Rotor
    rotor2: Rotor
    rotor3: Rotor
    reflector: Reflector

    def __init__(self, alphabet: list, alphabetMixed1: list, alphabetMixed2: list,
                 alphabetMixed3: list, alphabetReflect: list, positionSymbol1: str,
                 positionSymbol2: str, positionSymbol3: str):
        self.alphabet = alphabet
        self.alphabetMixed1 = alphabetMixed1
        self.alphabetMixed2 = alphabetMixed2
        self.alphabetMixed3 = alphabetMixed3
        self.alphabetReflect = alphabetReflect
        self.positionSymbol1 = positionSymbol1
        self.positionSymbol2 = positionSymbol3
        self.positionSymbol3 = positionSymbol2
        self.rotor1 = Rotor(alphabet, alphabetMixed1, positionSymbol1)
        self.rotor2 = Rotor(alphabet, alphabetMixed2, positionSymbol2)
        self.rotor3 = Rotor(alphabet, alphabetMixed3, positionSymbol3)
        self.reflector = Reflector(alphabet, alphabetReflect)

    def process(self, symbol: str):
        symbol = self.rotor1.getSymbolForward(symbol)
        print("Rotor1 Forward: ", symbol)
        symbol = self.rotor2.getSymbolForward(symbol)
        print("Rotor2 Forward: ", symbol)
        symbol = self.rotor3.getSymbolForward(symbol)
        print("Rotor3 Forward: ", symbol)
        symbol = self.reflector.reflect(symbol)
        print("Reflector: ", symbol)
        symbol = self.rotor3.getSymbolBack(symbol)
        print("Rotor1 Back: ", symbol)
        symbol = self.rotor2.getSymbolBack(symbol)
        print("Rotor2 Back: ", symbol)
        symbol = self.rotor1.getSymbolBack(symbol)
        print("Rotor3 Back: ", symbol)

        return symbol



def main():
    alphabet = ["A", "B", "C", "D", "E", "F", 
                "G", "H", "I", "J", "K", "L",
                "M", "N", "O", "P", "Q", "R",
                "S", "T", "U", "V", "W", "X", "Y", "Z"]

    alphabetMixed1 = ["E", "K", "M", "F", "L", "G", 
                      "D", "Q", "V", "Z", "N", "T",
                      "O", "W", "Y", "H", "X", "U",
                      "S", "P", "A", "I", "B", "R", "C", "J"]

    alphabetMixed2 = ["A", "J", "D", "K", "S", "I", 
                      "R", "U", "X", "B", "L", "H",
                      "W", "T", "M", "C", "Q", "G",
                      "Z", "N", "P", "Y", "F", "V", "O", "E"]

    alphabetMixed3 = ["B", "D", "F", "H", "J", "L", 
                      "C", "P", "R", "T", "X", "V",
                      "Z", "N", "Y", "E", "I", "W",
                      "G", "A", "K", "M", "U", "S", "Q", "O"]

    alphabetReflect = ["Y", "R", "U", "H", "Q", "S", 
                       "L", "D", "P", "X", "N", "G",
                       "O", "K", "M", "I", "E", "B",
                       "F", "Z", "C", "W", "V", "J", "A", "T"]

    positionSymbol1 = "R"
    positionSymbol2 = "V"
    positionSymbol3 = "C"

    enigma = Enigma(alphabet, alphabetMixed1, alphabetMixed2, alphabetMixed3,
                    alphabetReflect, positionSymbol1, positionSymbol2, positionSymbol3)

    print("Res", enigma.process("W"))

    # rotor = Rotor(alphabet, alphabetMixed2, positionSymbol1)
    # print(rotor.getSymbolPosition(alphabet, ))

    # reflector = Reflector(alphabet, alphabetReflect)

if __name__ == "__main__":
    main()
