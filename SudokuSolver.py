from tkinter import *
from tkinter import ttk, StringVar
from tkinter import font as tkFont
import tkinter.messagebox
import os.path
from os import path
from itertools import combinations

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

class InputGrid(object):
    global message_button

    def setMessage(self, messageText):
        self.messageText = messageText
        message_button.delete('1.0', END)
        message_button.insert('1.0', messageText)

    def appendMessage(self, messageText):
        self.messageText = messageText
        message_button.insert('end', messageText)
        message_button.yview(END)

    # This function will make specific letter in the string bold or of colour
    # if full-partial-flag is set to 'F', then it is marked in Blue and if it is 'P it is marked as red
    # red numbers are the candidates to be removed.
    def markBold(self, full_partial_flag, matchText, cand_text, row, column, gridlist):

        self.cand_text = cand_text
        self.matchText = matchText
        self.full_partial_flag = full_partial_flag
        self.row = row
        self.column = column
        gridlist[row][column].delete('1.0', END)
        for letterItem in list(cand_text):
            if letterItem in set(list(matchText)):
                if full_partial_flag == 'F':
                    gridlist[row][column].tag_configure('Blue', foreground='Blue', font=helv10B)
                    gridlist[row][column].insert('end', letterItem, 'Blue')
                else:
                    gridlist[row][column].tag_configure('Blue', foreground='Red', font=helv10B)
                    gridlist[row][column].insert('end', letterItem, 'Blue')
            else:
                gridlist[row][column].tag_configure('Black', foreground='Black', font=helv08)
                gridlist[row][column].insert('end', letterItem, 'Black')

        return


    def blankGrid(self):    # This is called on button FILL
        global gridlist, textEntry, gridValue, sudokuStatus, solve_button, message_button
        if sudokuStatus == '':
            sudokuStatus = 'Fill'
        else:
            response = tkinter.messagebox.askquestion("Question", "Are you sure you want to start again")
            if response == 'yes':
                sudokuStatus = ''
            else:
                return
        for row in range(9):
            for column in range(9):
                gridValue[row][column] = ' '
                gridlist[row][column].delete('1.0', END)
                gridlist[row][column].configure(bg=self.markCellColour(False, row, column),fg='Blue', font=helv15)

        gridlist[0][0].focus()
        solve_button.config(state=ACTIVE)
        hints_button.config(state=ACTIVE)
        return

# This marks any cell as error
    def markCellColour(self, errorFlag, i, j):
        self.errorFlag = errorFlag
        self.i = i
        self.j = j

        if errorFlag:
            boxcolour = 'Red'
        else:
            tobecoloured = (i in (0, 1, 2, 6, 7, 8) and j in (0, 1, 2, 6, 7, 8)) or (
                                    i in (3, 4, 5) and j in (3, 4, 5))
            if tobecoloured:
                boxcolour = 'Yellow'
            else:
                boxcolour = "White"

        return boxcolour

# This function will make a list of cells to be checked for duplicates in row, column and box
    def findRangeToBeChecked(self, row_column_box, include_cell, rownum, colnum):
        self.row_column_box = row_column_box    # this will have value of A for all, R for Row, C for Column, B for Box
        self.rownum = rownum
        self.colnum = colnum
        self.include_cell = include_cell        # 'Y will indicate the cell in parameters should be included else no.

        rangeList = []

        if row_column_box in ('A', 'R'):
            for column in range(9):
                if column != colnum or include_cell == 'Y':
                    rangeList.append([rownum, column])

        if row_column_box in ('A', 'C'):
            for row in range(9):
                if row != rownum or include_cell == 'Y':
                    rangeList.append([row, colnum])

        if row_column_box in ('A', 'B'):
            for m in range(3):
                for n in range(3):
                    if ((int(rownum / 3) * 3 + m != rownum) or (
                            int(colnum / 3) * 3 + n != colnum)) or include_cell == 'Y':
                        rangeList.append([int(rownum / 3) * 3 + m, int(colnum / 3) * 3 + n])

        return rangeList

# This function checks if the item is duplicate of any other cell in given range
    def checkDup(self, errorFlag, i, j):
        global cellRange, message_button
        self.i = i
        self.j = j
        self.errorFlag = errorFlag

        for m in range(len(cellRange)):
            if gridValue[i][j] != ' ' and gridValue[i][j] == gridValue[cellRange[m][0]][cellRange[m][1]]:
                gridlist[i][j].config(bg=self.markCellColour(errorFlag, i, j))
                errorFlag = True
        return errorFlag

    def checkGrid(self):        # This is first step in Hints or in Start
        global gridlist, textEntry, boxcolour, cellRange, sudokuStatus, message_button, gridValue
        print(gridValue)

        for row in range(9):
            for column in range(9):
                gridValue[row][column] = gridlist[row][column].get('1.0', END)
                gridValue[row][column] = gridValue[row][column][ :-1]

        # First check for having only numbers 1 to 9. Colour the grid in red to indicate errors and give message
        errorAny = False
        for row in range(9):
            for column in range(9):
                if gridValue[row][column] in ('1', '2', '3', '4', '5', '6', '7', '8', '9', ' ', ''):
                    errorFlag = False
                    if gridValue[row][column] == '':
                        gridValue[row][column] = ' '
                    else:
                        pass
                else:
                    errorFlag = True
                    errorAny = True

                gridlist[row][column].config(bg=self.markCellColour(errorFlag, row, column))
        if errorAny:
            self.setMessage("Enter only numbers 1 to 9 or blanks")
            return

        # check for duplicate values in rows, columns and the box
        errorAny = False
        for row in range(9):
            for column in range(9):
                cellRange = self.findRangeToBeChecked('A', 'N', row, column)
                if self.checkDup(errorAny, row, column):
                    errorAny = True

        if errorAny:
            self.setMessage("Please remove duplicates in rows, columns and boxes")
            return
        else:
            self.setMessage("All entries are correct. If you want start solving click Start")
        return errorAny

    # This gets list of unique numbers in the selected row/column/box among the candidates
    def findUniqueNums(self, cellRange, candidates):
        self.candidates = candidates
        self.cellRange = cellRange
        uniqueNums = ''

        for i in range(9):
            x = cellRange[i][0]
            y = cellRange[i][1]

            for elements in list(candidates[x][y]):
                if elements not in uniqueNums:
                    uniqueNums += str(elements)

        return sorted(uniqueNums)

    # This fills the ComboList dictionary with details of where each combination of numbers
    # occurs in the grid and how many of them in the grid
    def fillCombolist(self, size, cellRange, row_column_box, comboList,
                              candidates):
        self.size = size
        self.cellRange = cellRange
        self.row_column_box = row_column_box
        self.comboList = comboList
        self.candidates = candidates

        for comboNum in list(comboList):
            comboNumSet = set(comboNum)
            subset_count = 0
            superset_count = 0
            some_common_Letters_Count = 0
            elem_index = 0
            for i in range(9):
                x = cellRange[i][0]
                y = cellRange[i][1]
                candidatesSet = set(candidates[x][y])
                if len(candidatesSet) > 0:
                    intersection_set = candidatesSet.intersection(comboNumSet)
                    match_flag = 'None'
                    if len(intersection_set) > 0:  # meaning there are some common numbers
                        match_flag = 'Some'
                        some_common_Letters_Count += 1
                    if comboNumSet.issubset(candidatesSet):
                        match_fag = 'SuperSet'
                        superset_count += 1
                    if candidatesSet.issubset(comboNumSet):
                        match_flag = 'Subset'
                        subset_count += 1
                    if match_flag != 'None':
                        comboList[comboNum][3].append([])
                        comboList[comboNum][3][elem_index] = \
                                [match_flag, x, y, row_column_box]
                        elem_index += 1

            comboList[comboNum][0] = subset_count
            comboList[comboNum][1] = some_common_Letters_Count
            comboList[comboNum][2] = superset_count

        return comboList

    # Returns array of all possible combination of unique numbers in pairs, triplets, quads
    def getCombolist(self, size, uniqueNums):
        self.size = size
        self.uniqueNums = uniqueNums
        comboNum = [0] * size
        comboList = {}

        comb = combinations(uniqueNums, size)
        for unique_comb in comb:
            comboNum = ''
            for numbers in unique_comb:
                comboNum += numbers
            comboList[comboNum] = [0, 0, 0, []]
        return comboList

    # Get description for the type of tuples found
    def get_desc_foundtype(self, size):
        self.size = size
        foundType = 'Singles'
        if size == 2:
            foundType = 'Pairs'
        elif size == 3:
            foundType = "Triplets"
        elif size == 4:
            foundType = 'Foursome'
        else:
            foundType = 'Fivesome'
        return foundType

    # Get the next row, column or box. First complete all rows, then columns, then boxes
    def get_next_rcb(self, row, column, row_column_box_flag):
        self.row = row
        self.column = column
        self.row_column_box_flag = row_column_box_flag

        rcb_complete_flag = False
        if row_column_box_flag == 'R':
            if row <= 7:
                row += 1
            else:
                row_column_box_flag = 'C'
                row = 0
                column = 0

        elif row_column_box_flag == 'C':

            if column <= 7:
                column += 1
            else:
                row_column_box_flag = 'B'
                row = 0
                column = 0

        else:
            if row <= 3:
                if column <= 3:
                    column += 3
                else:
                    row += 3
                    column = 0
            else:
                if column <= 3:
                    column += 3
                else:
                    rcb_complete_flag = True

        return row, column, row_column_box_flag, rcb_complete_flag

    # Process combo numbers for tuples and blocking numbers
    def findCombos(self, candidates, actionList):
        self.candidates = candidates
        self.actionList = actionList
        comboList = {}
        foundFlag = False
        size = 2
        # Process combo numbers from sizes to 2 to 5 across all rows/cols/boxes
        while (size <= 5) and (not foundFlag):
            rcb_complete = False
            foundFlag = False
            row = 0
            column = 0
            row_column_box_flag = 'R'

            while not (foundFlag or rcb_complete):

                cellRange = self.findRangeToBeChecked(row_column_box_flag, 'Y', row, column)
                uniqueNums = self.findUniqueNums(cellRange, candidates)

                if len(uniqueNums) > size:  # Dont waste time in looking for combos if the number of
                    # missing items is less than size
                    comboList = self.getCombolist(size, uniqueNums)
                    comboList = self.fillCombolist(size, cellRange, row_column_box_flag,
                                            comboList, candidates)
                    for elem in comboList:
                        if (comboList[elem][0] == size) and (comboList[elem][1] > size):

                            foundFlag = True
                            foundType = self.get_desc_foundtype(size)

                            # note the coordinates of first cell
                            x = comboList[elem][3][0][1]
                            y = comboList[elem][3][0][2]
                            rcb_flag = comboList[elem][3][0][3]

                            self.appendMessage("Hidden " + foundType + ' of numbers ' +
                                               elem + ' in ' + rcb_flag + '...Next\n')

                            actionList.append([elem, x, y, row_column_box_flag])

                            for i in range(len(comboList[elem][3])):
                                if (comboList[elem][3][i][0] == 'Subset'):
                                    full_partial_flag = 'F'
                                elif (comboList[elem][3][i][0] == 'Some'):
                                    full_partial_flag = 'P'
                                else:
                                    full_partial_flag = ''
                                if full_partial_flag != '':
                                    x = comboList[elem][3][i][1]
                                    y = comboList[elem][3][i][2]
                                    rcb_flag = comboList[elem][3][i][3]
                                    self.markBold(full_partial_flag, elem, candidates[x][y], x, y, gridlist)
                                    if full_partial_flag == 'F':
                                        gridlist[x][y].configure(bg='Pink', font=helv10B)

                row, column, row_column_box_flag, rcb_complete = \
                    self.get_next_rcb(row, column, row_column_box_flag)
            size += 1

        return foundFlag

    # checks if the coordinates supplied fall within a row or column of box
    def check_coords_within_box(self, size, rcb_flag, x1, x2, y1, y2, x3, y3):
        self.size = size
        self.rcb_flag = rcb_flag
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.x3 = x3
        self.y3 = y3

        n1, n2, n3 = 0, 0, 0
        match_flag = False
        if rcb_flag == 'R':
            n1 = y1
            n2 = y2
            n3 = y3
        elif rcb_flag == 'C':
            n1 = x1
            n2 = x2
            n3 = x3

        if rcb_flag in ('R', 'C'):
            if size == 2:
                if n2 == (n1 + 1):
                    if n1 in (0, 1, 3, 4, 6, 7):
                        match_flag = True
            else:
                if n1 in (0, 3, 6):
                    if n2 == (n1 + 1):
                        if n3 == (n2 + 1):
                            match_flag = True
        else:
            if size == 2:
                if x1 == x2:
                    if y2 == (y1 + 1):
                        if y1 in (0, 1, 3, 4, 6, 7):
                            match_flag = True
                else:
                    if y1 == y2:
                        if x2 == (x1 + 1):
                            if x1 in (0, 1, 3, 4, 6, 7):
                                match_flag = True
            else:
                if (x1 == x2) and (x2 == x3):
                    if y1 in (0, 3, 6):
                        if y2 == (y1 + 1):
                            if y3 == (y2 + 1):
                                match_flag = True
                elif (y1 == y2) and (y2 == y3):
                    if x1 in (0, 3, 6):
                        if x2 == (x1 + 1):
                            if x3 == (x2 + 1):
                                match_flag = True

        return match_flag
    # Check for presence in the row/column/box for pointing numbers
    def check_pointing_presence(self, elem, rcb_flag,x1, x2, y1, y2, x3, y3):
        self.elem = elem
        self.rcb_flag = rcb_flag
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.x3 = x3
        self.y3 = y3
        row = 0
        col = 0
        actionList = []
        pointing_flag = ''
        action_index = 0
        # need to set initial coordinates for checking of row/col/box
        if rcb_flag in ('R', 'C'): # need to search in the box
            if x1 % 3 > 0:
                row = x1 - (x1 % 3)
            else:
                row = x1
            if y1 % 3 > 0:
                col = y1 - (y1 % 3)
            else:
                col = y1
            pointing_flag = 'B'

        else:
            if x1 == x2:    # meaning pointing numbers occur at column
                row = x1
                col = 0
                pointing_flag = 'R'
            elif y1 == y2:  # meaning pointing numbers occur in row
                row = 0
                col = y1
                pointing_flag = 'C'
            else:
                print("Something wrong in pointing numbers! + "
                      f"rcb_flag,: {x1}{y1}{x2}{y2}{x3}{y3}")

        for i in range(9):
            if not ((row in (x1, x2, x3)) and (col in (y1, y2, y3))):
                candidatesSet = set(candidates[row][col])
                if set(elem).issubset(candidatesSet):
                    actionList.append([elem, row, col, pointing_flag])
            if pointing_flag == 'R':
                col += 1
            elif pointing_flag == 'C':
                row += 1
            else:
                if col in (2,5,8):
                    row += 1
                    col = col - 2
                else:
                    col += 1

        return actionList

    # find Blockers or Pointing Numbers in rows/columns/boxes
    def findPointers(self, candidates):
        global unmark_cellrange
        self.candidates = candidates
        actionList = []
        comboList = {}

        rcb_complete = False
        foundFlag = False
        row = 0
        column = 0
        row_column_box_flag = 'R'

        while not (foundFlag or rcb_complete):

            cellRange = self.findRangeToBeChecked(row_column_box_flag, 'Y', row, column)
            uniqueNums = self.findUniqueNums(cellRange, candidates)

            if len(uniqueNums) >= 2:  # Dont waste time in looking for pointers if the number of
                # missing items is less than size

                comboList = self.getCombolist(1, uniqueNums)
                comboList = self.fillCombolist(1, cellRange, row_column_box_flag,
                                               comboList, candidates)

                for elem in comboList:
                    subset_count = comboList[elem][0]
                    some_common_Letters_Count = comboList[elem][1]
                    superset_count = comboList[elem][2]

                    if (superset_count in (2,3)):    # if occurs 2 or 3 times in r/c/b

                        x1 = comboList[elem][3][0][1]
                        y1 = comboList[elem][3][0][2]
                        rcb_flag = comboList[elem][3][0][3]

                        x2 = comboList[elem][3][1][1]
                        y2 = comboList[elem][3][1][2]

                        if superset_count == 3:
                            x3 = comboList[elem][3][2][1]
                            y3 = comboList[elem][3][2][2]

                        else:
                            x3 = -1
                            y3 = -1

                        # now check that these x,y, occur within a box range for rows/columns
                        if self.check_coords_within_box(superset_count, rcb_flag,
                                                        x1, x2, y1, y2, x3, y3):
                            # now check if the same numbers are present in corresponding r/c/b
                            actionList = self.check_pointing_presence(elem, rcb_flag,
                                                                     x1, x2, y1, y2, x3, y3)
                            if len(actionList) > 0:
                                foundFlag = True
                                # note the coordinates of first cell
                                rcb_flag = comboList[elem][3][0][3]

                                unmark_cellrange = []
                                unmark_cellrange.append([x1, y1])
                                unmark_cellrange.append([x2, y2])
                                if superset_count == 3:
                                    unmark_cellrange.append([x3, y3])

                                self.markBold('F', elem, candidates[x1][y1], x1, y1, gridlist)
                                gridlist[x1][y1].configure(bg='Pink', font=helv10B)
                                self.markBold('F', elem, candidates[x2][y2], x2, y2, gridlist)
                                gridlist[x2][y2].configure(bg='Pink', font=helv10B)
                                if x3 > 0:
                                    self.markBold('F', elem, candidates[x3][y3], x3, y3, gridlist)
                                    gridlist[x3][y3].configure(bg='Pink', font=helv10B)

                                for i in range(len(actionList)):
                                    x = actionList[i][1]
                                    y = actionList[i][2]
                                    self.markBold('P', elem, candidates[x][y], x, y, gridlist)
                    if foundFlag:
                        break
            row, column, row_column_box_flag, rcb_complete = \
                self.get_next_rcb(row, column, row_column_box_flag)

        return actionList

    # Replaces in the candidates array, all the numbers that are part of combonum
    # in the array of findRangeToBeChecked.
    def replaceAcross(self, comboNum, cellRange, candidates, unmark_cellrange):
        self.comboNum = comboNum
        self.cellRange = cellRange
        self.candidates = candidates
        self.unmark_cellrange = unmark_cellrange

        for i in range(len(cellRange)):
            x = cellRange[i][0]
            y = cellRange[i][1]
            candidatesItem = candidates[x][y]

            if len(candidatesItem) >= 2:

                if not set(str(candidatesItem)).issubset(set(str(comboNum))):
                    newSet = sorted(set(str(candidatesItem)) - set(str(comboNum)))
                    candidates[x][y] = ''.join(list(newSet))

                    gridlist[x][y].delete('1.0', END)
                    gridlist[x][y].insert('1.0', candidates[x][y])
                    gridlist[x][y].configure(bg=self.markCellColour(False, x, y), fg='Blue',
                                                wrap=CHAR, padx=5, font=helv08)
                else:
                    gridlist[x][y].delete('1.0', END)
                    gridlist[x][y].insert('1.0', candidates[x][y])
                    gridlist[x][y].configure(bg=self.markCellColour(False, x, y), fg='Blue',
                                             wrap=CHAR, padx=5, font=helv08)

        for i in range(len(unmark_cellrange)):
            x = unmark_cellrange[i][0]
            y = unmark_cellrange[i][1]
            gridlist[x][y].delete('1.0', END)
            gridlist[x][y].insert('1.0', candidates[x][y])
            gridlist[x][y].configure(bg=self.markCellColour(False, x, y), fg='Blue',
                                     wrap=CHAR, padx=5, font=helv08)

        return
    # Finds X Wing among the candidates
    def find_x_wing(self, candidates):
        global actionList, unmark_cellrange
        self.candidates = candidates

        row = 0
        column = 0
        rc_flag = 'R'
        foundFlag = False
        rc_complete_flag = False
        x_wing_number = ''
        elem = ''
        unmark_cellrange = []
        actionList = []
        while not(foundFlag or rc_complete_flag):
            cellRange = self.findRangeToBeChecked(rc_flag, 'Y', row, column)
            uniqueNums = self.findUniqueNums(cellRange, candidates)

            if len(uniqueNums) >= 2:  # Dont waste time in looking for pointers if the number of
                # missing items is less than size

                comboList = self.getCombolist(1, uniqueNums)
                comboList = self.fillCombolist(1, cellRange, rc_flag, comboList, candidates)

                for elem in comboList:

                    subset_count = comboList[elem][0]
                    some_common_Letters_Count = comboList[elem][1]
                    superset_count = comboList[elem][2]

                    if superset_count == 2:    # if occurs twice in row or column

                        x11 = comboList[elem][3][0][1]      # these are coordinates of top of X Wing
                        y11 = comboList[elem][3][0][2]
                        x12 = comboList[elem][3][1][1]
                        y12 = comboList[elem][3][1][2]

                        x1y1 = x11*10+y11
                        x1y2 = x12*10+y12

                        # now check for other rows/columns for the same number occurring in X Wing
                        if rc_flag == 'R':
                            start_rc = row
                        else:
                            start_rc = column

                        for i in range(start_rc+1, 9):  # check for occurrence of same numbers in next rows/columns
                            if rc_flag == 'R':
                                row2 = i
                                column2 = 0
                            else:
                                column2 = i
                                row2 = 0

                            cellRange2 = self.findRangeToBeChecked(rc_flag, 'Y', row2, column2)
                            uniqueNums2 = self.findUniqueNums(cellRange, candidates)

                            if elem in uniqueNums2:  # if the elem found is present in this row or column
                                comboList2 = self.getCombolist(1, uniqueNums2)
                                comboList2 = self.fillCombolist(1, cellRange2, rc_flag, comboList2, candidates)

                                subset_count2 = comboList2[elem][0]
                                some_common_Letters_Count2 = comboList2[elem][1]
                                superset_count2 = comboList2[elem][2]

                                if superset_count2 == 2:                 # there are exactly two occurrences in this r/c
                                    x21 = comboList2[elem][3][0][1]      # the bottom side of X Wing
                                    y21 = comboList2[elem][3][0][2]
                                    x22 = comboList2[elem][3][1][1]
                                    y22 = comboList2[elem][3][1][2]

                                    if (rc_flag == 'R' and y11 == y21 and y12 == y22) \
                                            or (rc_flag == 'C' and x11 == x21 and x12 == x22):

                                        unmark_cellrange = []
                                        unmark_cellrange.append([x11, y11])
                                        unmark_cellrange.append([x12, y12])
                                        unmark_cellrange.append([x21, y21])
                                        unmark_cellrange.append([x22, y22])
                                        x_wing_number = elem

                                        self.replaceAcross(x_wing_number, [], candidates, unmark_cellrange)

                                        # Now we have to check if there are numbers to be removed in those r/c

                                        if rc_flag == 'R':
                                            cellRange1 = self.findRangeToBeChecked('C', 'Y', 0, y11)
                                            cellRange2 = self.findRangeToBeChecked('C', 'Y', 0, y12)
                                        else:
                                            cellRange1 = self.findRangeToBeChecked('R', 'Y', x11, 0)
                                            cellRange2 = self.findRangeToBeChecked('R', 'Y', x12, 0)
                                        actionList = []

                                        for i in range(9):
                                            x1 = cellRange1[i][0]
                                            y1 = cellRange1[i][1]
                                            x2 = cellRange2[i][0]
                                            y2 = cellRange2[i][1]

                                            if not (((rc_flag == 'R') and (x1 == x11 or x1 == x21)) or
                                                    (rc_flag == 'C' and (y1 == y11 or y1 == y21))):
                                                candidatesSet = set(candidates[x1][y1])
                                                if set(x_wing_number).issubset(candidatesSet):
                                                    actionList.append([x_wing_number, x1, y1, rc_flag])

                                            if not (((rc_flag == 'R') and (x2 == x12 or x2 == x22)) or
                                                    (rc_flag == 'C' and (y2 == y12 or y2 == y22))):
                                                candidatesSet = set(candidates[x2][y2])
                                                if set(x_wing_number).issubset(candidatesSet):
                                                    actionList.append([x_wing_number, x2, y2, rc_flag])

                                        if len(actionList) > 0:
                                            foundFlag = True
                                            break


            if rc_flag == 'R':
                if row == 8:
                    rc_flag = 'C'
                    column = 0
                    row = 0
                else:
                    row += 1
            else:
                if column == 8:
                    rc_complete_flag = True
                else:
                    column += 1

        if foundFlag:   # mark the cells as pink and numbers in bold
            for item_index in range(len(unmark_cellrange)):
                x = unmark_cellrange[item_index][0]
                y = unmark_cellrange[item_index][1]

                self.markBold('F',x_wing_number, candidates[x][y], x, y, gridlist)
                gridlist[x][y].configure(bg='Pink')
            for item_index in range(len(actionList)):
                x = actionList[item_index][1]
                y = actionList[item_index][2]

                self.markBold('P', x_wing_number, candidates[x][y], x, y, gridlist)

        return x_wing_number, unmark_cellrange, actionList

    # Check if the set of 3 cells are inside a box
    def check_if_in_box_or_row_column(self, x1, y1, x2, y2, x3, y3):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.x3 = x3
        self.y3 = y3

        check_flag = False
        if ((int(x1/3) == int(x2/3) and int(x2/3) == int(x3/3)) and
            (int(y1/3) == int(y2/3) and int(y2/3) == int(y3/3))):
            check_flag = True

        if ((x1 == x2 and x2 == x3) or (y1 == y2 and y2 == y3)):
            check_flag = True
        return check_flag

    # returns the cell range pointed to by XY wing cells
    def get_cell_range_for_xy_wing(self, xyz_flag, x1, y1, x2, y2, x3, y3):
        self.xyz_flag = xyz_flag
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.x3 = x3
        self.y3 = y3
        cellRange = []

        if (x1 == x2 and int(x3 / 3) == int(x1 / 3)):
            # cells are (x1, y1/3), (x1, y1/3+1), (x2, y1/3+2) except for (x1, y1)
            # cells are (x3, y2/3), (x3, y2/3+1), (x3, y2/3+2)

            cellRange.append([x1, int(y1 / 3) * 3])
            cellRange.append([x1, int(y1 / 3) * 3 + 1])
            cellRange.append([x1, int(y1 / 3) * 3 + 2])
            if not xyz_flag:
                cellRange.append([x3, int(y2 / 3) * 3])
                cellRange.append([x3, int(y2 / 3) * 3 + 1])
                cellRange.append([x3, int(y2 / 3) * 3 + 2])

        elif (x1 == x3 and int(x2 / 3) == int(x1 / 3)):
            cellRange.append([x1, int(y1 / 3) * 3])
            cellRange.append([x1, int(y1 / 3) * 3 + 1])
            cellRange.append([x1, int(y1 / 3) * 3 + 2])
            if not xyz_flag:
                cellRange.append([x2, int(y3 / 3) * 3])
                cellRange.append([x2, int(y3 / 3) * 3 + 1])
                cellRange.append([x2, int(y3 / 3) * 3 + 2])

        elif (y1 == y2 and int(y3 / 3) == int(y1 / 3)):
            # cells are (x1/3, y1), (x1/3+1, y1), (x1/3+2. y1) except (x1, y1)
            # cells are (x2/3, y3), (x2/3+1, y3), (x2/3+2, y3)
            cellRange.append([int(x1 / 3) * 3, y1])
            cellRange.append([int(x1 / 3) * 3 + 1, y1])
            cellRange.append([int(x1 / 3) * 3 + 2, y1])
            if not xyz_flag:
                cellRange.append([int(x2 / 3) * 3, y3])
                cellRange.append([int(x2 / 3) * 3 + 1, y3])
                cellRange.append([int(x2 / 3) * 3 + 2, y3])

        elif (y1 == y3 and int(y2 / 3) == int(y1 / 3)):
            # cells are (x1/3, y1), (x1/3+1, y1), (x1/3+2. y1) except (x1, y1)
            # cells are (x3/3, y2), (x3/3+1, y2), (x3/3+2, y2)
            cellRange.append([int(x1 / 3) * 3, y1])
            cellRange.append([int(x1 / 3) * 3 + 1, y1])
            cellRange.append([int(x1 / 3) * 3 + 2, y1])
            if not xyz_flag:
                cellRange.append([int(x3 / 3) * 3, y2])
                cellRange.append([int(x3 / 3) * 3 + 1, y2])
                cellRange.append([int(x3 / 3) * 3 + 2, y2])

        elif (x1 == x2 and y1 == y3):
            # there is only one cell (x3, y2)
            cellRange.append([x3, y2])
        elif (x1 == x3 and y1 == y2):
            # there is only one cell (x2, y3)
            cellRange.append([x2, y3])

        # Now remove (x1, y1) from cellrange
        range_length = len(cellRange)
        cinx = 0
        while cinx < range_length:
            if (x1 == cellRange[cinx][0]) and (y1 == cellRange[cinx][1]):
                cellRange.pop(cinx)
                range_length -= 1
            else:
                cinx += 1

        return cellRange

    # checks if candidate in specific cell at x, y is a XY-Wing
    def check_for_xy_wing_for_cell(self, xyz_flag, candidates, xy_cell_x, xy_cell_y):
        global actionList, unmark_cellrange
        self.xyz_flag = xyz_flag
        self.candidates = candidates
        self.xy_cell_x = xy_cell_x
        self.xy_cell_y = xy_cell_x

        foundFlag = False
        xy_wing_number = ''
        xy_value = candidates[xy_cell_x][xy_cell_y]
        if len(xy_value) == 2:
            x1_value = list(xy_value)[0]
            y1_value = list(xy_value)[1]
            cellRange = self.findRangeToBeChecked('A', 'N', xy_cell_x, xy_cell_y)

            for inx in range(len(cellRange)):
                cell_x1 = cellRange[inx][0]
                cell_y1 = cellRange[inx][1]
                cell_value = candidates[cell_x1][cell_y1]
                if len(cell_value) == 2 and cell_value != xy_value:
                    xz_value = ''
                    yz_value = ''
                    found_xz = False
                    found_yz = False
                    if x1_value in set(cell_value):
                        x2_value = x1_value
                        z2_value = cell_value.replace(x2_value, '')
                        xz_value = cell_value
                        found_xz = True

                        if y1_value < z2_value:
                            yz_value = y1_value + z2_value
                        else:
                            yz_value = z2_value + y1_value

                    if y1_value in set(cell_value):
                        y2_value = y1_value
                        z2_value = cell_value.replace(y2_value, '')
                        yz_value = cell_value
                        found_yz = True

                        if x1_value < z2_value:
                            xz_value = x1_value + z2_value
                        else:
                            xz_value = z2_value + x1_value

                        if xz_value != '' or yz_value != '':
                            # now that there is match for one wing, look  for match for 2nd wing
                            for inx2 in range(len(cellRange)):
                                cell_x2 = cellRange[inx2][0]
                                cell_y2 = cellRange[inx2][1]
                                cell_value = candidates[cell_x2][cell_y2]
                                if (found_yz and cell_value == xz_value) or \
                                        (found_xz and cell_value == yz_value):
                                    # these 3 should not be from the same box
                                    if not self.check_if_in_box_or_row_column(xy_cell_x, xy_cell_y,
                                                                              cell_x1, cell_y1, cell_x2, cell_y2):
                                        # now we need to check if there are cells pointing to XY wing
                                        xy_wing_number = z2_value
                                        xy_cellRange = self.get_cell_range_for_xy_wing(xyz_flag, xy_cell_x, xy_cell_y,
                                                                                       cell_x1, cell_y1, cell_x2,
                                                                                       cell_y2)

                                        actionList = []
                                        for cinx in range(len(xy_cellRange)):
                                            x_coord = xy_cellRange[cinx][0]
                                            y_coord = xy_cellRange[cinx][1]
                                            if xy_wing_number in set(candidates[x_coord][y_coord]):
                                                unmark_cellrange = []
                                                unmark_cellrange.append([xy_cell_x, xy_cell_y])
                                                unmark_cellrange.append([cell_x1, cell_y1])
                                                unmark_cellrange.append([cell_x2, cell_y2])
                                                foundFlag = True
                                                actionList.append([xy_wing_number, x_coord, y_coord, ''])
        return xy_wing_number, foundFlag

    # Finds XY Wing among the candidates
    def find_xy_wing(self, candidates):
        global actionList, unmark_cellrange
        self.candidates = candidates

        xy_cell_x = 0
        xy_cell_y = 0
        foundFlag = False
        complete_flag = False
        xy_wing_number = ''

        unmark_cellrange = []
        actionList = []
        xyz_flag = False
        while not(foundFlag or complete_flag):
            xy_wing_number, foundFlag = self.check_for_xy_wing_for_cell(xyz_flag, candidates, xy_cell_x, xy_cell_y)

            if xy_cell_y == 8:
                xy_cell_x += 1
                if xy_cell_x == 9:
                    complete_flag = True
                else:
                    xy_cell_y = 0
            else:
                xy_cell_y += 1

        if foundFlag:  # mark the cells as pink and numbers in bold
            for item_index in range(len(unmark_cellrange)):
                x = unmark_cellrange[item_index][0]
                y = unmark_cellrange[item_index][1]

                self.markBold('F', xy_wing_number, candidates[x][y], x, y, gridlist)
                gridlist[x][y].configure(bg='Pink')

            for item_index in range(len(actionList)):
                x = actionList[item_index][1]
                y = actionList[item_index][2]

                self.markBold('P', xy_wing_number, candidates[x][y], x, y, gridlist)

        return xy_wing_number, unmark_cellrange, actionList

    # Finds XYZ Wing among the candidates
    def find_xyz_wing(self, candidates):
        global actionList, unmark_cellrange
        self.candidates = candidates

        xyz_cell_x = 0
        xyz_cell_y = 0
        foundFlag = False
        complete_flag = False
        xyz_wing_number = ''

        unmark_cellrange = []
        actionList = []
        xyz_flag = True
        while not (foundFlag or complete_flag):
            cell_value = candidates[xyz_cell_x][xyz_cell_y]

            if len(cell_value) == 3:
                inx = 0
                while not(foundFlag or inx > 2):
                    number_removed = cell_value[inx]
                    candidates[xyz_cell_x][xyz_cell_y] = cell_value.replace(number_removed, '')
                    # Now check for the xy Wing with one number removed
                    xyz_wing_number, foundFlag = self.check_for_xy_wing_for_cell(xyz_flag, candidates,
                                                                                 xyz_cell_x, xyz_cell_y)

                    candidates[xyz_cell_x][xyz_cell_y] = cell_value
                    if foundFlag and xyz_wing_number == number_removed:
                        foundFlag = True
                    else:
                        foundFlag = False
                    inx += 1

            if xyz_cell_y == 8:
                xyz_cell_x += 1
                if xyz_cell_x == 9:
                    complete_flag = True
                else:
                    xyz_cell_y = 0
            else:
                xyz_cell_y += 1

        if foundFlag:  # mark the cells as pink and numbers in bold
            for item_index in range(len(unmark_cellrange)):
                x = unmark_cellrange[item_index][0]
                y = unmark_cellrange[item_index][1]

                self.markBold('F', xyz_wing_number, candidates[x][y], x, y, gridlist)
                gridlist[x][y].configure(bg='Pink')

            for item_index in range(len(actionList)):
                x = actionList[item_index][1]
                y = actionList[item_index][2]

                self.markBold('P', xyz_wing_number, candidates[x][y], x, y, gridlist)

        return xyz_wing_number, unmark_cellrange, actionList

    # Action on pressing Next button
    def nextButtonAction(self):
        global fillinStep   # value 0 - we have to generate candidates,
                            # value 1 - we have to find naked singles,
                            # value 2 - we have to replace singles
                            # value 3 - we have to find single occurences
                            # value 4 - we have to replace single occurences
                            # value 5 - we have to find pairs, etc
                            # value 6 - we have to remove 'pair values from candidates
                            # value 7 - we have to find pointing numbers
                            # value 8 - we have to remove pointing numbers from candidates
                            # value 9 - We have to find X Wing
                            # Value 10 -We have to remove the X-wing candidates
                            # value 11 -We have to find XY Wing
                            # Value 12 -We have to remove the XY-wing candidates
                            # value 13 -We have to find XYZ Wing
                            # Value 14 -We have to remove the XYZ-wing candidates
                            # Value 98 - Nothing more can be done
                            # Value 99 - Puzzle complete
        global candidates, gridlist, gridValue, next_button, comboList, actionList
        global unmark_cellrange, hilight_button

        wait_for_next_button = False
        while not wait_for_next_button:

            if fillinStep == 0:  # Meaning we first have to fill in candidates and then look for solving steps
                # First generate candidates for all missing cells
                candidates = self.generateCandidates(gridValue)

                if self.checkCompletion(candidates):
                    self.appendMessage("Puzzle Completed. Congrats. Start Another Puzzle")
                    next_button.configure(state=DISABLED)
                    wait_for_next_button = True
                    fillinStep = 99
                else:
                    self.appendMessage("Generated candidates... Next\n")
                    wait_for_next_button = True
                    fillinStep = 1     # Status changed to 2 so that next time it will look to find naked singles
            
            elif fillinStep == 1:   # find naked singles 

                if self.findNakedSingles(gridValue, candidates): # fillinStep will be changed to 2 if success in naked singles

                    fillinStep = 2
                    wait_for_next_button = True
                    hilight_button.configure(state=DISABLED)
                else:
                    hilight_button.configure(state=ACTIVE)
                    fillinStep = 3
                    
            elif fillinStep == 2:   # replace naked singles

                self.replaceNakedSingles(gridValue, candidates)
                fillinStep = 1

            elif fillinStep == 3:   #Find hidden singles
                
                foundFlag = False
                column = 0
                for row in range(9):
                    cellRange = self.findRangeToBeChecked(row_column_box='R', include_cell='Y',
                                                      rownum=row, colnum=column)
                    if self.findHiddenSingles(cellRange=cellRange, candidates=candidates,
                                                               grid=gridValue):
                        foundFlag = True

                if not foundFlag:
                    row = 0
                    for column in range(9):
                        cellRange = self.findRangeToBeChecked(row_column_box='C', include_cell='Y',
                                                          rownum=row, colnum=column)
                        if self.findHiddenSingles(cellRange=cellRange, candidates=candidates,
                                                                 grid=gridValue):
                            foundFlag = True

                if not foundFlag:
                    for row in (0, 3, 6):
                        for column in (0, 3, 6):
                            cellRange = self.findRangeToBeChecked(row_column_box='B', include_cell='Y',
                                                              rownum=row, colnum=column)
                            if self.findHiddenSingles(cellRange=cellRange, candidates=candidates,
                                                                    grid=gridValue):
                                foundFlag = True

                if foundFlag:

                    fillinStep = 4
                    wait_for_next_button = True
                    hilight_button.configure(state=DISABLED)
                else:
                    hilight_button.configure(state=ACTIVE)
                    fillinStep = 5
                    
            elif fillinStep == 4:   # replace hidden singles
                
                self.replaceHiddenSingle(grid=gridValue, candidates=candidates)
                fillinStep = 1

            elif fillinStep == 5:   # find combo of pairs, triplets, foursome and fivesome
                size = 2
                actionList = []
                if self.findCombos(candidates, actionList):
                    fillinStep = 6
                    wait_for_next_button = True
                    hilight_button.configure(state=DISABLED)
                else:
                    hilight_button.configure(state=ACTIVE)
                    fillinStep = 7

            elif fillinStep == 6:   # remove for combos of pairs, etc.

                for elements in range(len(actionList)):
                    elements = 0

                    comboNum = actionList[elements][0]
                    x = actionList[elements][1]
                    y = actionList[elements][2]
                    RCB_flag = actionList[elements][3]

                    includeCell = 'Y'
                    unmark_cellrange = []
                    cellrange = self.findRangeToBeChecked(RCB_flag, includeCell, x, y)
                    self.replaceAcross(comboNum, cellrange, candidates, unmark_cellrange)
                    fillinStep = 1
                    
            elif fillinStep == 7:   # find pointers across rows/columns/boxes
                self.appendMessage("Finding the pointing numbers....\n")
                actionList = self.findPointers(candidates)
                if len(actionList) > 0:
                    fillinStep = 8
                    wait_for_next_button = True
                    hilight_button.configure(state=DISABLED)
                else:
                    hilight_button.configure(state=ACTIVE)
                    fillinStep = 9

            elif fillinStep == 8:   # remove the pointer numbers found
                for elements in range(len(actionList)):
                    comboNum = actionList[elements][0]
                    x = actionList[elements][1]
                    y = actionList[elements][2]
                    RCB_flag = actionList[elements][3]

                    cellrange = []
                    cellrange.append([x, y, RCB_flag])
                    self.replaceAcross(comboNum, cellrange, candidates, unmark_cellrange)

                fillinStep = 1

            elif fillinStep == 9:
                self.appendMessage("Finding X Wing .....\n")
                elem, unmark_cellrange, actionList = self.find_x_wing(candidates)
                if len(actionList) > 0:
                    fillinStep = 10
                    wait_for_next_button = True
                    hilight_button.configure(state=DISABLED)
                else:
                    hilight_button.configure(state=ACTIVE)
                    fillinStep = 11

            elif fillinStep == 10:
                for elements in range(len(actionList)):
                    comboNum = actionList[elements][0]
                    x = actionList[elements][1]
                    y = actionList[elements][2]
                    RCB_flag = actionList[elements][3]

                    cellrange = []
                    cellrange.append([x, y, RCB_flag])
                    self.replaceAcross(comboNum, cellrange, candidates, unmark_cellrange)

                fillinStep = 1

            elif fillinStep == 11:
                self.appendMessage("Finding XY Wing .....\n")
                elem, unmark_cellrange, actionList = self.find_xy_wing(candidates)
                if len(actionList) > 0:
                    fillinStep = 12
                    wait_for_next_button = True
                    hilight_button.configure(state=DISABLED)
                else:
                    hilight_button.configure(state=ACTIVE)
                    fillinStep = 13

            elif fillinStep == 12:
                for elements in range(len(actionList)):
                    comboNum = actionList[elements][0]
                    x = actionList[elements][1]
                    y = actionList[elements][2]
                    RCB_flag = actionList[elements][3]

                    cellrange = []
                    cellrange.append([x, y, RCB_flag])
                    self.replaceAcross(comboNum, cellrange, candidates, unmark_cellrange)
                fillinStep = 1

            elif fillinStep == 13:
                self.appendMessage("Finding XYZ Wing .....\n")
                elem, unmark_cellrange, actionList = self.find_xyz_wing(candidates)
                if len(actionList) > 0:
                    fillinStep = 14
                    wait_for_next_button = True
                    hilight_button.configure(state=DISABLED)
                else:
                    hilight_button.configure(state=ACTIVE)
                    fillinStep = 99

            elif fillinStep == 14:
                for elements in range(len(actionList)):
                    comboNum = actionList[elements][0]
                    x = actionList[elements][1]
                    y = actionList[elements][2]
                    RCB_flag = actionList[elements][3]

                    cellrange = []
                    cellrange.append([x, y, RCB_flag])
                    self.replaceAcross(comboNum, cellrange, candidates, unmark_cellrange)
                fillinStep = 1

            else:
                self.appendMessage("Nothing more can be done. No more tricks\n")
                print(candidates)
                wait_for_next_button = True
                hilight_button.configure(state=ACTIVE)

            if self.checkCompletion(candidates):
                self.appendMessage("Puzzle Completed. Congrats. Start Another Puzzle")
                next_button.configure(state=DISABLED)
                wait_for_next_button = True
                fillinStep = 99
        return

    # Checks if the puzzle is completed
    def checkCompletion(self, candidates):
        self.candidates = candidates
        completionFlag = True
        for row in range(9):
            for column in range(9):
                if len(candidates[row][column]) > 0:
                    completionFlag = False
                    break

        return completionFlag


    # Start solving the puzzle.
    def startHints(self):
        global hints_button, next_button, gridValue, fillinStep
        # First check if there are errors in the puzzle
        if self.checkGrid():
            return

        fillinStep = 0
        next_button.config(state=ACTIVE)
        self.setMessage("Solution Started ...Press Next\n")
        return

    # Generate all possible candidates for the empty cells
    def generateCandidates(self, grid):

        self.grid = grid

        candidates = [[]]    # keeps all the potential candidates for each cell
        for row in range(9):
            candidates.append([])
            for column in range(9):
                candidates[row].append([])

        for row in range(9):
            for column in range(9):
                candidates[row][column] = ''
                if grid[row][column] == ' ':
                    cellRange = []
                    cellRange = self.findRangeToBeChecked("A", "Y", row, column)
                    count = 0
                    for number in range(9):
                        numberpresent = False
                        for cellitem in range(len(cellRange)):
                            if str(number+1) == grid[cellRange[cellitem][0]][cellRange[cellitem][1]]:
                                numberpresent = True
                            else:
                                pass
                        if not numberpresent:
                            candidates[row][column] += str(number+1)

                    gridlist[row][column].delete('1.0', END)
                    gridlist[row][column].insert('1.0', candidates[row][column])
                    gridlist[row][column].configure(bg=self.markCellColour(False, row, column),fg='Blue',
                                                    wrap=CHAR,padx=5, font=helv08)
                else:
                    gridlist[row][column].configure(bg=self.markCellColour(False, row, column),
                                                    state=DISABLED)
        return candidates

    # Replace each of the single candidates in the grid
    def findNakedSingles(self, grid, candidates):
        global gridlist, fillinStatus
        self.grid = grid
        self.candidates = candidates
        foundNakedSingles = False
        for row in range(9):
            for column in range(9):
                if len(candidates[row][column]) == 1:
                    grid[row][column] = candidates[row][column]
                    candidates[int(row)][int(column)] = 'x'     # these will be replaced in next step
                    foundNakedSingles = True
                    gridlist[row][column].configure(bg='Pink')
                    self.appendMessage(f"Naked Singles identified - {grid[row][column]}  ...Next\n")

        return foundNakedSingles

        # Replace each of the naked single candidates in the grid
    def replaceNakedSingles(self, grid, candidates):
        global gridlist, fillinStatus
        self.grid = grid
        self.candidates = candidates

        for row in range(9):
            for column in range(9):
                if candidates[row][column] == 'x':
                    candidates[row][column] = ''
                    gridlist[row][column].configure(bg=self.markCellColour(False, row, column),
                                                    fg='Blue', font=helv15B)
                    self.replaceAcross(grid[row][column],
                                       self.findRangeToBeChecked('R', 'Y', row, column),
                                       candidates, [])
                    self.replaceAcross(grid[row][column],
                                       self.findRangeToBeChecked('C', 'Y', row, column),
                                       candidates, [])
                    self.replaceAcross(grid[row][column],
                                       self.findRangeToBeChecked('B', 'Y', row, column),
                                       candidates, [])

    def findHiddenSingles(self, cellRange, candidates, grid):
        global gridlist
        self.cellRange = cellRange
        self.candidates = candidates
        self.grid = grid
        numLocation = []

        for i in range(9):
            numLocation.append([])

            # First count the occurrence of number 'i in each cellRange and store count in numLocation
            for cells in range(len(cellRange)):
                row = cellRange[cells][0]
                column = cellRange[cells][1]
                if str(i+1) in list(candidates[row][column]):
                    numLocation[i].append([str(row),str(column)])

        foundSingleOccurrences = False
        for i in range(9):
            if len(numLocation[i]) == 1:
                x = int(numLocation[i][0][0])
                y = int(numLocation[i][0][1])
                foundSingleOccurrences = True

                self.markBold('F', str(i+1), candidates[x][y], x, y, gridlist)
                gridlist[x][y].configure(bg='Pink', font=helv10B)

                candidates[x][y] = 'x'
                grid[x][y] = str(i+1)
                self.appendMessage("Hidden Singles Found - " + grid[x][y] + "  ...Next\n")

        return foundSingleOccurrences

    ## Now find the single occurrences and fill them
    def replaceHiddenSingle(self, candidates, grid):
        global gridlist, fillinStatus
        self.grid = grid
        self.candidates = candidates

        for row in range(9):
            for column in range(9):
                if candidates[row][column] == 'x':
                    candidates[row][column] = ''
                    gridlist[row][column].configure(bg=self.markCellColour(False, row, column),
                                                    fg='Blue', font=helv15B)

                    gridlist[row][column].delete('1.0', END)
                    gridlist[row][column].insert('1.0', grid[row][column])
                    self.replaceAcross(grid[row][column],
                                       self.findRangeToBeChecked('R', 'Y', row, column),
                                       candidates, [])
                    self.replaceAcross(grid[row][column],
                                       self.findRangeToBeChecked('C', 'Y', row, column),
                                       candidates, [])
                    self.replaceAcross(grid[row][column],
                                       self.findRangeToBeChecked('B', 'Y', row, column),
                                       candidates, [])

        return

# Define the function to select the file name
    def selectFile(self, arg):
        global puzzleList, filelines, gridValue, gridlist, window
        self.arg = arg
        puzzle_name = puzzleList.get()
        self.setMessage(f"Data from File {puzzle_name} loaded")
        root.title("Sudoku Solver for puzzle " + puzzle_name)
        solve_button.config(state=ACTIVE)
        puzzlenum = puzzleList.current()
        window.destroy()

        for row in range(9):
            rowDetails = list(filelines[puzzlenum * 10 + row + 1])
            print(rowDetails)
            for column in range(9):
                gridlist[row][column].configure(state=NORMAL)
                if rowDetails[column] == '0':
                    cell_entry = ' '
                    gridValue[row][column] = ' '
                else:
                    cell_entry = rowDetails[column]
                    gridValue[row][column] = cell_entry

                gridlist[row][column].delete('1.0', END)
                gridlist[row][column].update()
                gridlist[row][column].insert('1.0', cell_entry)

                gridlist[row][column].configure(bg=self.markCellColour(False, column, row),fg='Black',
                                                font=helv15)
        for x in range(9):
            rowvalue = ''
            for y in range(9):
                rowvalue += gridlist[x][y].get('1.0', END)
                rowvalue = rowvalue[:-1]
            print(rowvalue)
        print(gridValue)

    # Highlights the candidates that are pairs or candidates of specific numbers
    def highlight_candidates(self, arg):
        global hilight_options, candidates, gridlist
        self.arg = arg
        hilight_selected = hilight_options.get()

        # reset the colours of grid
        for row in range(9):
            for column in range(9):
                if candidates[row][column] == '':
                    gridlist[row][column].configure(bg=self.markCellColour(False, row, column))
                else:
                    gridlist[row][column].delete('1.0', END)
                    gridlist[row][column].configure(bg=self.markCellColour(False, row, column),
                                                    wrap=CHAR,padx=5, font=helv08)
                    gridlist[row][column].insert('1.0', candidates[row][column], 'Blue')

        if hilight_selected != 'Pairs':
            selected_num = hilight_selected[0]

        for x in range(9):
            for y in range(9):
                if len(candidates[x][y]) == 2 and hilight_selected == 'Pairs':
                    gridlist[x][y].configure(bg='Pink', font=helv10B)
                else:
                    if hilight_selected != 'Pairs':
                        if selected_num in list(candidates[x][y]):
                            self.markBold('F', selected_num, candidates[x][y], x, y, gridlist)
                            gridlist[x][y].configure(bg='Pink')


# Load the saved puzzles from the system. The puzzles are saved in a file Puzzles.txt
    def loadPuzzles(self):
        global puzzleList, filelines, window
        filename = 'SudokuPuzzles.txt'
        if path.exists(filename):
            pass
        else:
            self.setMessage("Input Puzzles file SudokuPuzzles.txt does not exist")
            return

    # label
        window = Tk()
        Label(window, text="Select the File :", font=("Times New Roman", 15)).grid(column=0,
                                             row=5, padx=10, pady=25)

    # Combobox creation
        n = StringVar()
        n = 'Select from list'
        puzzleList = ttk.Combobox(window, width=27, textvariable=n)

        puzzleList.grid(column=1, row=5)

    # First open the file of puzzles and get list of all puzzles available

        puzzleFile = open(filename)
        filelines = puzzleFile.readlines()

    # The structure of file is such that it has filename, followed by 9 lines of puzzle and then it repeats
        totalpuzzles = len(filelines) / 10
        puzzlenum = 0
        comboList = []
        while puzzlenum < totalpuzzles:
            comboList.append(filelines[puzzlenum * 10])
            puzzlenum += 1
        puzzleList['values'] = comboList
        puzzleList.bind("<<ComboboxSelected>>", self.selectFile)

    def emptygrid(self):
        global gridlist, textEntry, gridValue, boxcolour, solve_button, hints_button, message_button, next_button
        global hilight_options, hilight_button, cell_entry
        gridlist = []       # stores the grid label object in two dimensions
        gridValue = [[]]    # stores the numbers in the grid in two dimensions

        for row in range(9):
            gridlist.append([])
            gridValue.append([])
            for column in range(9):
                gridValue[row].append([])
                gridValue[row][column] = ''
                f = Frame(root, height=gridboxsize*1.2, width=gridboxsize, bd=1,
                          bg='Black')
#                f = Frame(root, height=gridboxsize*1.2, width=gridboxsize, borderleft=bLeft,
#                          bordertop=bTop,borderright=bRight,borderbottom=bBottom)
                f.pack_propagate(0)  # don't shrink
                if column in (3,6):
                    x_dimension = column * gridboxsize +3
                else:
                    x_dimension = column * gridboxsize
                if row in (3,6):
                    y_dimension = (row * gridboxsize*1.2) + 3
                else:
                    y_dimension = row * gridboxsize*1.2
                f.place(x=x_dimension, y=y_dimension)
                gridlist[row].append(Text(f, fg="Black", bg=self.markCellColour(False, row, column), font=helv15,
                                           padx=10))
                gridlist[row][column].pack(fill=BOTH, expand=1)


        # Create action buttons for 'Fill', 'Start', 'Next', Save'
        f = Frame(root, height=gridboxsize, width=gridboxsize * 9/5)
        f.pack_propagate(0)  # don't shrink
        f.place(x=0, y=9 * gridboxsize*1.2)
        fill_button = Button(f, text="Fill", font=helv15, relief=SUNKEN, justify=CENTER,
                             command=self.blankGrid)
        fill_button.pack(fill=BOTH, expand=1)
        f = Frame(root, height=gridboxsize, width=gridboxsize * 9/5)
        f.pack_propagate(0)  # don't shrink
        f.place(x=gridboxsize*9/5*1, y=9 * gridboxsize*1.2)
        solve_button = Button(f, text="Solve", font=helv15, relief=SUNKEN, state=DISABLED, justify=CENTER
                              )
        solve_button.pack(fill=BOTH, expand=1)

        f = Frame(root, height=gridboxsize, width=gridboxsize * 9/5)
        f.pack_propagate(0)  # don't shrink
        f.place(x=gridboxsize*9/5*2, y=9 * gridboxsize*1.2)
        hints_button = Button(f, text="Hints", font=helv15, relief=SUNKEN, justify=CENTER,
                              command=self.startHints)
        hints_button.pack(fill=BOTH, expand=1)

        f = Frame(root, height=gridboxsize, width=gridboxsize * 9/5)
        f.pack_propagate(0)  # don't shrink
        f.place(x=gridboxsize*9/5*3, y=9 * gridboxsize*1.2)
        load_button = Button(f, text="Load", font=helv15, relief=SUNKEN, justify=CENTER, command=self.loadPuzzles)
        load_button.pack(fill=BOTH, expand=1)

        f = Frame(root, height=gridboxsize, width=gridboxsize * 9/5)
        f.pack_propagate(0)  # don't shrink
        f.place(x=gridboxsize*9/5*4, y=9 * gridboxsize*1.2)
        hilight_label = Label(f,text='Show', font=helv10B, relief=SUNKEN, justify=CENTER)
        hilight_label.bind()
        hilight_label.pack(fill=BOTH, expand=1)

        hilight_options = StringVar()
        hilight_button = ttk.Combobox(f, textvariable = hilight_options)
        hilight_button['values'] = ["Pairs", '1s', '2s', '3s', '4s', '5s', '6s', '7s', '8s', '9s']
        hilight_button.pack(fill=BOTH, expand=1)
        hilight_button.bind("<<ComboboxSelected>>", self.highlight_candidates)

        scrollbar = Scrollbar(root)
        scrollbar.pack(side=RIGHT, fill=Y)

        f = Frame(root, height=gridboxsize*1.2*9, width=gridboxsize*5)
        f.pack_propagate(0)  # don't shrink
        f.place(x=gridboxsize*9, y=0)
        message_button = Text(f, font=helv08, relief=SUNKEN, wrap=WORD)
        self.setMessage("First please click Fill and enter puzzle data or load")
        message_button.configure(yscrollcommand=scrollbar.set)
        scrollbar.config(command=message_button.yview)
        message_button.pack(fill=BOTH, expand=1)

        f = Frame(root, height=gridboxsize, width=gridboxsize*3)
        f.pack_propagate(0)
        f.place(x=gridboxsize*10, y=gridboxsize*9*1.2)
        next_button = Button(f, font=helv15, justify=LEFT, text="Next", state=DISABLED, command=self.nextButtonAction)
        next_button.pack(fill=BOTH, expand=1)

        return


root = Tk()
root.title("Sudoku Solver")
gridboxsize = 40
root.geometry(str(str(gridboxsize * 14+20) + 'x' + str(round(gridboxsize * 10*1.2))))


helv15 = tkFont.Font(family='Arial', size=15, weight=tkFont.NORMAL)
helv15B = tkFont.Font(family='Arial', size=15, weight=tkFont.BOLD)
helv10B = tkFont.Font(family='Arial', size=10, weight=tkFont.BOLD)
helv08 = tkFont.Font(family='Arial', size=8, weight=tkFont.NORMAL)
sudokuStatus = ''
inputgridobj = InputGrid()
inputgridobj.emptygrid()


root.mainloop()
