Sudoku_Solver
=============

A Sudoku Solver in Python\n

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

Examples:
=========
sudoku1.txt : problem provided by John Joo

sudoku2.txt : Sudoku problem by Arto Inkala in 2006 [http://usatoday30.usatoday.com/news/offbeat/2006-11-06-sudoku_x.htm]

sudoku3.txt : Another sudoku problem by Arto Inkala. More difficult than sudoku2.txt [http://www.mirror.co.uk/news/weird-news/worlds-hardest-sudoku-can-you-242294]


GUI usage:

Open button: Open txt file that contains Sudoku problem in csv

Solve button: Solves the loaded sudoku problem

Save button: Saves the solution onto csv file.

User Input button: Using user input: User can input numbers directly on the grid

Read button: Press this to read the user input grid into the memory

Note:
========

There is a sudoku solver in Python by Peter Norvig [http://norvig.com/sudoku.html]

This solver has been checked against Norvig's problem collection 'hard.txt' and 'hardest.txt'

Disclaimer: This code does not copy Norvig's algorithm in any way.

