# -*- coding: utf-8 -*-
"""
Created on Tue Oct 21 11:50:18 2014

@author: jerry.prawiharjo
"""

import os
import sys
from collections import *
import time

inFN = "sudoku3.txt"
outFN = "sudoku3-sol.txt"

class Sudoku(object):
    __X = 'ABCDEFGHI'
    __Y = 'abcdefghi'
    __SudokuKeyList = []
    __ProblemList = []
    __SudokuBoxes = []
    MinClue = 17
    
    def __init__(self):
        self.__makeList()
        self.__SudokuGrid = self.__convertToGrid(self.__SudokuKeyList)
        self.__makeBoxes()
        self.__SudokuIterables = [self.__SudokuGrid, zip(*self.__SudokuGrid), self.__SudokuBoxes]
        self.Initialized = False
        self.Solved = False
    
    def __makeList(self):
        self.__SudokuKeyList = []
        for ch in self.__X:
            self.__SudokuKeyList.extend([ch+a for a in self.__Y])

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

    @property
    def ValidateProblem(self):
        if self.Initialized:
            for kI in self.__SudokuIterables:
                for kx in kI:
                    MembersList = []
                    for ky in kx:
                        if isinstance(self.__SudokuDict[ky],int):
                            if self.__SudokuDict[ky] > 0:
                                MembersList.append(self.__SudokuDict[ky])
                        MembersSet = set(MembersList)
                        if len(MembersSet) != len(MembersList):
                            return False
            return True
        else:
            return False
    
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

    def read_csv(self,FileName,verbose = False):
        self.__ProblemList = []
        if os.path.exists(FileName):
            Wf = open(FileName)
            LinesRead = Wf.readlines()
            Wf.close()
            kcount = 0
            for line in LinesRead:
                TempArray = map(int,line.rstrip('\n').split(','))
                kcount +=1
                if len(TempArray) == 9:
                    self.__ProblemList.extend(TempArray)
                else:
                    if verbose: print "Error parsing input file: Line %i in the input file has incorrect array length, or does not come in csv format" %kcount
                    return False
            if len(self.__ProblemList) == 81: 
                if verbose: print "Input file successfully parsed"
            else:
                if verbose: print "Error parsing input file: Input file has incorrect Sudoku row size"
                return False
            self.__assignDict()
            self.__ProblemGrid = self.__convertToGrid(self.__ProblemList)
            self.Initialized = True
            return True
        else:
            if verbose: print "Input file does not exist!"
            return False

    def __getSudokuList(self):
        return self.__ProblemList

    def __setSudokuList(self,inList):
        if len(inList) == 81:
            self.__ProblemList = inList[:]
            self.__assignDict()
            self.__ProblemGrid = self.__convertToGrid(self.__ProblemList)
            self.Initialized = True
            return True
        else:
            return False
    
    SudokuList = property(fget = __getSudokuList,fset = __setSudokuList)

    def Clear(self):
        self.Solved = False
        self.Initialized = False
        
    def parse_string_grid(self,inString):
        inString = inString.rstrip('\n')
        self.__ProblemList = []
        if len(inString) == 81:
            for k in inString:
                if k == '.':
                    k = '0'
                self.__ProblemList.append(int(k))
        self.__assignDict()
        self.__ProblemGrid = self.__convertToGrid(self.__ProblemList)

    def CheckOutputFile(self,FN):
        if os.path.exists(FN):
            strask = "Output file exists, Overwrite file? [y/n] : "
            user_input = raw_input(strask)
            if user_input.upper() == 'Y':
                print ""
                return True
            else:
                print ""
                return False
        else:
            return True

    def CheckOutputFileExists(self,FN):
        if os.path.exists(FN):
            print "Output file exists, it will be overwritten"
        else:
            print FN + " will be created"
        return True
            
    def write_csv(self,FileName,verbose = False, Solution = True):
        if Solution:
            OutGrid = self.__SolutionGrid
        else:
            OutGrid = self.__ProblemGrid
        try:
            Wf = open(FileName,'w')
            for kx in OutGrid:
                temp = str(kx)
                temp = temp[1:-1]
                Wf.write(temp.replace(' ','') + '\n')
            Wf.close()
            if verbose: print "Successfully saved output file"
            return True
        except:
            if verbose: print "Failed to save output file."
            return False

    def __assignDict(self):
        self.__SudokuDict = {}
        kc = 0
        for kx in self.__SudokuKeyList:
            self.__SudokuDict[kx] = self.__ProblemList[kc]
            kc += 1
        self.__SudokuDict = OrderedDict(sorted(self.__SudokuDict.items(), key = lambda t:t[0]))

    def __Singularity(self):
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

    def __ReduceProblemSpace(self):
        for kx in self.__SudokuBoxes:
            Nrange = set(range(1,10))
            Box = []
            for ki in kx:
                Box.append(self.__SudokuDict[ki])
            if Box.count(0) > 0:
                Nrange = Nrange - set(Box)
            while Box.count(0) > 0:
                self.__SudokuDict[kx[Box.index(0)]] = Nrange.copy()
                Box[Box.index(0)] = list(Nrange.copy())

        Removed = True
        while Removed:
            for kx in self.__SudokuBoxes:
                Removed = False
                for ki in kx:
                    if isinstance(self.__SudokuDict[ki],set):
                        if len(self.__SudokuDict[ki]) == 1:
                            self.__SudokuDict[ki] = self.__SudokuDict[ki].pop()
                        else:
                            for mm in range(2):
                                if mm == 0:
                                    Indexer = [ki[0]+x for x in self.__Y]
                                elif mm == 1:
                                    Indexer = [x+ki[1] for x in self.__X]
                                Indexer.remove(ki)
                                for kR in Indexer:
                                    if not isinstance(self.__SudokuDict[kR],set) and isinstance(self.__SudokuDict[ki],set):
                                        if len(self.__SudokuDict[ki]) > 1:
                                            orig = self.__SudokuDict[ki]
                                            self.__SudokuDict[ki] = self.__SudokuDict[ki] - set([self.__SudokuDict[kR]])
                                            if orig != self.__SudokuDict[ki]:                                            
                                                Removed = True
                                        if len(self.__SudokuDict[ki]) == 1:
                                            self.__SudokuDict[ki] = self.__SudokuDict[ki].pop()
                                        elif len(self.__SudokuDict[ki]) == 0:
                                            self.__SudokuDict[ki] = 0

    def __FindUniqueValue(self):
        Found = True
        while Found:
            Found = False
            for kI in self.__SudokuIterables:
                for kx in kI:
                    NonUniqueList = []
                    for ki in kx:
                        if isinstance(self.__SudokuDict[ki],set):
                            NonUniqueList.extend(list(self.__SudokuDict[ki]))
                        else:
                            NonUniqueList.append(self.__SudokuDict[ki])
                    UniqueList = set(NonUniqueList)
                    for kb in UniqueList:
                        if NonUniqueList.count(kb) == 1:
                            for ki in kx:
                                if isinstance(self.__SudokuDict[ki],set):
                                    if kb in self.__SudokuDict[ki]:
                                        self.__SudokuDict[ki] = kb
                                        Found = True
            self.__RemoveDuplicates()

    def __EliminateOccupiedValues(self):
        for mm in range(0,2):
            for kx in self.__SudokuBoxes:
                if mm == 0:
                    R1 = set(kx[0:3])
                    R2 = set(kx[3:6])
                    R3 = set(kx[6:])
                else:
                    R1 = set(kx[0::3])
                    R2 = set(kx[1::3])
                    R3 = set(kx[2::3])
                x1 = set([])
                x2 = set([])
                x3 = set([])
                for x in R1:
                    if isinstance(self.__SudokuDict[x],set):
                        x1.union(self.__SudokuDict[x])
                for x in R2:
                    if isinstance(self.__SudokuDict[x],set):
                        x2.union(self.__SudokuDict[x])
                for x in R3:
                    if isinstance(self.__SudokuDict[x],set):
                        x3.union(self.__SudokuDict[x])
                if len(x1.intersection(x2)) == 0 and len(x2.intersection(x3)) ==0 and len(x1.intersection(x3)) == 0:
                    if mm == 0:
                        CC1= set([sorted(R1)[0][0] + x for x in self.__Y]) - R1
                        CC2= set([sorted(R2)[0][0] + x for x in self.__Y]) - R2
                        CC3= set([sorted(R3)[0][0] + x for x in self.__Y]) - R3
                    else:
                        CC1= set([x + sorted(R1)[0][1] for x in self.__X]) - R1
                        CC2= set([x + sorted(R2)[0][1] for x in self.__X]) - R2
                        CC3= set([x + sorted(R3)[0][1] for x in self.__X]) - R3
                    
                    Z = [[CC1,x1],[CC2,x2],[CC3,x3]]
                    for kz in Z:
                        for kc in kz[0]:
                            if isinstance(self.__SudokuDict[kc],set):
                                if len(self.__SudokuDict[kc]) > 1:
                                    self.__SudokuDict[kc] = self.__SudokuDict[kc] - kz[1]
                                if len(self.__SudokuDict[kc]) == 1:
                                    self.__SudokuDict[kc] = self.__SudokuDict[kc].pop()
                                elif len(self.__SudokuDict[kc]) == 0:
                                    self.__SudokuDict[kc] = 0
            self.__RemoveDuplicates()

    def __RemoveDuplicates(self):
        Removed = True
        while Removed:
            for kI in self.__SudokuIterables:
                Removed = False
                for kx in kI:
                    Members = set([])
                    for ky in kx:
                        if not isinstance(self.__SudokuDict[ky],set):
                            Members.add(self.__SudokuDict[ky])
                    for ky in kx:
                        if isinstance(self.__SudokuDict[ky],set):
                            orig = self.__SudokuDict[ky].copy()
                            self.__SudokuDict[ky] = self.__SudokuDict[ky] - Members
                            if orig != self.__SudokuDict[ky]:
                                Removed = True
                            if len(self.__SudokuDict[ky]) == 1:
                                self.__SudokuDict[ky] = self.__SudokuDict[ky].pop()
                            elif len(self.__SudokuDict[ky]) == 0:
                                self.__SudokuDict[ky] = 0
                        
    def __DoubleValueStrategy(self):
        Removed = True
        while Removed:
            for kI in self.__SudokuIterables:
                Removed = False
                for kx in kI:
                    Index = []
                    Members = []
                    for ky in kx:
                        if isinstance(self.__SudokuDict[ky],set):
                            if len(self.__SudokuDict[ky]) == 2:
                                Index.append(ky)
                                Members.append(self.__SudokuDict[ky])
                    if len(Index) == 2 and Members[0] == Members[1]:
                        kxx = set(kx) - set(Index)
                        for ky in kxx:
                            if isinstance(self.__SudokuDict[ky],set):
                                orig = self.__SudokuDict[ky].copy()
                                self.__SudokuDict[ky] = self.__SudokuDict[ky] - set(Members[0])
                                if orig != self.__SudokuDict[ky]:
                                    Removed = True
                                if len(self.__SudokuDict[ky]) ==0:
                                    self.__SudokuDict[ky] = 0
    
    def __CountEmptyCell(self):
        k = 0
        for kx in self.__SudokuBoxes:
            for ki in kx:
                if isinstance(self.__SudokuDict[ki],set):
                    k += 1
        return k

    def __SolutionDictToList(self):
        self.__SolutionList = []
        for kx in self.__SudokuGrid:
            for ky in kx:
                self.__SolutionList.append(self.__SudokuDict[ky])
        self.__SolutionGrid = self.__convertToGrid(self.__SolutionList)
    
    def __getSudokuSolution(self):
        if self.__SolutionList is not None:
            return self.__SolutionList
        else:
            return
        
    SudokuSolution = property(fget = __getSudokuSolution)
    
    def __LogicSolve(self):
        N0 = 0
        for kk in range(10):
            self.__FindUniqueValue()
            self.__DoubleValueStrategy()
            self.__EliminateOccupiedValues()
            Nempty = self.__CountEmptyCell()
            if Nempty == N0:
                break
            else:
                N0 = Nempty
        if Nempty == 0:
            return True
        else:
            return False
            
    def __BruteForceSearch(self):
        Odict, Qout = self.__Branch()
        
        for kq in range(len(Qout[1])):
            Iq = Qout[1].pop()
            self.__SudokuDict[Qout[0]] = Iq
            self.__RemoveDuplicates()
            self.__FindUniqueValue()
            self.__DoubleValueStrategy()
            if self.__CountEmptyCell() == 0:
                self.__SolutionDictToList()
                if self.__Metric(self.__SolutionGrid) == 0:
                    return True
                else:
                    self.__SudokuDict = Odict.copy()
            else:
                if not(self.__BruteForceSearch()):
                    self.__SudokuDict = Odict.copy()
                else:
                    return True
        return False
        
    def __Branch(self):
        Original = self.__SudokuDict.copy()
        Q = self.__SudokuDict.iteritems()
        while True:
            try:
                kI = next(Q)
            except StopIteration:
                break
            if isinstance(kI[1],set):
                break
        return Original,kI
    
    def Solve(self, verbose=False):
        if self.CheckMinClue:
            if self.ValidateProblem:
                self.__Singularity()
                self.__ReduceProblemSpace()
                if verbose: print 'Attempting to solve by logic...'
                Nempty = self.__LogicSolve()
                if not Nempty:
                    if verbose: print 'OK, that didn\'t work. Let\'s use Brute Force Search...'
                    Nempty = self.__BruteForceSearch()
                self.__SolutionDictToList()
                
                if Nempty:        
                    if self.__Metric(self.__SolutionGrid) == 0:
                        if verbose: print "Solution Found!"
                        self.Solved = True
                        return True
                    else:
                        if verbose: print "Failed to find solution!"
                        self.Solved = False
                        return False
                else:
                        if verbose: print "Failed to find solution!"
                        self.Solved = False
                        return False
            else:
                if verbose: print "Problem is ill-posed. There are duplicate values."
                return False
        else:
            if verbose: print "Problem does not have the minimum number of clue"
            return False
    
    @property
    def CheckMinClue(self):
        if (81 - self.__ProblemList.count(0)) >= self.MinClue:
            return True
        else:
            return False
                

    def __Metric(self,inGrid):
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
        print "No command line arguments. Using example files %s" %inFN

    if A.CheckOutputFileExists(outFN):
        if A.read_csv(inFN,verbose = True):
            tstart = time.clock()
            A.Solve(verbose = True)
            telapsed = time.clock() - tstart
            print telapsed
            A.write_csv(outFN,verbose = True)
            
