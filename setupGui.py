# -*- coding: utf-8 -*-
"""
Created on Sun Oct 26 16:28:07 2014

@author: jerry.prawiharjo
"""

import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"excludes": ["scipy","cvxopt","PySide","tcl"],
                     "includes":["Tkinter"],"include_msvcr":True,
                     'compressed':True,'copy_dependent_files':True,'create_shared_zip':True,
                     'include_in_shared_zip':True,'optimize':2}
# GUI applications require a different base on Windows (the default is for a
# console application).
base = "Win32GUI"

setup(  name = "Sudoku Solver GUI",
        version = "1.0",
        description = "Sudoku Solver in Python by Jerry Prawiharjo",
        options = {"build_exe": build_exe_options},
        executables = [Executable("sudoku_gui.py", base=base),
                       Executable("sudoku_solver.py", base=base)])
        
