# -*- coding: utf-8 -*-
"""
Created on Fri Oct 24 20:53:19 2014

@author: jerry.prawiharjo
"""

from Tkinter import *
from tkFileDialog import *
import sudoku_solver
import time
import threading

class StatusBar(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.label = Label(self, bd=1, relief=RAISED, anchor=W, font = ('Helvetica','14'))
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
        
        self.UserInput = False
        
        self.UnoccColor = "#fb0"
        self.OccColor = 'green'
        
        self.file_opt = options = {}
        options['defaultextension'] = '.txt'
        options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
        options['initialdir'] = '.'
        options['initialfile'] = ''
        options['parent'] = self
        
        
        toolbar = Frame(self,bd = 1, relief = RAISED)
        self.Tfont = ('Helvetica','12','bold')

        b = Button(toolbar, text = 'Open', width=6, command=self.onOpen, font = self.Tfont)
        b.pack(side=LEFT, padx=2, pady=2)
        
        b = Button(toolbar, text="Save", width=6, command=self.onSave, font = self.Tfont)
        b.pack(side=LEFT, padx=2, pady=2)
        
        b = Button(toolbar, text="Solve", width=6, command=self.onSolve, font = self.Tfont)
        b.pack(side=LEFT, padx=2, pady=2)

        self.btnClear = Button(toolbar, text="User Input", width=8,
                               command=self.onClear, font = self.Tfont)
        self.btnClear.pack(side=LEFT, padx=2, pady=2)

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

        self.canvas.bind("<Double-Button-1>", self.set_focus)
        self.canvas.bind("<Button-1>", self.set_focus)
        self.canvas.bind("<Key>", self.handle_key)

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
            self.UserInput = False

    def onSave(self):
        if self.Sudoku.Solved:
            self.status.set("Saving solution grid...")
            filename = asksaveasfilename(**self.file_opt)
            if filename != "":
                if self.Sudoku.write_csv(filename):
                    self.status.set("Solution successfully saved")
                else:
                    self.status.set("There was an error when attempting to save output file")
            else:
                    self.status.set("Output file not saved. No filename supplied")
        elif self.Sudoku.Initialized:
            self.status.set("Saving current Sudoku grid")
            filename = asksaveasfilename(**self.file_opt)
            if filename != "":
                if self.Sudoku.write_csv(filename,Solution = False):
                    self.status.set("Current grid is successfully saved")
        else:
            self.status.set("!There is nothing to save!")

    def onSolve(self):
        Tstart = time.clock()
        if self.Sudoku.Initialized:
            success = self.Sudoku.Solve()
            Telapsed = time.clock() - Tstart
            if success:
                self.status.set("Solution found in %0.3f s", Telapsed)
                self.setSudokuSolutionGrid()
            else:
                if not(self.Sudoku.CheckMinClue):
                    self.status.set("Sudoku does not have the minimum number of clues [%i]" 
                                    %self.Sudoku.MinClue)
                elif not(self.Sudoku.ValidateProblem):
                    self.status.set("Sudoku problem is ill-posed")
                else:
                    self.status.set("Failed find solution")
        else:
            self.status.set("No problem found")
            
    def onClear(self):
        self.UserInput = True
        self.SudokuList = [0] * 81
        self.clearSudokuGrid()
        self.status.set("User input mode. Directly input values in the grid")
        self.focus()

    def setSudokuSolutionGrid(self):
        SudokuList = self.Sudoku.SudokuSolution
        for kk in range(81):
            self.canvas.itemconfigure(self.GridText[kk],text = SudokuList[kk])

    def setSudokuProblemGrid(self):
        SudokuList = self.Sudoku.SudokuList
        for kk in range(81):
            if SudokuList[kk] != 0:
                self.canvas.itemconfigure(self.GridText[kk],text = SudokuList[kk])
                self.canvas.itemconfigure(self.Grid[kk],fill = self.OccColor, outline = self.OccColor)
    
    def clearSudokuGrid(self):
        for kk in range(81):
            self.canvas.itemconfigure(self.Grid[kk],outline=self.UnoccColor, fill=self.UnoccColor)
            self.canvas.itemconfigure(self.GridText[kk],text = " ")
        self.Sudoku.Initialized = False
        self.status.clear()

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
                                             outline=self.UnoccColor, fill=self.UnoccColor))
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

    def set_focus(self, event):
        if self.canvas.type(CURRENT) != "text":
            return
        if self.UserInput:
            self.canvas.focus_set() # move focus to canvas
            self.canvas.focus(CURRENT) # set focus to text item
            self.canvas.select_from(CURRENT, 0)
            self.canvas.select_to(CURRENT, END)

    def handle_key(self, event):
        item = self.canvas.focus()
        if not item:
            return

        itemindex = int(item) - self.GridText[0]        
        insert = self.canvas.index(item, INSERT)
        
        AllowedChars = '123456789'

        if event.char in AllowedChars + ' ':
            if self.canvas.select_item():
                self.canvas.dchars(item, SEL_FIRST, SEL_LAST)
                self.canvas.select_clear()
            if insert < 1:
                self.canvas.insert(item, "insert", event.char)
        elif event.keysym == "BackSpace":
            if self.canvas.select_item():
                self.canvas.dchars(item, SEL_FIRST, SEL_LAST)
                self.canvas.select_clear()
            else:
                if insert > 0:
                    self.canvas.dchars(item, insert-1, insert)
        elif event.keysym == "Right":
            self.canvas.icursor(item, insert+1)
            self.canvas.select_clear()
        elif event.keysym == "Left":
            self.canvas.icursor(item, insert-1)
            self.canvas.select_clear()
        else:
            pass
        
        if self.canvas.itemcget(self.GridText[itemindex],'text') == '':
            self.canvas.itemconfigure(self.GridText[itemindex], text = ' ')
            
        if self.canvas.itemcget(self.GridText[itemindex],'text') in AllowedChars:
            self.canvas.itemconfigure(self.Grid[itemindex], fill = self.OccColor, outline = self.OccColor)
            self.SudokuList[itemindex] = int(self.canvas.itemcget(self.GridText[itemindex],'text'))
        elif self.canvas.itemcget(self.GridText[itemindex],'text') == '':
            self.canvas.itemconfigure(self.Grid[itemindex], fill=self.UnoccColor, outline=self.UnoccColor)
            self.SudokuList[itemindex] = 0
        else:
            self.canvas.itemconfigure(self.Grid[itemindex], fill=self.UnoccColor, outline=self.UnoccColor)
            self.SudokuList[itemindex] = 0
        
        self.Sudoku.SudokuList = self.SudokuList

def main():
    root = Tk()
    app = MainForm(root)
    root.geometry("590x670+200+100")
    root.resizable(0,0)
    root.mainloop()


if __name__ == '__main__':
    main()  