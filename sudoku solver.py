# -*- coding: utf-8 -*-
"""
Created on Tue Oct 21 11:50:18 2014

@author: jerry.prawiharjo
"""

import os
import sys

inFN = "Sudoku1.txt"
outFN = "Sudoku1-sol.txt"

class Sudoku(object):
    __X = 'ABCDEFGHI'
    __Y = 'abcdefghi'
    __SudokuList = []
    __ProblemList = []
    __SudokuBoxes = []

    def __init__(self):
        self.__makeList()
        self.__SudokuGrid = self.__convertToGrid(self.__SudokuList)
        self.__makeBoxes()
        self.__SudokuIterables = [self.__SudokuGrid, zip(*self.__SudokuGrid), self.__SudokuBoxes]
    
    def __makeList(self):
        self.__SudokuList = []
        for ch in self.__X:
            self.__SudokuList.extend([ch+a for a in self.__Y])

    def __makeBoxes(self):
        self.__SudokuBoxes = []
        x = ['ABC','DEF','GHI']
        y = ['abc','def','ghi']
        for kx in x:
            for ky in y:
                Boxes = []
                for ch in kx:
                    Boxes.extend([ch+a for a in ky])
                self.__SudokuBoxes.append(Boxes)
    
    def __convertToGrid(self,inList):
        outGrid = []
        if len(inList) == 81:
            for kk in range(0,9):
                outGrid.append(inList[kk*9:(kk+1)*9])
        return outGrid
        
    def PrintGrid(self,inGrid):
        for kk in range(0,9):
            print str(inGrid[kk][:]),
            print '\r'

    def read_csv(self,FileName):
        self.__ProblemList = []
        if os.path.exists(FileName):
            Wf = open(FileName)
            LinesRead = Wf.readlines()
            kcount = 1
            for line in LinesRead:
                TempArray = map(int,line.rstrip('\n').split(','))
                kcount +=1
                if len(TempArray) == 9:
                    self.__ProblemList.extend(TempArray)
                else:
                    print "Line %i in the input file has incorrect array length, or does not come in csv format" %kcount
                    return False
            if len(self.__ProblemList) == 81: 
                print "Input file successfully parsed"
            else:
                print "Input file has incorrect Sudoku row size"
                return False
            self.__assignDict()
            self.__ProblemGrid = self.__convertToGrid(self.__ProblemList)
            Wf.close()
            return True
        else:
            return False

    def CheckOutputFile(self,FN):
        if os.path.exists(FN):
            strask = "Output file exist, Overwrite file? [y/n] :"
            user_input = raw_input(strask)
            if user_input.upper() == 'Y':
                print ""
                return True
            else:
                print ""
                return False

    def write_csv(self,FileName):
        self.__ProblemList = []
        try:
            Wf = open(FileName,'w')
            for kx in self.__SolutionGrid:
                temp = str(kx)
                temp = temp[1:-1]
                Wf.write(temp + '\r\n')
            Wf.close()
            print "Successfully saved output file."
            return True
        except:
            print "Failed to save output file."
            return False

    def __assignDict(self):
        self.__SudokuDict = {}
        kc = 0
        for kx in self.__SudokuList:
            self.__SudokuDict[kx] = self.__ProblemList[kc]
            kc += 1

    def Singularity(self):
        replaced = True
        while replaced:
            replaced = False
            for kI in self.__SudokuIterables:
                for kx in kI:
                    Member = []
                    for ky in kx:
                        Member.append(self.__SudokuDict[ky])
                    if Member.count(0) == 1:
                        self.__SudokuDict[kx[Member.index(0)]] = 45 - sum(Member)
                        replaced = True
        return

    def Hitman(self):
        for kx in self.__SudokuBoxes:
            Nrange = range(1,10)
            Box = []
            for ki in kx:
                Box.append(self.__SudokuDict[ki])
            if Box.count(0) > 0:
                Nrange = list(set(Nrange) - set(Box))
            while Box.count(0) > 0:
                self.__SudokuDict[kx[Box.index(0)]] = Nrange[:]
                Box[Box.index(0)] = Nrange[:]

        Removed = True
        while Removed:
            Removed = False
            for kx in self.__SudokuBoxes: 
                for ki in kx:
                    if isinstance(self.__SudokuDict[ki],list):
                        if len(self.__SudokuDict[ki]) == 1:
                            self.__SudokuDict[ki] = self.__SudokuDict[ki][0]
                        else:
                            for mm in range(2):
                                if mm == 0:
                                    Indexer = [ki[0]+x for x in self.__Y]
                                elif mm == 1:
                                    Indexer = [x+ki[1] for x in self.__X]
                                Indexer.remove(ki)
                                for kR in Indexer:
                                    if not isinstance(self.__SudokuDict[kR],list):
                                        self.__SudokuDict[ki] = sorted(set(self.__SudokuDict[ki]) - set([self.__SudokuDict[kR]]))
                                        Removed = True
                                if len(self.__SudokuDict[ki]) == 1:
                                    self.__SudokuDict[ki] = self.__SudokuDict[ki][0]
            return Removed

    def FindTheRealMcCoy(self):
        Found = True
        while Found:
            Found = False
            for kI in self.__SudokuIterables:
                for kx in kI:
                    NonUniqueList = []
                    for ki in kx:
                        if isinstance(self.__SudokuDict[ki],list):
                            NonUniqueList.extend(self.__SudokuDict[ki])
                        else:
                            NonUniqueList.append(self.__SudokuDict[ki])
                    UniqueList = sorted(set(NonUniqueList))
                    for kb in UniqueList:
                        if NonUniqueList.count(kb) == 1:
                            for ki in kx:
                                if isinstance(self.__SudokuDict[ki],list):
                                    if kb in self.__SudokuDict[ki]:
                                        self.__SudokuDict[ki] = kb
                                        Found = True
            
            self.RemoveDoppelGaenger()

    def RemoveTheFakes(self):
        for mm in range(0,2):
            for kx in self.__SudokuBoxes:
                if mm == 0:
                    R1 = kx[0:3]
                    R2 = kx[3:6]
                    R3 = kx[6:]
                else:
                    R1 = kx[0::3]
                    R2 = kx[1::3]
                    R3 = kx[2::3]
                x1 = []
                x2 = []
                x3 = []
                for x in R1:
                    if isinstance(self.__SudokuDict[x],list):
                        x1.extend(self.__SudokuDict[x])
                for x in R2:
                    if isinstance(self.__SudokuDict[x],list):
                        x2.extend(self.__SudokuDict[x])
                for x in R3:
                    if isinstance(self.__SudokuDict[x],list):
                        x3.extend(self.__SudokuDict[x])
                x1 = set(x1)
                x2 = set(x2)
                x3 = set(x3)
                if len(x1.intersection(x2)) == 0 and len(x2.intersection(x3)) ==0 and len(x1.intersection(x3)) == 0:
                    if mm == 0:
                        CC1= list(set([R1[0][0] + x for x in self.__Y]) - set(R1))
                        CC2= list(set([R2[0][0] + x for x in self.__Y]) - set(R2))
                        CC3= list(set([R3[0][0] + x for x in self.__Y]) - set(R3))
                    else:
                        CC1= list(set([x + R1[0][1] for x in self.__X]) - set(R1))
                        CC2= list(set([x + R2[0][1] for x in self.__X]) - set(R2))
                        CC3= list(set([x + R3[0][1] for x in self.__X]) - set(R3))
                    
                    Z = [[CC1,x1],[CC2,x2],[CC3,x3]]
                    for kz in Z:
                        for kc in kz[0]:
                            if isinstance(self.__SudokuDict[kc],list):
                                if len(self.__SudokuDict[kc]) > 1:
                                    self.__SudokuDict[kc] = sorted(set(self.__SudokuDict[kc]) - kz[1])
                                if len(self.__SudokuDict[kc]) == 1:
                                    self.__SudokuDict[kc] = self.__SudokuDict[kc][0]
            self.RemoveDoppelGaenger()

    def RemoveDoppelGaenger(self):
        Removed = True
        while Removed:
            Removed = False
            for kI in self.__SudokuIterables:
                for kx in kI:
                    Members = []
                    for ky in kx:
                        if not isinstance(self.__SudokuDict[ky],list):
                            Members.append(self.__SudokuDict[ky])
                    for ky in kx:
                        if isinstance(self.__SudokuDict[ky],list):
                            self.__SudokuDict[ky] = sorted(set(self.__SudokuDict[ky]) - set(Members))
                            if len(self.__SudokuDict[ky]) == 1:
                                self.__SudokuDict[ky] = self.__SudokuDict[ky][0]
                        
    def DoubleDragon(self):
        Removed = True
        while Removed:
            Removed = False
            for kI in self.__SudokuIterables:
                for kx in kI:
                    Index = []
                    Members = []
                    for ky in kx:
                        if isinstance(self.__SudokuDict[ky],list):
                            if len(self.__SudokuDict[ky]) == 2:
                                Index.append(ky)
                                Members.append(self.__SudokuDict[ky])
                    if len(Index) == 2 and Members[0] == Members[1]:
                        kxx = list(kx[:])
                        kxx = sorted(set(kxx) - set(Index))
                        for ky in kxx:
                            if isinstance(self.__SudokuDict[ky],list):
                                self.__SudokuDict[ky] = sorted(set(self.__SudokuDict[ky]) - set(Members[0]))
                                Removed = True
    
    def CountEmptyCell(self):
        k = 0
        for kx in self.__SudokuBoxes:
            for ki in kx:
                if isinstance(self.__SudokuDict[ki],list):
                    k += 1
        return k

    def __SolutionDictToList(self):
        self.__SolutionList = []
        for kx in self.__SudokuGrid:
            for ky in kx:
                self.__SolutionList.append(self.__SudokuDict[ky])
        self.__SolutionGrid = self.__convertToGrid(self.__SolutionList)
    
    def Solve(self):
        self.Singularity()
        self.Hitman()
        for kk in range(10):
            self.FindTheRealMcCoy()
            self.DoubleDragon()
            self.RemoveTheFakes()
            Nempty = self.CountEmptyCell()
            if Nempty == 0:
                break
        self.__SolutionDictToList()
        if self.Metric(self.__SolutionGrid) == 0:
            print "Solution Found!"
            return True
        else:
            print "Failed to find solution!"
            return False

    def Metric(self,inGrid):
        SumRow = 0
        for k in range(0,9): 
            SumRow += abs(sum(inGrid[k]) - 45)
        
        SumCol = 0
        for l in range(0,9):
            SumCol += abs(sum(zip(*inGrid)[l]) - 45)
    
        SumBox = 0
        for l in range(0,3):
            for k in range(0,3):
                a = 0
                for m in range(0,3):
                    for n in range(0,3):
                        a += inGrid[m+(l*3)][n+(k*3)]
                SumBox += abs(a-45)
        return SumRow + SumCol + SumBox


if __name__ == "__main__":
    A = Sudoku()

    arg = sys.argv
    if len(arg) == 3:
        inFN = str(arg[1])
        outFN = str(arg[2])
    elif len(arg) == 2:
        inFN = arg[1]
        fn, ext = os.path.splitext(inFN)
        outFN = fn + '-sol' + ext
    else:
        print "No command line arguments. Using example files Sudoku1.txt"
    
    if True:#A.CheckOutputFile(outFN):
        print "Output will be saved to " + outFN
        if A.read_csv(inFN):
            A.Solve()
            A.write_csv(outFN)