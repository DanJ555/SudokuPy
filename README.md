# SudokuPy
This is a simple script to solve sudoku puzzles I got the idea bored out of my mind at warfighter. Sites that randomly generate puzzles have 4 catagories: easy, normal, hard,
really hard. While doing a puzzle I thought about the algorithm I was doing to solve them and how it failed with the hardest tier. I then wrote this script to prove to myself the
hardest tier really does need guessing to solve. As such, this script will easily solve tiers 1-3, but I haven't quiet gotten it to consistently solve 4. I think it still bugs out
with some puzzles. I want to come back to this when I have a proper row,column,&9x9 box objects, and not just lists inside lists containing the cell object, to see if I can
implement better guessing.

*********************
****THE ALGORITHM****
*********************

This is how I solve difficult puzzles and should essentially still be the same process the code follows. Nothing unique, just book keeping. After checking the whole grid and
filling in obvious cells, I'll denote each number each cell can be tiny so as to fit in the space. I'll then check each box's possible values against it's neighbors in its box,
row, and column. If cell's book keeping is whittled down to a single number then it must be that number, as it can't allow any other. If it is the only cell of its box, row, or
column that has the possibility of being a number then it must clearly be that number, as no other cell in its group allows for it. Then I'll update the book keeping for all
neighboring cells.

This is essentially what the script does. Every cell has it's value but also has a shadow list, 0-9, of values it can be. This list is continuously updated as another cell from 
one of its parent groups will eliminate it's newly deduced value from the shadow list of all other cells in all three of its parent lists. Then in the solve() function the script
will tally up possible values for each cell in each box, row, or column and notice whether a value only appears once and update the cell with the corresponding shadowlist that 
contained the unique value.
