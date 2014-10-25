Sudoku_Solver
=============

A Sudoku Solver in Python

usage: python sudoku_solver.py "input.txt" "output.txt"

input.txt: Input sudoku problem, in the form of csv, e.g.
0,3,5,2,9,0,8,6,4
0,8,2,4,1,0,7,0,3
7,6,4,3,8,0,0,9,0
2,1,8,7,3,9,0,4,0
0,0,0,8,0,4,2,3,0
0,4,3,0,5,2,9,7,0
4,0,6,5,7,1,0,0,9
3,5,9,0,2,8,4,1,7
8,0,0,9,0,0,5,2,6

output.txt: Optional. Output file. If the filename already exists, it will be overwritten.
If it's not supplied, it will be in the form of "input-sol.txt"

The program makes use of os, sys, and collections libraries
