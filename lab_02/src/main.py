from random import randint, shuffle
import pickle


class Rotor():
    alphabet: list
    alphabetMixed: list
    position: int

    def __init__(self, alphabet: list, alphabetMixed: list, position: int):
        self.alphabet = alphabet
        self.alphabetMixed = alphabetMixed
        self.position = position

    def setPosition(self, position):
        self.position = position

    def rotate(self):
        self.position += 1

        return self.position

    def getSymbolForward(self, symbol: str):
        foundPosition = (self.getSymbolPosition(self.alphabet, symbol) +
            self.position) % (len(self.alphabet))
        foundSymbol = self.alphabetMixed[foundPosition]

        return foundSymbol

    def getSymbolBack(self, symbol: str):
        foundPosition = (self.getSymbolPosition(self.alphabetMixed, symbol) -
            self.position) % (len(self.alphabet))
        foundSymbol = self.alphabet[foundPosition]

        return foundSymbol

    def getSymbolPosition(self, alphabet: list, symbol: str):
        curPos = -1

        for i in range(len(alphabet)):
            if (alphabet[i] == symbol):
                curPos = i
                break

        return curPos


class Reflector():
    alphabet: dict

    def __init__(self, alphabet: dict):
        self.alphabet = alphabet

    def reflect(self, symbol: str):
        return self.alphabet[symbol]


class Enigma():
    alphabet: list
    alphabetReflect: dict
    alphabetMixedN: list
    positionN: list
    rotorCount: int
    rotors: list
    reflector: Reflector

    def __init__(self, alphabet: list, rotorCount: int, alphabetReflect: list = None,
        alphabetMixedN: list = None, positionN: list = None):
        self.alphabet = alphabet.copy()
        self.rotorCount = rotorCount if (rotorCount >= 0) else 0

        if (alphabetReflect is None):
            self.alphabetReflect = self.generateReflectAlphabet().copy()
        else:
            self.alphabetReflect = alphabetReflect.copy()

        if (alphabetMixedN is None):
            self.alphabetMixedN = self.generateMixedAlphabets().copy()
        else:
            if (len(alphabetMixedN) != self.rotorCount):
                print("Ошибка: Кол-во Перемешанных Алфавитов не соответствует кол-ву роторов. \
                    Перемешанные Алфавиты сгенерированы автоматически")
                self.alphabetMixedN = self.generateMixedAlphabets().copy()
            else:
                self.alphabetMixedN = alphabetMixedN.copy()

        if (positionN is None):
            self.positionN = [randint(0, len(self.alphabet)) for _ in range(self.rotorCount)]
        else:
            if (len(positionN) != self.rotorCount):
                print("Ошибка: Кол-во Позиционных Cимволов не соответствует кол-ву роторов. \
                    Позиционные Cимволы сгенерированы автоматически")
                self.positionN = [randint(0, len(self.alphabet)) for _ in range(self.rotorCount)]
                
            self.positionN = positionN.copy()

        self.rotors = [Rotor(self.alphabet, 
                             self.alphabetMixedN[i], 
                             self.positionN[i]) 
                       for i in range(self.rotorCount)]

        self.reflector = Reflector(self.alphabetReflect)
    
    def reset(self):
        for i, rotor in enumerate(self.rotors):
            rotor.setPosition(self.positionN[i])

    def generateMixedAlphabets(self):
        shuffledAlphabets = list()

        for _ in range(self.rotorCount):
            tmpAlphabet = self.alphabet.copy()
            shuffle(tmpAlphabet)
            shuffledAlphabets.append(tmpAlphabet)

        return shuffledAlphabets        

    def generateReflectAlphabet(self):
        tmpReflectAlphabet = self.alphabet.copy()
        shuffle(tmpReflectAlphabet)
        alphabetReflect = dict()

        for i in range(0, len(tmpReflectAlphabet), 2):
            alphabetReflect[tmpReflectAlphabet[i]] = tmpReflectAlphabet[i + 1]
            alphabetReflect[tmpReflectAlphabet[i + 1]] = tmpReflectAlphabet[i]

        return alphabetReflect

    def rotateRotors(self):
        for rotor in self.rotors:
            position = rotor.rotate()

            if (position != 0):
                break

    def process(self, symbol: str):

        for ind in range(0, len(self.rotors), 1):
            symbol = self.rotors[ind].getSymbolForward(symbol)

        symbol = self.reflector.reflect(symbol)

        for ind in range(len(self.rotors) - 1, -1, -1):
            symbol = self.rotors[ind].getSymbolBack(symbol)
        
        self.rotateRotors()

        return symbol



FILE = "data.bin"


def generateBinaryFilePickle():
    string = "DARTHVADER"

    with open(FILE, "wb") as file:
        pickle.dump(string, file)

    with open(FILE, "rb") as file:
        print("Clear Binary:", bin(file.read()))
        # print("From Binary:", pickle.load(file))


def generateBinaryFile():
    string = "DARTHVADER"

    with open(FILE, "wb") as file:
        for symbol in string:
            symbol += "\n"
            bt = symbol.encode()
            file.write(bt)

    with open(FILE, "rb") as file:
        res = file.readlines()

        for symbol in res:
            print(bin(symbol[:-1]))

    



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

    # alphabetReflect = ["Y", "R", "U", "H", "Q", "S", 
    #                    "L", "D", "T", "X", "N", "G",
    #                    "O", "K", "M", "I", "E", "B",
    #                    "F", "Z", "C", "W", "V", "J", "A", "P"]

    alphabetReflect = {"A": "Y", "B": "R", "C": "U", "D": "H",
                       "E": "Q", "F": "S", "G": "L", "H": "D",
                       "I": "T", "J": "X", "K": "N", "L": "G",
                       "M": "O", "N": "K", "O": "M", "P": "I",
                       "Q": "E", "R": "B", "S": "F", "T": "Z",
                       "U": "C", "V": "W", "W": "V", "X": "J",
                       "Y": "A", "Z": "P"}

    positionSymbol1 = "R"
    positionSymbol2 = "V"
    positionSymbol3 = "C"

    # enigma = Enigma(alphabet, 3, alphabetReflect,
    #                 [alphabetMixed1, alphabetMixed2, alphabetMixed3],
    #                 [positionSymbol1, positionSymbol2, positionSymbol3])

    enigma = Enigma(alphabet, 3, positionN=[1, 2, 3])
    # enterSymbol = "T"
    # print("\nEnter Symbol: ", enterSymbol, "\n\n")
    # res = enigma.process(enterSymbol)
    # enigma.reset()
    # print("Res Encrypt: ", res, "\n\n")
    # print("Res Decrypt: ", enigma.process(res))

    testString = "DARTHVADER"
    encryptString = str()
    decryptString = str()

    for symbol in testString:
        res = enigma.process(symbol)
        encryptString += res

    print("Encrypt String: ", encryptString)
    enigma.reset()

    for symbol in encryptString:
        res = enigma.process(symbol)
        decryptString += res

    print("Decrypt String: ", decryptString)

    # generateBinaryFile()
    

if __name__ == "__main__":
    main()
