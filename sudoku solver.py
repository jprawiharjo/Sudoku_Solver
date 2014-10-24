# -*- coding: utf-8 -*-
"""
Created on Tue Oct 21 11:50:18 2014

@author: jerry.prawiharjo
"""

import os
import sys

inFN = "Sudoku1.txt"
outFN = "Sudoku1-sol.txt"

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


class Sudoku(object):
    X = 'ABCDEFGHI'
    Y = 'abcdefghi'
    SudokuList = []
    SudokuGrid = []
    ProblemList = []
    SudokuBoxes = []

    def __init__(self):
        self.__makeList()
        self.SudokuGrid = self.__convertToGrid(self.SudokuList)
        self.__makeBoxes()
    
    def __makeList(self):
        self.SudokuList = []
        for ch in self.X:
            self.SudokuList.extend([ch+a for a in self.Y])

    def __makeBoxes(self):
        self.SudokuBoxes = []
        x = ['ABC','DEF','GHI']
        y = ['abc','def','ghi']
        self.SudokuBoxes = []
        for kx in x:
            for ky in y:
                Boxes = []
                for ch in kx:
                    Boxes.extend([ch+a for a in ky])
                self.SudokuBoxes.append(Boxes)
    
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
        self.ProblemList = []
        if os.path.exists(FileName):
            Wf = open(FileName)
            LinesRead = Wf.readlines()
            kcount = 1
            for line in LinesRead:
                TempArray = map(int,line.rstrip('\n').split(','))
                kcount +=1
                if len(TempArray) == 9:
                    self.ProblemList.extend(TempArray)
                else:
                    print "Line %i in the input file has incorrect array length, or does not come in csv format" %kcount
                    return False
            if len(self.ProblemList) == 81: 
                print "Input file successfully parsed"
            else:
                print "Input file has incorrect Sudoku row size"
                return False
            self.__assignDict()
            self.ProblemGrid = self.__convertToGrid(self.ProblemList)
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
        self.ProblemList = []
        Wf = open(FileName,'w')
        for kx in self.SolutionGrid:
            temp = str(kx)
            temp = temp[1:-1]
            Wf.write(temp + '\r\n')
        Wf.close()

    def __assignDict(self):
        self.SudokuDict = {}
        kc = 0
        for kx in self.SudokuList:
            self.SudokuDict[kx] = self.ProblemList[kc]
            kc += 1

    def SingleChoiceStrategy(self):
        replaced = True
        while replaced:
            replaced = False
            for kx in self.X:
                row = []
                for ky in self.Y:
                    row.append(self.SudokuDict[kx+ky])
                if row.count(0) == 1:
                    self.SudokuDict[kx+self.Y[row.index(0)]] = 45-sum(row)
                    replaced = True
    
            for ky in self.Y:
                col = []
                for kx in self.X:
                    col.append(self.SudokuDict[kx+ky])
                if col.count(0) == 1:
                    self.SudokuDict[self.X[col.index(0)]+ky] = 45-sum(col)
                    replaced = True
            
            for kx in self.SudokuBoxes:
                Box = []
                for ki in kx:
                    Box.append(self.SudokuDict[ki])
                if Box.count(0) == 1:
                    self.SudokuDict[kx[Box.index(0)]] = 45-sum(Box)
                    replaced = True
        return

    def EliminationStrategy(self):
        Removed = True
        while Removed:
            Removed = False
            for kx in self.SudokuBoxes:
                Nrange = range(1,10)
                Box = []
                for ki in kx:
                    Box.append(self.SudokuDict[ki])
                if Box.count(0) > 0:
                    for k in Box: 
                        try: 
                            Nrange.remove(k)
                        except:
                            pass
                while Box.count(0) > 0:
                    self.SudokuDict[kx[Box.index(0)]] = Nrange[:]
                    Box[Box.index(0)] = Nrange[:]
    
            for kx in self.SudokuBoxes: 
                for ki in kx:
                    if isinstance(self.SudokuDict[ki],list):
                        if len(self.SudokuDict[ki]) == 1:
                            self.SudokuDict[ki] = self.SudokuDict[ki][0]
                        else:
                            Row = [ki[0]+x for x in self.Y]
                            Row.remove(ki)
                            for kR in Row:
                                if not isinstance(self.SudokuDict[kR],list):
                                    try:
                                        self.SudokuDict[ki].remove(self.SudokuDict[kR])
                                        Removed = True
                                    except:
                                        pass
                            Col = [x+ki[1] for x in self.X]
                            Col.remove(ki)
                            for kR in Col:
                                if not isinstance(self.SudokuDict[kR],list):
                                    try:
                                        self.SudokuDict[ki].remove(self.SudokuDict[kR])
                                        Removed = True
                                    except:
                                        pass
                            if len(self.SudokuDict[ki]) == 1:
                                self.SudokuDict[ki] = self.SudokuDict[ki][0]
            return Removed

    def FindUniqueMember(self):
        Found = True
        #Within the box
        while Found:
            Found = False
            for kx in self.SudokuBoxes:
                BoxNonUniqueList = []
                for ki in kx:
                    if isinstance(self.SudokuDict[ki],list):
                        BoxNonUniqueList.extend(self.SudokuDict[ki])
                    else:
                        BoxNonUniqueList.append(self.SudokuDict[ki])
                BoxUniqueList = list(set(BoxNonUniqueList))
                for kb in BoxUniqueList:
                    if BoxNonUniqueList.count(kb) == 1:
                        for ki in kx:
                            if isinstance(self.SudokuDict[ki],list):
                                if kb in self.SudokuDict[ki]:
                                    self.SudokuDict[ki] = kb
                                    Found = True
        self.RemoveDuplicate()

        Found = True
        #Row-wise                    
        while Found:
            Found = False
            for kx in self.SudokuGrid:
                RowNonUniqueList = []
                for ky in kx:
                    if isinstance(self.SudokuDict[ky],list):
                        RowNonUniqueList.extend(self.SudokuDict[ky])
                RowUniqueList = list(set(RowNonUniqueList))
                for kb in RowUniqueList:
                    if RowNonUniqueList.count(kb) == 1:
                        for ky in kx:
                            if isinstance(self.SudokuDict[ky],list):
                                if kb in self.SudokuDict[ky]:
                                    self.SudokuDict[ky] = kb
                                    Found = True
        self.RemoveDuplicate()

        Found = True
        #Column-wise                    
        while Found:
            Found = False
            for kx in zip(*self.SudokuGrid):
                ColNonUniqueList = []
                for ky in kx:
                    if isinstance(self.SudokuDict[ky],list):
                        ColNonUniqueList.extend(self.SudokuDict[ky])
                ColUniqueList = list(set(ColNonUniqueList))
                for kb in ColUniqueList:
                    if ColNonUniqueList.count(kb) == 1:
                        for ky in kx:
                            if isinstance(self.SudokuDict[ky],list):
                                if kb in self.SudokuDict[ky]:
                                    self.SudokuDict[ky] = kb
                                    Found = True
        self.RemoveDuplicate()

    def Assasination(self):
        for mm in range(0,2):
            for kx in self.SudokuBoxes:
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
                    if isinstance(self.SudokuDict[x],list):
                        x1.extend(self.SudokuDict[x])
                for x in R2:
                    if isinstance(self.SudokuDict[x],list):
                        x2.extend(self.SudokuDict[x])
                for x in R3:
                    if isinstance(self.SudokuDict[x],list):
                        x3.extend(self.SudokuDict[x])
                x1 = set(x1)
                x2 = set(x2)
                x3 = set(x3)
                if len(x1.intersection(x2)) == 0 and len(x2.intersection(x3)) ==0 and len(x1.intersection(x3)) == 0:
                    if mm == 0:
                        CC1= list(set([R1[0][0] + x for x in self.Y]) - set(R1))
                        CC2= list(set([R2[0][0] + x for x in self.Y]) - set(R2))
                        CC3= list(set([R3[0][0] + x for x in self.Y]) - set(R3))
                    else:
                        CC1= list(set([x + R1[0][1] for x in self.X]) - set(R1))
                        CC2= list(set([x + R2[0][1] for x in self.X]) - set(R2))
                        CC3= list(set([x + R3[0][1] for x in self.X]) - set(R3))
                    
                    Z = [[CC1,x1],[CC2,x2],[CC3,x3]]
                    for kz in Z:
                        for kc in kz[0]:
                            if isinstance(self.SudokuDict[kc],list):
                                if len(self.SudokuDict[kc]) > 1:
                                    self.SudokuDict[kc] = list(set(self.SudokuDict[kc]) - kz[1])
                                    self.SudokuDict[kc] = list(self.SudokuDict[kc])
                                if len(self.SudokuDict[kc]) == 1:
                                    self.SudokuDict[kc] = self.SudokuDict[kc][0]
            self.RemoveDuplicate()

    def RemoveDuplicate(self):
        Removed = True
        while Removed:
            Removed = False
            for kx in self.SudokuGrid:
                RowMembers = []
                for ky in kx:
                    if not isinstance(self.SudokuDict[ky],list):
                        RowMembers.append(self.SudokuDict[ky])
                for ky in kx:
                    if isinstance(self.SudokuDict[ky],list):
                        for kR in RowMembers:
                            try:
                                self.SudokuDict[ky].remove(kR)
                                Removed = True
                            except:
                                pass
                        if len(self.SudokuDict[ky]) == 1:
                            self.SudokuDict[ky] = self.SudokuDict[ky][0]
            for kx in zip(*self.SudokuGrid):
                ColMembers = []
                for ky in kx:
                    if not isinstance(self.SudokuDict[ky],list):
                        ColMembers.append(self.SudokuDict[ky])
                for ky in kx:
                    if isinstance(self.SudokuDict[ky],list):
                        for kR in ColMembers:
                            try:
                                self.SudokuDict[ky].remove(kR)
                                Removed = True
                            except:
                                pass
                        if len(self.SudokuDict[ky]) == 1:
                            self.SudokuDict[ky] = self.SudokuDict[ky][0]
            for kx in self.SudokuBoxes:
                BoxMembers = []
                for ki in kx:
                    if not isinstance(self.SudokuDict[ki],list):
                        BoxMembers.append(self.SudokuDict[ki])
                for ki in kx:
                    if isinstance(self.SudokuDict[ki],list):
                        for kb in BoxMembers:
                            try:
                                self.SudokuDict[ki].remove(kb)
                                Removed = True
                            except:
                                pass
                        if len(self.SudokuDict[ki]) == 1:
                            self.SudokuDict[ki] = self.SudokuDict[ki][0]
                        
    def DoubleDragonStrategy(self):
        Removed = True
        while Removed:
            Removed = False

            A = [self.SudokuGrid, zip(*self.SudokuGrid), self.SudokuBoxes]
            for kA in A:
                for kx in kA:
                    Index = []
                    Members = []
                    for ky in kx:
                        if isinstance(self.SudokuDict[ky],list):
                            if len(self.SudokuDict[ky]) == 2:
                                Index.append(ky)
                                Members.append(self.SudokuDict[ky])
                    if len(Index) == 2 and Members[0] == Members[1]:
                        kxx = list(kx[:])
                        for kk in Index:
                            if kk in kxx: kxx.remove(kk)
                        for ky in kxx:
                            if isinstance(self.SudokuDict[ky],list):
                                for kR in set(Members[0]):
                                    if kR in self.SudokuDict[ky]:
                                        self.SudokuDict[ky].remove(kR)
                                        Removed = True


    
    def CountEmptyCell(self):
        k = 0
        for kx in self.SudokuBoxes:
            for ki in kx:
                if isinstance(self.SudokuDict[ki],list):
                    k += 1
        return k

    def __SolutionDictToList(self):
        self.SolutionList = []
        for kx in self.SudokuGrid:
            for ky in kx:
                self.SolutionList.append(self.SudokuDict[ky])
        self.SolutionGrid = self.__convertToGrid(self.SolutionList)
                
    
    def Solve(self):
        self.SingleChoiceStrategy()
        self.EliminationStrategy()
        for kk in range(10):
            self.FindUniqueMember()
            self.DoubleDragonStrategy()
            self.Assasination()
            Nempty = self.CountEmptyCell()
            if Nempty == 0:
                break
            print Nempty
        self.__SolutionDictToList()


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
    
    if A.CheckOutputFile(outFN):
        print "Output will be saved to " + outFN
        if A.read_csv(inFN):
            A.Solve()
    #A.write_csv(outFN)