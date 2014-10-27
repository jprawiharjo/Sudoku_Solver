Sudoku_Solver
=============================

**A Sudoku Solver in Python**

***usage***: `python sudoku_solver.py [input.txt] [output.txt]`

* `input.txt`: Input sudoku problem, in the form of csv, e.g.

    0,3,5,2,9,0,8,6,4  
    0,8,2,4,1,0,7,0,3  
    7,6,4,3,8,0,0,9,0  
    2,1,8,7,3,9,0,4,0  
    0,0,0,8,0,4,2,3,0  
    0,4,3,0,5,2,9,7,0  
    4,0,6,5,7,1,0,0,9  
    3,5,9,0,2,8,4,1,7  
    8,0,0,9,0,0,5,2,6  


* `output.txt`: Optional. Output file. If the filename already exists, it will be overwritten.  
If it's not supplied, it will be in the form of "input-sol.txt"

The python code calls for **os**, **sys**, and **collections** libraries

## GUI: ##

***usage***: `python sudoku_gui.py`

<a href="http://tinypic.com?ref=29wsjd2" target="_blank"><img src="http://i62.tinypic.com/29wsjd2.png" border="0" alt="Image and video hosting by TinyPic"></a>

**Open button**: Open txt file that contains Sudoku problem in csv format

**Save button**: Saves the solution onto csv file, or the current grid, if the problem is not already solved

**Solve button**: Solves the loaded sudoku problem

**User Input button**: Using user input mode: It will clear the grid and allow the user to input numbers directly on the grid

**User Input button**: Self-explanatory

*Notes*: Before pressing solve, user can still edit the loaded grid

This code calls for sudoku_solver.py, and use Tkinter [tkFileDialog, tkMessageBox] for GUI

## Stand-alone: ##

***usage***: `python setupGui.py build`

This will create executable under `.\build\` using cx_Freeze


## Example Files: ##

**sudoku1.txt**: problem provided by John Joo

**sudoku2.txt**: Sudoku problem by Arto Inkala, c.2006 
[[http://usatoday30.usatoday.com/news/offbeat/2006-11-06-sudoku_x.htm]](http://usatoday30.usatoday.com/news/offbeat/2006-11-06-sudoku_x.htm "Created by Arto Inkala c.2006")

**sudoku3.txt**: Dubbed the world's most difficult sudoku problem, by Arto Inkala, c.2010. More difficult than sudoku2.txt [[http://www.mirror.co.uk/news/weird-news/worlds-hardest-sudoku-can-you-242294]](http://www.mirror.co.uk/news/weird-news/worlds-hardest-sudoku-can-you-242294 "Dubbed the world's most difficult Sudoku, by Arto Inkala, c. 2010")

**sudoku4.txt**: Yet another hard sudoku problem


## Notes: ##

There is a sudoku solver in Python by Peter Norvig [[http://norvig.com/sudoku.html]](http://norvig.com/sudoku.html)

This solver has been checked against Norvig's problem collection 'hard.txt' and 'hardest.txt'

**Disclaimer**: This code does not copy nor use Norvig's code in any way.

