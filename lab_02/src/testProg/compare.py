src = "main"
dst = "decoded.bin"

f1 = open(src, "rb")
f2 = open(dst, "rb")

ind = 0


while True:

    b1 = f1.read(1)
    b2 = f2.read(1)

    if (not b1) and (not b2):
        print("Конец обоих файлов")
        break
    elif (not b1):
        print("Конец src файла")
        break
    elif (not b2):
        print("Конец dst файла")
        break

    if (b1 != b2):
        print("НЕТ! [", ind, "] b1 = ", b1, "; b2 = ", b2)
        break

    ind += 1

f1.close()
f2.close()