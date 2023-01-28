

import math
import json


# ATTACK-RAYS ON EMPTY BOARD
# 
# Generation functions for attack-rays on an empty board. These attack-rays are used in
# further generation of attack-sets that will be used throughout the game and engine.
# These are generally cheap to compute and have a finite number of states but they are
# used often.
# =====================================================================================

# POSITIVE ATTACK-RAYS
# =====================================================================================
def genNAttkRays(): # NORTH
	lookup = [None] * 100
	north = 0x40100401004010040100401

	for i in range(100):
		lookup[i] = ((north << i) & 0xFFFFFFFFFFFFFFFFFFFFFFFFF)

	return lookup


def genEAttkRays(): # EAST
	lookup = [None] * 100

	for row in range(10):
		east = 0x3FF << (row * 10)
		east &= 0xFFFFFFFFFFFFFFFFFFFFFFFFF
		for col in range(10):
			lookup[row * 10 + col] = east
			east &= 0x7FDFF7FDFF7FDFF7FDFF7FDFF # removes right-most board columns of bits
			east <<= 1

	return lookup



def genNEAttkRays(): # NORTH-EAST
	lookup = [None] * 100

	for row in range(10):
		diag = 0x8010020040080100200400801 << (10 * row)
		diag &= 0xFFFFFFFFFFFFFFFFFFFFFFFFF
		for col in range(10):
			lookup[row * 10 + col] = diag
			diag &= 0x7FDFF7FDFF7FDFF7FDFF7FDFF # removes left-most board column of bits
			diag <<= 1

	return lookup



def genNWAttkRays(): # NORTH-WEST
	lookup = [None] * 100

	for row in range(10):
		aDiag = 0x40201008040201008040200 << (10 * row)
		for col in range(9, -1, -1):
			aDiag &= 0xFFFFFFFFFFFFFFFFFFFFFFFFF
			lookup[row * 10 + col] = aDiag
			aDiag &= 0xFFBFEFFBFEFFBFEFFBFEFFBFE # removes right-most columns of bits
			aDiag >>= 1

	return lookup



# NEGATIVE ATTACK-RAYS
# =====================================================================================
def genSAttkRays(): # SOUTH
	lookup = [None] * 100

	for i in range(99, -1, -1):
		south = 0x8020080200802008020080200
		lookup[i] = south >> (99 - i)

	return lookup



def genWAttkRays(): # WEST
	lookup = [None] * 100

	for row in range(10):
		west = 0x3FF << (10 * row)
		west &= 0xFFFFFFFFFFFFFFFFFFFFFFFFF
		for col in range(9, -1, -1):
			lookup[row * 10 + col] = west
			west &= 0xFFBFEFFBFEFFBFEFFBFEFFBFE # removes left-most board column of bits
			west >>= 1

	return lookup



def genSWAttkRays(): # SOUTH-WEST
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



def genSEAttkRays(): # SOUTH-EAST
	lookup = [None] * 100

	for row in range(9, -1, -1):
		aDiag = 0x40201008040201008040200 >> (10 * (9 - row))
		aDiag &= 0xFFFFFFFFFFFFFFFFFFFFFFFFF
		for col in range(10):
			lookup[row * 10 + col] = aDiag
			aDiag &= 0x7FDFF7FDFF7FDFF7FDFF7FDFF
			aDiag <<= 1 

	return lookup
		

# ATTACK-RAYS JSON FILE
# Functions to read and write the attackRays.json file that holds the precomputed
# attack-rays bitboards in dictionary of lists of integers.
# =====================================================================================
def writeAttkRaysFile():
	with open("attackRays.json", "w") as f:
		attkRays = {
			"NW": genNWAttkRays(),
			"N": genNAttkRays(),
			"NE": genNEAttkRays(),
			"E": genEAttkRays(),
			"SE": genSEAttkRays(),
			"S": genSAttkRays(),
			"SW": genSWAttkRays(),
			"W": genWAttkRays()
		}

		f.write(json.dumps(attkRays))


		
def readAttkRaysFile():
	with open("attackRays.json", "r") as f:
		return json.load(f)



# BITBOARD MANIPULATION 
# Simple functions to output and look at bitboards in a more human friendly manner.
# =====================================================================================
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



def examineBboardList(bboard):
	while True:
		cmd = input("Examine Bitboard at index (enter -1 to exit): ")

		if cmd == "-1":
			break
		
		printBboard(bboard[int(cmd)])
	



def hexifyBboardList(bblist):
	return [hex(el) for el in bblist]



def examineAttkRaysFile():
	index = readAttkRaysFile()

	while True:
		key = input("Piece key: ")

		while True:
			cmd = input("Examine Bitboard at index (enter -1 to exit): ")

			printBboard(index[key][int(cmd)])

			if cmd == "-1":
				break
			

def examGenKingAttkPiece():
	from main import genKingAttkPiece

	# indices = [1, 25, 60, 89]

	# for idx in indices:
	# 	print(f"SQUARE {idx}")
	# 	printBboardList(genKingAttkPiece(idx))

	for i in range(100):
		printBboard(genKingAttkPiece(i))



def examGenKnightAttkPiece():
	from main import genKnightAttkPiece

	# indices = [1, 25, 60, 89]

	# for idx in indices:
	# 	print(f"SQUARE {idx}")
	# 	printBboardList(genKnightAttkPiece(idx))

	for i in range(100):
		printBboard(genKnightAttkPiece(i))
	


def examGenPawnAttkPiece():
	from main import genPawnAttkPiece

	for i in range(100):
		printBboard(genPawnAttkPiece(i))
	


# BITSCAN INDEX GENERATION
# 
# Generation functions for a custom 128-bit (forward/reverse) Bitscan implementation
# using De Brujin multiplication. Each index is tied to a specific de brujin sequence.
# These functions do not reliable generate complete indexes depending on the inputted
# de brujin sequence.
# 
# For more details about the algorithms
# (Forward bitscan) https://www.chessprogramming.org/BitScan#De_Bruijn_Multiplication
# (Reverse bitscan) https://www.chessprogramming.org/BitScan#De_Bruijn_Multiplication_2
# =====================================================================================
def genDeBrujinIndex(valFunc, idxFunc, inGen):
	index = [None] * 128
	for i in inGen():
		if index[valFunc(i)] != None:
			print(f"CONFLICT at index {valFunc(i)} :: {index[valFunc(i)]} and {idxFunc(i)}")
		index[valFunc(i)] = idxFunc(i)

	return index



def genFBitscanIndex(debrujin):
	"""
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
	# printBboardList(genSEAttkRays())

	# print(hexifyBboardList(genWAttkRays()))

	# writeAttkRaysFile()
	# examineAttkRaysFile()

	examGenPawnAttkPiece()
	
