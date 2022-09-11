

import math



def genNAttkRays():
	lookup = [None] * 100
	north = 0x10040100401004010040100401

	for i in range(100):
		lookup[i] = ((north << i) & 0xFFFFFFFFFFFFFFFFFFFFFFFFF)

	return lookup



def genEAttkRays():
	lookup = [None] * 100

	for row in range(10):
		east = 0x3FF << (row * 10)
		for col in range(10):
			lookup[row * 10 + col] = (east & 0xFFFFFFFFFFFFFFFFFFFFFFFFF)
			east &= 0x1FF7FDFF7FDFF7FDFF7FDFF7FDFF # removes right-most board columns of bits
			east <<= 1


	return lookup



def genNEAttkRays():
	lookup = [None] * 100

	for row in range(10):
		diag = 0x8010020040080100200400801 << (10 * row)
		for col in range(10):
			lookup[row * 10 + col] = (diag & 0xFFFFFFFFFFFFFFFFFFFFFFFFF)
			diag &= 0x1FF7FDFF7FDFF7FDFF7FDFF7FDFF # removes right-most board columns of bits
			diag <<= 1

	return lookup



def genNWAttkRays():
	lookup = [None] * 100

	for row in range(10):
		aDiag = 0x40201008040201008040200 << (10 * row)
		for col in range(9, -1, -1):
			aDiag &= 0xFFFFFFFFFFFFFFFFFFFFFFFFF
			lookup[row * 10 + col] = aDiag
			aDiag &= 0x3FEFFBFEFFBFEFFBFEFFBFEFFBFE # removes right-most columns of bits
			aDiag >>= 1

	return lookup



def genSAttkRays():
	lookup = [None] * 100

	for i in range(99, -1, -1):
		south = 0x8020080200802008020080200
		lookup[i] = south >> i

	return lookup



def genWAttkRays():
	lookup = [None] * 100

	for row in range(10):
		west = 0x3FF << (10 * row)
		west &= 0xFFFFFFFFFFFFFFFFFFFFFFFFF
		for col in range(9, -1, -1):
			lookup[row * 10 + col] = west
			west &= 0xFFBFEFFBFEFFBFEFFBFEFFBFE # removes left-most board column of bits
			west >>= 1

	return lookup



def genSWAttkRays():
	lookup = [None] * 100
	
	for row in range(9, -1, -1):
		diag = 0x8010020040080100200400801 >> (10 * (9 - row))
		diag &= 0xFFFFFFFFFFFFFFFFFFFFFFFFF
		for col in range(9, -1, -1):
			lookup[row * 10 + col] = diag
			diag &= 0xFFBFEFFBFEFFBFEFFBFEFFBFE # removes left-most board column of bits
			diag >>= 1
			diag &= 0xFFFFFFFFFFFFFFFFFFFFFFFFF

	return lookup



def genSEAttkRays():
	lookup = [None] * 100

	for row in range(9, -1, -1):
		aDiag = 0x40201008040201008040200 >> (10 * (9 - row))
		aDiag &= 0xFFFFFFFFFFFFFFFFFFFFFFFFF
		for col in range(10):
			lookup[row * 10 + col] = aDiag
			aDiag &= 0x7FDFF7FDFF7FDFF7FDFF7FDFF
			aDiag <<= 1 

	return lookup
		


def printBboard(bboard):
	bboardStr = bin(bboard)[2:].zfill(100)
	print(bboard)
	for i in range(0, 100, 10):
		print(bboardStr[i:i + 10][::-1])



def printBboardList(bbList):
	for bboard in bbList:
		hexBboard = hex(bboard)
		print(f" Start of {hexBboard} ".center(50, "="))
		printBboard(bboard)
		print(f" End of {hexBboard} ".center(50, "="))



def hexifyBboardList(bblist):
	return [hex(el) for el in bblist]


	
def genDeBrujinIndex(valFunc, idxFunc, inGen):
	"""
	Help function for generating indices for 128-bit Bitscan implementations using
	De Brujin multiplication.
	"""

	index = [None] * 128
	for i in inGen():
		if index[valFunc(i)] != None:
			print(f"CONFLICT at index {valFunc(i)} :: {index[valFunc(i)]} and {idxFunc(i)}")
		index[valFunc(i)] = idxFunc(i)

	return index



def genFBitscanIndex(debrujin):
	"""
	Generates a index that can be used for a custom 128-bit forward bitscan implementation
	using De Brujin multiplication.


	Algorithm details: https://www.chessprogramming.org/BitScan#De_Bruijn_Multiplication

	NOTES
	This may have the same issue as genRBitscanIndex() where certain De Brujin sequences
	may not result in a complete index. 

	128-bit De Brujin sequences that result in a complete index: 
	0x1061438916347932A5CD9D3EAD7B77F
	"""
	
	def valFunc(num): return ((debrujin * num) & 0xFE000000000000000000000000000000) >> 121
	def idxFunc(num): return int(math.log(num, 2))
	def inGen():
		for i in range(128):
			yield 1 << i

	return genDeBrujinIndex(valFunc, idxFunc, inGen)



def genRBitscanIndex(debrujin):
	"""
	Generates a index that can be used for a custom 128-bit reverse bitscan implementation
	using De Brujin multiplication.


	Algorithm details: https://www.chessprogramming.org/BitScan#De_Bruijn_Multiplication_2

	NOTES
	This does not reliably generate does not generate a complete index depending on
	the inputted De Brujin sequence.
	e.g 0x1061438916347932A5CD9D3EAD7B77F 

	128-bit De Brujin sequences that result in a complete index: 
	0x1FC47709ECA6B19CC17D25B45754379
	"""

	def valFunc(num): return ((debrujin * num) & 0xFE000000000000000000000000000000) >> 121
	def idxFunc(num): return int(math.log(num + 1, 2)) - 1
	def inGen():
		for i in range(128):
			yield (1 << (i + 1)) - 1

	return genDeBrujinIndex(valFunc, idxFunc, inGen)




if __name__ == "__main__":
	# print(genFBitscanIndex(0x1061438916347932A5CD9D3EAD7B77F))
	# print(genRBitscanIndex(0x1FC47709ECA6B19CC17D25B45754379))

	# printBboardList(genWAttkRays())
	# printBboardList(genSAttkRays())
	# printBboardList(genNAttkRays())

	# printBboardList(genSWAttkRays())
	printBboardList(genSEAttkRays())

