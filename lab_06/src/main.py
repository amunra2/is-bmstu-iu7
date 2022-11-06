import os
from bitarray import bitarray
from bitarray.util import ba2hex, hex2ba


SPACE = "  "


class Node():
    def __init__(self, count: int, data=None, left=None, right=None):
        self.data = data
        self.count = count
        self.left = left
        self.right = right

    def getData(self):
        return self.data

    def getCount(self):
        return self.count

    def printNode(self):
        print("{0}: {1}".format(self.data, self.count))


class HaffmanCode():
    def __init__(self) -> None:
        self.root = None

    def __translateDictToNodeList(self, dictionary: dict):
        """
            Перевод словаря в список Node
        """
        return [Node(v, k) for k, v in dictionary.items()]


    def __sortNodeList(self, nodes: list[Node], reverse=False):
        """
            Сортировка списка Node
        """
        return sorted(nodes, key=lambda item: item.count, reverse=reverse)


    def generateTreeByDict(self, frequencyTable: dict):
        """
            Генерация дерева для алгоритма Хаффмана по
            словарю {символ: частота встречи}
        """
        nodeList = self.__translateDictToNodeList(frequencyTable)

        while (len(nodeList) != 1):
            nodeList = self.__sortNodeList(nodeList, reverse=True)

            firstElem = nodeList.pop()
            secondElem = nodeList.pop()

            summarisedElem = Node(
                # data=firstElem.getData() + secondElem.getData(),
                count=firstElem.getCount() + secondElem.getCount(),
                left=secondElem,
                right=firstElem,
            )

            nodeList.append(summarisedElem)

        self.root = nodeList[0]


    def __getCodeBySymbleRecursive(self, root: Node, symbol, code):
        result = ""

        if (root.data == symbol):
            # print("{}: {}".format(symbol, code))
            result += code

        if (root.left):
            result += self.__getCodeBySymbleRecursive(root.left, symbol, code + "0")

        if (root.right):
            result += self.__getCodeBySymbleRecursive(root.right, symbol, code + "1") 

        return result

    
    def getCodeBySymbol(self, symbol):
        if (self.root == None):
            print("Ошибка: Дерево не сгенерировано")
            return

        return self.__getCodeBySymbleRecursive(self.root, symbol=symbol, code="")


    def __getSymbolByCodeRecursive(self, root: Node, code):
        result = ""

        if (code == ""):
            result = root.getData()

        if (code[:1] == "0"):
            result = self.__getSymbolByCodeRecursive(root.left, code[1:])

        if (code[:1] == "1"):
            result = self.__getSymbolByCodeRecursive(root.right, code[1:]) 

        return result

    def getSymbolByCode(self, code):
        if (self.root == None):
            print("Ошибка: Дерево не сгенерировано")
            return

        return self.__getSymbolByCodeRecursive(self.root, code)


    def getRoot(self):
        """
            Получить корень дерева
        """
        return self.root


    def printTree(self, space: str):
        """
            Распечатать дерево
        """
        self.__printTreeRecursive(self.root, space=space)


    def __printTreeRecursive(self, root: Node, space: str):
        """
            Распечатать дерево рекурсивно
        """
        print("{}{}: {}".format(space, root.data, root.count))

        if (root.left):
            self.__printTreeRecursive(root.left, space + SPACE)

        if (root.right):
            self.__printTreeRecursive(root.right, space + SPACE)


def getCountSymbolsDict(filePath: str):
    try:
        fullPath = os.path.join(os.getcwd(), filePath)
        file = open(fullPath, "rb")
    except:
        print("Ошибка: файл \'%s\' отстуствует" % fullPath)
        return

    frequencyTable = dict()

    while True:
        byte = file.read(1)

        if not byte:
            break

        count = 1
        
        if (byte in frequencyTable):
            count = frequencyTable.get(byte) + 1
        
        frequencyTable.update({byte: count})

    file.close()

    return frequencyTable


def compressFile(srcPath: str, dstPath: str, haffmanCode: HaffmanCode):
    try:
        fullPath = os.path.join(os.getcwd(), srcPath)
        srcFile = open(fullPath, "rb")
    except:
        print("Ошибка: файл \'%s\' отстуствует" % fullPath)
        return

    resultStringOfBits = ""

    ################# READ #######################
    while True:
        byte = srcFile.read(1)

        if not byte:
            break
        
        code = haffmanCode.getCodeBySymbol(byte)

        if (code == ""):
            print("Ошибка: Неверный символ")
            return

        resultStringOfBits += code

    srcFile.close()
    ################# READ #######################


    ################ ADD BITS #####################
    extraBits = len(resultStringOfBits) % 8

    if (extraBits != 0):
        bitsToAdd = 8 - extraBits
        resultStringOfBits += "0" * bitsToAdd
    ################ ADD BITS #####################


    ############### WRITE BITS ####################
    fullPath = os.path.join(os.getcwd(), dstPath)
    
    with (open(fullPath, "wb")) as dstFile:
        bytesToWrite = bitarray(resultStringOfBits).tobytes()
        dstFile.write(bytesToWrite)

        dstFile.write(bytes(str(bitsToAdd), encoding="utf-8"))
    ############### WRITE BITS ####################


def decompressFile(srcPath: str, dstPath: str, haffmanCode: HaffmanCode):
    try:
        fullPath = os.path.join(os.getcwd(), srcPath)
        srcFile = open(fullPath, "rb")
    except:
        print("Ошибка: файл \'%s\' отстуствует" % fullPath)
        return

    resultBytes = srcFile.read()
    srcFile.close()

    bitsToDelete = int(resultBytes[-1:].decode(encoding="utf-8"))
    resultBytes = resultBytes[:-1]

    bits = hex2ba(resultBytes.hex()).to01()
    bits = bits[:-bitsToDelete]

    
    fullPath = os.path.join(os.getcwd(), dstPath)
    dstFile = open(fullPath, "wb")

    code = ""

    while (bits != ""):
        code += bits[:1]
        bits = bits[1:]

        result = haffmanCode.getSymbolByCode(code)

        if (result != None):
            dstFile.write(result)
            code = ""

    dstFile.close()




def binStrToBytes(binString: str):
    bitArr = bitarray(binString)
    # hexArr = ba2hex(bitArr)
    byte = bitArr.tobytes()#bytes.fromhex(hexArr)
    print(byte)

    hexArr = byte.hex()
    bitArr = hex2ba(hexArr)
    print(bitArr)
    print(bitArr.to01())


def test(binString: str):
    print(len(binString) % 8)


def main():
    # dictionary = {"a": 15, "b": 7, "c": 6, "d": 6, "e": 5}

    srcPath = "lab_06/src/testProg/dv.png"
    dstPath = "lab_06/src/testProg/result.bin"


    dictionary = getCountSymbolsDict(srcPath)

    haffmanCode = HaffmanCode()
    haffmanCode.generateTreeByDict(dictionary)
    # haffmanCode.printTree(space="")

    compressFile(srcPath, dstPath, haffmanCode)

    srcPath = "lab_06/src/testProg/result.bin"
    dstPath = "lab_06/src/testProg/decompressed.bin"

    decompressFile(srcPath, dstPath, haffmanCode)





    



if __name__ == "__main__":
    main()




    
