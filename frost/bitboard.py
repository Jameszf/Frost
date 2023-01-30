
# Bit manipulation
def flipBit(bboard, pos): return bboard ^ (1 << pos) # Flip bit at pos.
def setBit(bboard, pos): return bboard | (1 << pos) # Set bit at pos to be 1.
def clearBit(bboard, pos): return bboard & ~(1 << pos) # Set bit at pos to be 0.
def getBit(bboard, pos): return 1 if (bboard & (1 << pos)) != 0 else 0


def ls1b(bboard): return bboard & -bboard 
def ms1b(bboard):
	# bitboard cannot be larger than 128 bits for ms1b() to work
	assert bboard < 0x100000000000000000000000000000000

	n = bboard
	n |= n >> 1
	n |= n >> 2
	n |= n >> 4
	n |= n >> 8
	n |= n >> 16
	n |= n >> 32
	n |= n >> 64
	return (n + 1) >> 1 
	

# bitscans
def rBitscan(bboard):
	"""
	128-bit Reverse Bitscan implementation using De Brujin multiplication.
	
	Details: https://www.chessprogramming.org/BitScan#De_Bruijn_Multiplication	
	"""

	if bboard == 0: return 0
	
	index = [0, 1, 2, 8, 3, 15, 9, 22, 4, 29,
			 16, 36, 10, 43, 23, 50, 5, 33, 30,
			 57, 17, 64, 37, 71, 11, 60, 44, 78,
			 24, 85, 51, 92, 6, 20, 34, 48, 31,
			 69, 58, 90, 18, 67, 65, 99, 38, 101,
			 72, 106, 12, 40, 61, 82, 45, 103, 79,
			 113, 25, 74, 86, 116, 52, 108, 93, 120,
			 127, 7, 14, 21, 28, 35, 42, 49, 32, 56,
			 63, 70, 59, 77, 84, 91, 19, 47, 68, 89,
			 66, 98, 100, 105, 39, 81, 102, 112, 73,
			 115, 107, 119, 126, 13, 27, 41, 55, 62,
			 76, 83, 46, 88, 97, 104, 80, 111, 114,
			 118, 125, 26, 54, 75, 87, 96, 110, 117,
			 124, 53, 95, 109, 123, 94, 122, 121]
	debrujin = 0x1061438916347932A5CD9D3EAD7B77F 
	shift = ls1b(bboard)
	return index[((debrujin * shift) & 0xFE000000000000000000000000000000) >> 121]



def fBitscan(bboard):
	"""
	128-bit Forward Bitscan implementation using De Brujin multiplication.

	Details: https://www.chessprogramming.org/BitScan#De_Bruijn_Multiplication_2
	"""

	if bboard == 0: return 0
	
	index = [0, 69, 1, 27, 70, 113, 2, 13, 28, 97,
			 71, 55, 114, 17, 3, 124, 14, 83, 29,
			 41, 98, 86, 72, 65, 56, 46, 115, 60,
			 18, 32, 4, 125, 111, 95, 15, 81, 84,
			 44, 30, 109, 42, 107, 99, 50, 87, 101,
			 73, 66, 52, 38, 57, 92, 47, 89, 116,
			 23, 61, 103, 19, 119, 33, 75, 5, 126,
			 68, 26, 112, 12, 96, 54, 16, 123, 82,
			 40, 85, 64, 45, 59, 31, 110, 94, 80,
			 43, 108, 106, 49, 100, 51, 37, 91, 88,
			 22, 102, 118, 74, 67, 25, 11, 53, 122,
			 39, 63, 58, 93, 79, 105, 48, 36, 90,
			 21, 117, 24, 10, 121, 62, 78, 104, 35,
			 20, 9, 120, 77, 34, 8, 76, 7, 6, 127]
	
	debrujin = 0x1FC47709ECA6B19CC17D25B45754379
	
	ms = bboard
	ms |= ms >> 1
	ms |= ms >> 2
	ms |= ms >> 4
	ms |= ms >> 8
	ms |= ms >> 16
	ms |= ms >> 32
	ms |= ms >> 64

	return index[((debrujin * ms) & 0xFE000000000000000000000000000000) >> 121]
