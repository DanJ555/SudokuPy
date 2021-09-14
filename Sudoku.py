#python script to solve sudoku puzzles
#written by DanJ555

from random import choice
from copy import copy, deepcopy

class cell:

    #class will initialize it's list of possible values if not given a value 1-9
    def __init__(self,v):
        self.value = v
        if v == 0:
            self.PossibleVals = [1,2,3,4,5,6,7,8,9]
        else:
            self.PossibleVals = []
        self.Parents = [None,None,None] #Box, Row, Column

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)

    def __add__(self,other):
        return self.value+other

    def __radd__(self,other):
        return self.__add__(other)

    def getValue(self):
        return self.value

    #sets the value of the cell to the one provided in the parameters
    #will then go into the parents list and remove it's value from the
    #list of possibles from all cells sharing its box, row, and column
    def setValue(self,v):
        old_v = self.value
        self.value = v
        if self.value!=old_v: printSdk(grid)
        if v != 0: self.PossibleVals = []
        for p in self.Parents:
            try:
                for c in p:
                    c.removePossible(v)
            except AttributeError:
                pass

    def getPosVals(self):
        return self.PossibleVals

    #goes through the list of possible values and pops the one desired
    #if the list contains only one entry the list will pop that entry and
    #update the cell's value
    def removePossible(self,x):
        try:
            pos = self.PossibleVals.index(x)
            self.PossibleVals.pop(pos)
        except ValueError:
            pass
        if len(self.PossibleVals)==1 and self.value == 0:
            self.setValue(self.PossibleVals.pop(0))
            #self.PossibleVals = []

    #for some reason it was necessary to implement a remove that doesn't
    #update the value
    #might merge with faction above as to not repeat code
    def tempRemove(self,x):
        try:
            pos = self.PossibleVals.index(x)
            self.PossibleVals.pop(pos)
        except ValueError: pass



#grid, boxes, rows, and columns are currently stored as a list
#should update into a data structure for better manipulation and
#grid compatibility
grid = []
boxes = []
rows = []
columns = []

SudokuBook = [
	[0,0,0,0,6,7,0,0,0,   #diab
	 0,1,0,9,0,0,7,0,0,
	 0,0,0,0,0,3,9,4,0,
	 1,0,0,0,4,0,3,0,7,
	 0,6,0,0,0,0,0,8,0,
	 4,0,5,0,9,0,0,0,2,
	 0,5,3,2,0,0,0,0,0,
	 0,0,6,0,0,5,0,2,0,
	 0,0,0,8,3,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,   #hard
	 9,0,0,0,6,3,0,0,1,
	 0,0,6,0,2,7,9,5,0,
	 1,0,0,0,0,9,0,0,0,
	 4,7,3,0,0,0,1,6,9,
	 0,0,0,1,0,0,0,0,8,
	 0,8,4,3,1,0,6,0,0,
	 2,0,0,6,8,0,0,0,5,
	 0,0,0,0,0,0,0,0,0],
	[0,0,0,4,0,0,0,0,9,   #hard
	 9,0,3,0,2,0,4,0,0,
	 4,2,0,0,9,3,6,0,0,
	 6,0,0,0,0,0,5,0,0,
	 0,4,0,0,0,0,0,9,0,
	 0,0,7,0,0,0,0,0,3,
	 0,0,9,1,6,0,0,5,4,
	 0,0,4,0,3,0,8,0,1,
	 2,0,0,0,0,7,0,0,0],
	[0,7,0,0,0,8,0,0,0,   #diab
	 0,0,4,0,0,0,2,5,6,
	 0,6,0,0,0,2,0,0,7,
	 0,0,3,0,7,0,0,6,0,
	 0,0,0,8,0,3,0,0,0,
	 0,9,0,0,6,0,4,0,0,
	 2,0,0,3,0,0,0,9,0,
	 3,5,9,0,0,0,6,0,0,
	 0,0,0,7,0,0,0,1,0],
	[3,0,0,2,0,7,0,0,0,   #hard
	 4,0,0,0,0,1,0,0,0,
	 0,0,7,8,0,0,0,9,0,
	 5,8,0,6,0,0,0,0,4,
	 2,0,0,0,9,0,0,0,6,
	 6,0,0,0,0,4,0,1,9,
	 0,5,0,0,0,9,2,0,0,
	 0,0,0,3,0,5,0,0,8],
	[7,0,4,0,0,0,0,0,0,   #hard
	 0,0,6,0,8,5,0,4,0,
	 8,0,1,0,2,6,0,0,0,
	 0,0,7,8,0,0,0,0,4,
	 1,0,0,0,0,0,0,0,7,
	 2,0,0,0,0,7,3,0,0,
	 0,0,0,6,1,0,5,0,3,
	 0,8,0,3,5,0,1,0,0,
	 0,0,0,0,0,0,4,0,2],
	[0,0,0,1,0,0,7,0,2,
	 0,5,2,0,0,8,0,0,0,
	 0,0,3,4,2,0,0,0,0,
	 0,0,8,0,0,0,9,5,0,
	 9,0,0,0,0,0,0,0,6,
	 0,2,7,0,0,0,8,0,0,
	 0,0,0,0,3,4,5,0,0,
	 0,0,0,6,0,0,1,7,0,
	 6,0,4,0,0,9,0,0,0],
	[5,3,0,0,7,0,0,0,0,   #idk
	 6,0,0,1,9,5,0,0,0,
	 0,9,8,0,0,0,0,6,0,
	 8,0,0,0,6,0,0,0,3,
	 4,0,0,8,0,3,0,0,1,
	 7,0,0,0,2,0,0,0,6,
	 0,6,0,0,0,0,2,8,0,
	 0,0,0,4,1,9,0,0,5,
	 0,0,0,0,8,0,0,7,9]]

#make test grid
def simpleSdkPop():
    for i in range(9):
        for j in range(9):
            grid[i].append(j+1)

#turn list from puzzle book into a grid
def generatePuzzle(grid,puzzle):
    for i in puzzle:
        grid.append(cell(i))
    populateBoxes(grid)
    populateRows(grid)
    populateColumns(grid)
    return grid

#creates boxes
def populateBoxes(grid):
    box = -1
    for i, c in enumerate(grid):
        if (i%3) == 0: box+=1
        boxes[box].append(c)
        c.Parents[0] = boxes[box]
        if (i%9) == 8 and (i%27) != 26: box-=3

#creates rows
def populateRows(grid):
    for i in range(9):
        for j in range(0+9*i,9+9*i):
            #print(j)
            rows[i].append(grid[j])
            grid[j].Parents[1] = rows[i]

#creates columns
def populateColumns(grid):
    for i, c in enumerate(grid):
        columns[i%9].append(c)
        c.Parents[2] = columns[i%9]

#prints grid as a puzzle
def printSdk(grid):
    print("___________________")
    for i in range(9):
        string = "|"
        for j in range(0+9*i,9+9*i):
            if grid[j].getValue() == 0: string += (" |")
            else: string += (str(grid[j])+"|")
        print(string)
    print("‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾")

''' unused
def purgePos(lst):
    for i in lst:
        val = i.value()
        if val == 0: break
'''
#will solve a puzzle from the puzzle book
def solve(puzzle):
    clearGrid()
    global grid
    guessing = False
    guesses = []
    grid = generatePuzzle(grid,puzzle)
    copy_grid = deepcopy(grid)
    printSdk(grid)
    while not solved():
        updatePossibles()
        for h, lst in enumerate([boxes,rows,columns]):
            for l in lst:
                tallies = []
                for i in range(9):
                    tallies.append([])
                    for c in l:
                        if (i+1) in c.PossibleVals:
                            tallies[i].append(c)
                for t in tallies:
                    if len(t) == 1:
                        t[0].setValue(tallies.index(t)+1)
                if h==0:
                    tallies = []
                    for i in range(9):
                        tallies.append([])
                        for c in l:
                            if (i+1) in c.PossibleVals:
                                tallies[i].append(c)
                    for i, t in enumerate(tallies):
                        if 2 <= len(t) <= 3:
                            for par in range(2):
                                if t[0].Parents[par+1] == t[1].Parents[par+1] == t[-1].Parents[par+1]:
                                    for c in t[0].Parents[par+1]:
                                        c.tempRemove(i+1)
                                    for c in t:
                                        c.PossibleVals.append(i+1)
        #this part attempts to see if the puzzle is stuck
        if grid != copy_grid: copy_grid = copy(grid)
        elif grid == copy_grid:
            #if it is not guessing yet it sets a frame
            if not guessing:
                mgrid = deepcopy(grid)
                guessing = True
                #print("This puzzle is hard, let's try guessing")
                for i in grid:
                    if i.getValue() == 0:
                        g = choice(i.PossibleVals)
                        guesses.append(g)
                        i.setValue(g)
                        break
            elif guessing:
                #if solved(): break
                for i, c in enumerate(grid):
                    c.PossibleVals = [1,2,3,4,5,6,7,8,9]
                    c.value = mgrid[i].getValue()
                updatePossibles()
                for i in grid:
                    if i.getValue() == 0:
                        for g in guesses:
                            i.removePossible(g)
                        if i.getValue() == 0:
                            i.setValue(choice(i.PossibleVals))
                        break
                #print(grid)
                #print(mgrid)

#used to reinitialize grid's possible values due to laziness
def updatePossibles():
    for i in grid: i.setValue(i.getValue())

#will determine whether or not the grid is solved
#each box, row, and column needs a sum of 45 to return True
def solved():
    for area in (boxes,rows,columns):
        for i in area:
            total = 0
            for j in i: total += j
            if total != 45: return False
    print("Solved!")
    return True

#intialize grid or empty and reinitialize
def clearGrid():
    global grid, boxes, rows, columns
    grid = []
    boxes = []
    rows = []
    columns = []
    for i in [boxes,rows,columns]:
        for j in range(9):
            i.append([])

#currently cannot solve diabolic / very hard
#either impossible without guessing or requires logic i dont know
solve(SudokuBook[-1])
#printSdk()
