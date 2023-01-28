import unittest


def testFBitscan():
    print("Start of randomized forward bitscan test.")

    for i in range(1, 5000):
        num = random.randint(1, 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF)
        bboard = Bitboard.makeBitboard(num)
        result = bboard.fBitscan()
        bboard.insect(Bitboard.makeBitboard(1 << result))
        assert bboard.barray == (num & -num), f"WRONG :: Forward bitscan outputted {result} for {bin(num)}."

    print("End of randomized forward bitscan test.")


def testRBitscan():
    print("Start of randomized reverse bitscan test.")

    for i in range(1, 5000):
        num = random.randint(1, 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF)
        bboard = Bitboard.makeBitboard(num)
        result = bboard.rBitscan()
        bboard.insect(Bitboard.makeBitboard(1 << result))
        assert bboard.barray == ms1b(num), f"WRONG :: Reverse bitscan outputted {result} for {bin(num)}."

    print("End of randomized reverse bitscan test.")



def manualFBitscanTest():
    print("Start of manual forward bitscan test.")

    while True:
        inNum = int(input("Enter input number (in decimal): "))

        bboard = Bitboard.makeBitboard(inNum)
        result = bboard.fBitscan()
        numstr = bin(inNum)[2:].zfill(128)

        print(f"Input number in binary: {numstr}")
        print(f"Resulting index: {result}")

        if inNum == -1:
            break

    print("End of manual forward bitscan test.")



def manualRBitscanTest():
    print("Start of manual reverse bitscan test.")

    while True:
        inNum = int(input("Enter input number (in decimal): "))

        bboard = Bitboard.makeBitboard(inNum)
        result = bboard.rBitscan()
        numstr = bin(inNum)[2:].zfill(128)

        print(f"Input number in binary: {numstr}")
        print(f"Resulting index: {result}")

        if inNum == -1:
            break

    print("End of manual reverse bitscan test.")


if __name__ == "__main__":
    result = unittest.TestResult()
    loader = unittest.TestLoader()
    suite = loader.discover("./")
    print(suite)
    suite.run(result)
    print(result)
    unittest.main()
