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

        # print("ALPHABET")
        # print(alphabet)
        # print("ALPHABET_MIXED")
        # print(alphabetMixed)
        # print("POSITION")
        # print(position)

    def setPosition(self, position):
        self.position = position

    def rotate(self):
        self.position = (self.position + 1) % len(self.alphabet)

        return self.position

    def getSymbolForward(self, symbol):
        foundPosition = (self.getSymbolPosition(self.alphabet, symbol) +
            self.position) % (len(self.alphabet))
        foundSymbol = self.alphabetMixed[foundPosition]

        return foundSymbol

    def getSymbolBack(self, symbol):
        foundPosition = (self.getSymbolPosition(self.alphabetMixed, symbol) -
            self.position) % (len(self.alphabet))
        foundSymbol = self.alphabet[foundPosition]

        return foundSymbol

    def getSymbolPosition(self, alphabet: list, symbol):
        curPos = -1

        for i in range(len(alphabet)):
            if (alphabet[i] == symbol):
                curPos = i
                break

        if (curPos == -1):
            print("NO SYMBOL")

        return curPos


class Reflector():
    alphabet: dict

    def __init__(self, alphabet: dict):
        self.alphabet = alphabet

    def reflect(self, symbol):
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

    def process(self, symbol):

        # print("Symbol In = ", symbol)

        for ind in range(0, len(self.rotors), 1):
            symbol = self.rotors[ind].getSymbolForward(symbol)
            # print("RotorForward[", ind, "] = ", symbol)

        symbol = self.reflector.reflect(symbol)
        # print("Reflect[", ind, "] = ", symbol)


        for ind in range(len(self.rotors) - 1, -1, -1):
            symbol = self.rotors[ind].getSymbolBack(symbol)
            # print("RotorBack[", ind, "] = ", symbol)

        
        self.rotateRotors()

        return symbol

    def encodeBinary(self, pathSrc: str, dstName: str):
        # symbol = self.rotors[0].getSymbolForward(b'\xd8')
        # print("IN: ", symbol)
        # symbol = self.rotors[0].getSymbolBack(symbol)
        # print("BACK: ", symbol)

        # self.process(symbol)

        srcFile = open(pathSrc, "rb")
        dstFile = open(dstName, "wb")

        print("====================================")

        # while (byte := srcFile.read(1)):
        # for i in range(105):
        while True:
            byte = srcFile.read(1)

            if not byte:
                break

            encodedByte = self.process(byte)
            # print("[", i, "]", type(encodedByte), encodedByte, bytes([i for i in encodedByte]), "\n")
            dstFile.write(bytes(encodedByte))

        srcFile.close()
        dstFile.close()

        print("Кодирование прошло успешно")
            



FILE = "data.bin"


def generateBinaryAlphabet():
    # alphabet = list()

    # for i in range(256):
    #     symbol = chr(i).encode()
    #     res = [bytes([x]) for x in symbol]

    #     for byte in res:
    #         alphabet.append(byte)

    # alphabet = set(alphabet)
    # alphabet = list(alphabet)

    # print(len(alphabet))
    # print(alphabet)

    alphabet = bytes([code for code in range(256)])
    # print([i for i in (bytes([code for code in range(256)]))])
    alphabetList = [bytes([x]) for x in alphabet]
    # print(alphabet)
    # print(alphabetList)
    return alphabetList

    # return bytes([code for code in range(256)])

    


def generateBinaryFilePickle():
    string = "DARTHVADER"

    with open(FILE, "wb") as file:
        pickle.dump(string, file)

    with open(FILE, "rb") as file:
        print("Clear Binary:", file.read())
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
            print(symbol[:-1].decode())

    



def main():

    alphabetBytes = generateBinaryAlphabet()

    enigma = Enigma(alphabetBytes, 3)
    print([rotor.position for rotor in enigma.rotors])
    enigma.encodeBinary("./testProg/main", "./testProg/encoded.bin")
    print([rotor.position for rotor in enigma.rotors])
    enigma.reset()
    print([rotor.position for rotor in enigma.rotors])
    enigma.encodeBinary("./testProg/encoded.bin", "./testProg/decoded.bin")

    # enigma = Enigma(alphabetBytes, 3)
    # start = b'+'
    # encrypted = enigma.process(start)
    # enigma.reset()
    # decrypted = enigma.process(encrypted)

    # print("Src: ", start, "Encrypted: ", encrypted, "Decrypted: ", decrypted)




    alphabet = ["A", "B", "C", "D", "E", "F", 
                "G", "H", "I", "J", "K", "L",
                "M", "N", "O", "P", "Q", "R",
                "S", "T", "U", "V", "W", "X", "Y", "Z"]

    # alphabetMixed1 = ["E", "K", "M", "F", "L", "G", 
    #                   "D", "Q", "V", "Z", "N", "T",
    #                   "O", "W", "Y", "H", "X", "U",
    #                   "S", "P", "A", "I", "B", "R", "C", "J"]

    # alphabetMixed2 = ["A", "J", "D", "K", "S", "I", 
    #                   "R", "U", "X", "B", "L", "H",
    #                   "W", "T", "M", "C", "Q", "G",
    #                   "Z", "N", "P", "Y", "F", "V", "O", "E"]

    # alphabetMixed3 = ["B", "D", "F", "H", "J", "L", 
    #                   "C", "P", "R", "T", "X", "V",
    #                   "Z", "N", "Y", "E", "Q", "W",
    #                   "G", "A", "K", "M", "U", "S", "I", "O"]

    # # alphabetReflect = ["Y", "R", "U", "H", "Q", "S", 
    # #                    "L", "D", "T", "X", "N", "G",
    # #                    "O", "K", "M", "I", "E", "B",
    # #                    "F", "Z", "C", "W", "V", "J", "A", "P"]

    # alphabetReflect = {"A": "Y", "B": "R", "C": "U", "D": "H",
    #                    "E": "Q", "F": "S", "G": "L", "H": "D",
    #                    "I": "T", "J": "X", "K": "N", "L": "G",
    #                    "M": "O", "N": "K", "O": "M", "P": "I",
    #                    "Q": "E", "R": "B", "S": "F", "T": "Z",
    #                    "U": "C", "V": "W", "W": "V", "X": "J",
    #                    "Y": "A", "Z": "P"}

    # positionSymbol1 = "R"
    # positionSymbol2 = "V"
    # positionSymbol3 = "C"

    # enigma = Enigma(alphabet, 3, alphabetReflect,
    #                 [alphabetMixed1, alphabetMixed2, alphabetMixed3],
    #                 [positionSymbol1, positionSymbol2, positionSymbol3])


    # enigma = Enigma(alphabet, 3)

    # testString = "DARTHVADER"
    # encryptString = str()
    # decryptString = str()

    # for symbol in testString:
    #     res = enigma.process(symbol)
    #     encryptString += res

    # print("Encrypt String: ", encryptString)
    # enigma.reset()

    # for symbol in encryptString:
    #     res = enigma.process(symbol)
    #     decryptString += res

    # print("Decrypt String: ", decryptString)

    # generateBinaryFile()

    

    

if __name__ == "__main__":
    main()
