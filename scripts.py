

import math



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
	print(genFBitscanIndex(0x1061438916347932A5CD9D3EAD7B77F))
	print(genRBitscanIndex(0x1FC47709ECA6B19CC17D25B45754379))

