# The idea of the solution is to use bitwise
# Each coordinate in the cube represents a bit position in a 125-bit integer
# The index, 0-124, can be converted to represent a level, row, and column

def getLevelRowCol(i):
  return([int(i / 25),  int((i / 5) % 5), int(i % 5)])

# The idea of the puzzle is to add one piece at a time
# For any given empty cell, there are 24 positions for the next piece
# This hashtag outlines the other cells occupied by each piece

pieceMap = {"A":[25, 50, 75, 20],"B": [25, 50, 75, 45],"C": [25, 50, 75, 26],"D": [25, 50, 75, 51],"E": [25, 50, 75, 30],"F": [25, 50, 75, 55],"G": [25, 50, 75, 24],"H": [25, 50, 75, 49],"I": [24, 25, 26, 23],"J": [24, 25, 26, 27],"K": [20, 25, 30, 15],"L": [20, 25, 30, 35],"M": [4, 5, 6, 3],"N": [4, 5, 6, 7],"O": [5, 10, 15, 4],"P": [5, 10, 15, 9],"Q": [5, 10, 15, 30],"R": [5, 10, 15, 35],"S": [5, 10, 15, 6],"T": [5, 10, 15, 11],"U": [1, 2, 3, 26],"V": [1, 2, 3, 27],"W": [1, 2, 3, 6],"X": [1, 2, 3, 7]}

pieces = {}
pieceByIndex = {}

# this converts cell positions from the pieceMap into a bitwise interger
def calcBitsFromList(l):
  return (1 + (1 << l[0]) + (1 << l[1]) + (1 << l[2]) + (1 << l[3]))

for piece in pieceMap:
    pieces[piece] = calcBitsFromList(pieceMap[piece])

# this generates a dictionary of valid pieces for any given cell
for i in range(125):
    pieceByIndex[i] = []
    level, row, col = getLevelRowCol(i)
    if level < 2:
        if row > 0:
            pieceByIndex[i].extend(["A", "B"])
        if row < 4:
            pieceByIndex[i].extend(["E", "F"])
        if col > 0:
            pieceByIndex[i].extend(["G", "H"])
        if col < 4:
            pieceByIndex[i].extend(["C", "D"])
    if level < 4:
        if col > 1 and col < 4:
            pieceByIndex[i].append("I")
        if row > 1 and row < 4:
            pieceByIndex[i].append("K")
        if col > 0 and col < 3:
            pieceByIndex[i].append("J")
        if row > 0 and row < 3:
            pieceByIndex[i].append("L")
    if row < 4:
        if col > 1 and col < 4:
            pieceByIndex[i].append("M")
        if col > 0 and col < 3:
            pieceByIndex[i].append("N")
    if row < 2:
        if col > 0:
            pieceByIndex[i].extend(["O", "P"])
        if level < 4:
            pieceByIndex[i].extend(["Q", "R"])
        if col < 4:
            pieceByIndex[i].extend(["S", "T"])
    if col < 2:
        if level < 4:
            pieceByIndex[i].extend(["U", "V"])
        if row < 4:
            pieceByIndex[i].extend(["W", "X"])

solutionsFound = 0
deadEndsFound = 0

# recursive function to add one piece at a time
def addPiece(moves, nextEmptyCell, puzzle):
    global solutionsFound
    global deadEndsFound
    deadEnd = True
    # finds next empty cell that needs to be filled
    while ((puzzle >> nextEmptyCell) & 1):
        nextEmptyCell += 1
    # we generated the list of valid pieces for any given index earlier
    # now we iterate through those options
    for piece in pieceByIndex[nextEmptyCell]:
        # converts piece to appropriate bitwise interger
        pieceBits = pieces[piece] << nextEmptyCell
        # checks to see if current puzzle has room for piece
        if pieceBits & puzzle != 0:
            continue
        deadEnd = False
        movesCopy = list(moves)
        movesCopy.append(tuple([nextEmptyCell, piece]))
        # if the list of moves == 25, then the puzzle must be complete
        if len(movesCopy) == 25:
            solutionsFound += 1
            print(solutionsFound)
            printSolution(movesCopy)
            return
        addPiece(movesCopy, nextEmptyCell, pieceBits | puzzle)
    # it can take a while before first solution is found
    # this is so user doesn't think the program frozen
    if deadEnd:
        deadEndsFound += 1
        if deadEndsFound % 1000000 == 0:
            print (str(int(deadEndsFound / 1000000)),"million dead ends found")

# outputs the solution in a way that the user can reconstruct
def printSolution(moves):
    output = [""] * 125
    for i in range(25):
        index, piece = moves[i]
        letter = "abcdefghijklmnopqrstuvwxyz"[i]
        output[index] = letter
        for position in pieceMap[piece]:
            output[index + position] = letter
    output = "".join(output)
    print (output[0:5], output[25:30], output[50:55], output[75:80], output[100:105])
    print (output[5:10], output[30:35], output[55:60], output[80:85], output[105:110])
    print (output[10:15], output[35:40], output[60:65], output[85:90], output[110:115])
    print (output[15:20], output[40:45], output[65:70], output[90:95], output[115:120])
    print (output[20:25], output[45:50], output[70:75], output[95:100], output[120:125])
    print ("")
    return

addPiece([], 0, 0)
