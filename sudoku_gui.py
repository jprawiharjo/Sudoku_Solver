# -*- coding: utf-8 -*-
"""
Created on Fri Oct 24 20:53:19 2014

@author: jerry.prawiharjo
"""

from Tkinter import *
from tkFileDialog import *
import sudoku_solver
import time

class StatusBar(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.label = Label(self, bd=1, relief=RAISED, anchor=W)
        self.label.pack(fill=X)

    def set(self, format, *args):
        self.label.config(text=format % args)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()

class MainForm(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        
        self.Sudoku = sudoku_solver.Sudoku()
        self.initUI()
        
    def initUI(self):
        self.parent.title("Sudoku Solver")
        self.pack(fill=BOTH, expand=1)
        
        
        self.file_opt = options = {}
        options['defaultextension'] = '.txt'
        options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
        options['initialdir'] = '.'
        options['initialfile'] = ''
        options['parent'] = self
        
        
        toolbar = Frame(self,bd = 1, relief = RAISED)


        b = Button(toolbar, text = 'Open', width=6, command=self.onOpen)
        b.pack(side=LEFT, padx=2, pady=2)
        
        b = Button(toolbar, text="Save", width=6, command=self.onSave)
        b.pack(side=LEFT, padx=2, pady=2)
        
        b = Button(toolbar, text="Solve", width=6, command=self.onSolve)
        b.pack(side=LEFT, padx=2, pady=2)

        toolbar.pack(side=TOP, fill=X)
        
        self.Cfont = ('Helvetica','24','bold')

        self.Length = 50
        self.Space = 10
        self.InitX = 30
        self.InitY = 30

        self.canvas = Canvas(self)
        self.canvas.pack()
        self.CreateGrid()
        self.initFillGrid()

        self.status = StatusBar(self.parent)
        self.status.pack(side=BOTTOM, fill=X)

    def onOpen(self):
        self.clearSudokuGrid()
        filename = askopenfilename(**self.file_opt)
        if filename != "" :
            success = self.Sudoku.read_csv(filename)
            if success:
                self.status.set("Input file successfully parsed")
            else:
                self.status.set("Failed to open file")
            self.setSudokuProblemGrid()

    def onSave(self):
        filename = asksaveasfilename(**self.file_opt)
        if filename != "":
            if self.Sudoku.write_csv(filename):
                self.status.set("Output file successfully saved")
            else:
                self.status.set("Output file not saved. No solution available")

    def onSolve(self):
        Tstart = time.clock()
        if self.Sudoku.Initialized:
            success = self.Sudoku.Solve()
            Telapsed = time.clock() - Tstart
            if success:
                self.status.set("Solution found in %0.3f s", Telapsed)
                self.setSudokuSolutionGrid()
            else:
                self.status.set("Failed find solution")
        else:
            self.status.set("No problem found")

    def setSudokuSolutionGrid(self):
        SudokuList = self.Sudoku.SudokuSolution
        for kk in range(81):
            self.canvas.itemconfigure(self.GridText[kk],text = SudokuList[kk])
            

    def setSudokuProblemGrid(self):
        SudokuList = self.Sudoku.SudokuList
        for kk in range(81):
            if SudokuList[kk] != 0:
                self.canvas.itemconfigure(self.GridText[kk],text = SudokuList[kk])
                self.canvas.itemconfigure(self.Grid[kk],fill = 'green', outline = 'green')
    
    def clearSudokuGrid(self):
        for kk in range(81):
            self.canvas.itemconfigure(self.Grid[kk],outline="#fb0", fill="#fb0")
            self.canvas.itemconfigure(self.GridText[kk],text = " ")

    def CreateGrid(self):
        Length = self.Length
        Space = self.Space
        InitX = self.InitX
        InitY = self.InitY
        self.Grid = []
        for ky in range(9):
            for kx in range(9):
                self.Grid.append(self.canvas.create_rectangle(InitX + kx * (Length + Space), 
                                             InitY + ky * (Length + Space), 
                                             InitX + Length + kx * (Length + Space), 
                                             InitY + Length + ky * (Length + Space), 
                                             outline="#fb0", fill="#fb0"))
        for kx in range(4):
            self.canvas.create_line(InitX - 5 + kx * 3 * (Length + Space), InitY - 5, 
                                    InitX - 5 + kx * 3 * (Length + Space), InitY - 5 + Length * 9 + Space * 9, width = 3)
        for kx in range(4):
            self.canvas.create_line(InitX - 5, InitY - 5 + kx * 3 * (Length + Space), 
                                    InitX - 5 + Length * 9 + Space * 9, InitY - 5 + kx * 3 * (Length + Space), width = 3 )
        self.canvas.pack(side = TOP, fill=BOTH, expand = 1)

    def initFillGrid(self):
        inGrid = range(81)
        if len(inGrid) == 81:
            self.GridText = []
            for ky in range(9):
                for kx in range(9):
                    self.GridText.append(self.canvas.create_text(self.InitX + self.Length/2 + kx * (self.Length + self.Space), 
                                                             self.InitY + self.Length/2 + ky * (self.Length + self.Space),
                                                             text=' ',font=self.Cfont))

def main():
    root = Tk()
    app = MainForm(root)
    root.geometry("590x650+200+100")
    root.resizable(0,0)
    root.mainloop()


if __name__ == '__main__':
    main()  