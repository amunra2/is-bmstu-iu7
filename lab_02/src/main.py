from random import shuffle


class Rotor():
    alphabet: list
    alphabetMixed: list
    positionSymbol: str

    def __init__(self, alphabet: list, alphabetMixed: list, positionSymbol: str):
        self.alphabet = alphabet
        self.alphabetMixed = alphabetMixed
        self.positionSymbol = positionSymbol

    def rotate(self):
        posititonOld = self.getSymbolPosition(self.alphabet, self.positionSymbol)
        self.positionSymbol = self.alphabet[(posititonOld + 1) % len(self.alphabet)]

        return self.positionSymbol

    def getSymbolForward(self, symbol: str):
        foundPosition = (self.getSymbolPosition(self.alphabet, self.positionSymbol) + 
            self.getSymbolPosition(self.alphabet, symbol)) % (len(self.alphabet))
        foundSymbol = self.alphabetMixed[foundPosition]

        # print(self.getSymbolPosition(self.alphabet, self.positionSymbol), " + ",
        #     self.getSymbolPosition(self.alphabet, symbol), " = ", foundPosition)

        return foundSymbol

    def getSymbolBack(self, symbol: str):
        foundPosition = (self.getSymbolPosition(self.alphabetMixed, symbol) -
            self.getSymbolPosition(self.alphabet, self.positionSymbol)) % (len(self.alphabet))
        foundSymbol = self.alphabet[foundPosition]

        # print(self.getSymbolPosition(self.alphabetMixed, symbol), " - ",
        #     self.getSymbolPosition(self.alphabet, self.positionSymbol), " = ", foundPosition)

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
        mixedSymbol = self.alphabetMixed[self.getSymbolPosition(self.alphabet, symbol)]
        print(self.getSymbolPosition(self.alphabet, symbol), self.getSymbolPosition(self.alphabetMixed, mixedSymbol))
        print(mixedSymbol, self.alphabet[self.getSymbolPosition(self.alphabetMixed, mixedSymbol)])
        return self.alphabet[self.getSymbolPosition(self.alphabet, mixedSymbol)]

    def getSymbolPosition(self, alphabet: list, symbol: str):
        curPos = -1

        for i in range(len(alphabet)):
            if (alphabet[i] == symbol):
                curPos = i
                break

        return curPos


class Enigma():
    alphabet: list
    alphabetReflect: list
    alphabetMixedN: list
    positionSymbolN: list
    rotorCount: int
    rotors: list
    reflector: Reflector

    def generateMixedAlphabets(self):
        shuffledAlphabets = list()

        for _ in range(self.rotorCount):
            tmpAlphabet = self.alphabet.copy()
            shuffle(tmpAlphabet)
            shuffledAlphabets.append(tmpAlphabet)

        return shuffledAlphabets        


    def __init__(self, alphabet: list, rotorCount: int, alphabetReflect: list = None,
        alphabetMixedN: list = None, positionSymbolN: list = None):
        self.alphabet = alphabet.copy()
        self.rotorCount = rotorCount if (rotorCount >= 0) else 0

        if (alphabetReflect is None):
            tmpReflectAlphabet = alphabet.copy()
            shuffle(tmpReflectAlphabet)
            self.alphabetReflect = tmpReflectAlphabet.copy()
        else:
            self.alphabetReflect = alphabetReflect.copy()

        if (alphabetMixedN is None):
            self.alphabetMixedN = self.generateMixedAlphabets().copy()
            # print(self.alphabetMixedN)
        else:
            if (len(alphabetMixedN) != self.rotorCount):
                print("Ошибка: Кол-во Перемешанных Алфавитов не соответствует кол-ву роторов. \
                    Перемешанные Алфавиты сгенерированы автоматически")
                self.alphabetMixedN = self.generateMixedAlphabets().copy()
            else:
                self.alphabetMixedN = alphabetMixedN.copy()

        if (positionSymbolN is None):
            self.positionSymbolN = ["A" for _ in range(self.rotorCount)]
        else:
            if (len(positionSymbolN) != self.rotorCount):
                print("Ошибка: Кол-во Позиционных Cимволов не соответствует кол-ву роторов. \
                    Позиционные Cимволы сгенерированы автоматически")
                self.positionSymbolN = ["A" for _ in range(self.rotorCount)]
                
            self.positionSymbolN = positionSymbolN.copy()

        self.rotors = [Rotor(self.alphabet, 
                             self.alphabetMixedN[i], 
                             self.positionSymbolN[i]) 
                       for i in range(self.rotorCount)]

        self.reflector = Reflector(self.alphabet, self.alphabetReflect)

        print("================INIT====================")
        print(self.alphabet)
        print(self.alphabetMixedN)
        print(self.alphabetReflect)
        print(self.positionSymbolN)
        print(self.rotorCount)
        print("========================================")

    def rotateRotors(self):
        for rotor in self.rotors:
            postitonSymbol = rotor.rotate()

            if (postitonSymbol != self.alphabet[0]):
                break

    def process(self, symbol: str):
        print("Symbol = ", symbol)

        for ind in range(0, len(self.rotors), 1):
            symbol = self.rotors[ind].getSymbolForward(symbol)
            print("Rotor[", ind,"] Forward: ", symbol)

        symbol = self.reflector.reflect(symbol)
        print("Rotor Reflect: ", symbol)

        for ind in range(len(self.rotors) - 1, -1, -1):
            symbol = self.rotors[ind].getSymbolBack(symbol)
            print("Rotor[", ind,"] Back: ", symbol)
        
        # print("\nBefore: ", self.rotors[0].positionSymbol)
        # self.rotateRotors()
        # print("After: ", self.rotors[0].positionSymbol)

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
                      "Z", "N", "Y", "E", "Q", "W",
                      "G", "A", "K", "M", "U", "S", "I", "O"]

    alphabetReflect = ["Y", "R", "U", "H", "Q", "S", 
                       "L", "D", "T", "X", "N", "G",
                       "O", "K", "M", "I", "E", "B",
                       "F", "Z", "C", "W", "V", "J", "A", "P"]

    positionSymbol1 = "R"
    positionSymbol2 = "V"
    positionSymbol3 = "C"

    # enigma = Enigma(alphabet, 3, alphabetReflect,
    #                 [alphabetMixed1, alphabetMixed2, alphabetMixed3],
    #                 [positionSymbol1, positionSymbol2, positionSymbol3])

    enigma = Enigma(alphabet, 3, alphabetReflect=alphabetReflect)
    enterSymbol = "T"
    print("\nEnter Symbol: ", enterSymbol, "\n\n")
    res = enigma.process(enterSymbol)
    print("Res Encrypt: ", res, "\n\n")
    print("Res Decrypt: ", enigma.process(res))

    #rotor = Rotor(alphabet, alphabetMixed2, positionSymbol1)
    #print(rotor.getSymbolPosition(alphabet, ))

    # reflector = Reflector(alphabet, alphabetReflect)

if __name__ == "__main__":
    main()
