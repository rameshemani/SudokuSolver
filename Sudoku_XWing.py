from tkinter import *
from tkinter import ttk, StringVar
from tkinter import font as tkFont
import tkinter.messagebox

from itertools import combinations

class sudoku():

    cand_xx4 = [['145', '14589', '', '456', '134569', '1349', '', '1456', '468'],
             ['', '1459', '459', '', '12459', '', '125', '1245', ''],
             ['1457', '', '4578', '2456', '12456', '14', '12568', '', '2468'],
             ['', '478', '478', '', '489', '', '689', '467', ''],
             ['1245', '12458', '', '45', '', '489', '', '24', '2489'],
             ['', '24578', '4578', '', '458', '', '28', '247', ''],
             ['2457', '', '34579', '247', '1234', '134', '1259', '', '29'],
             ['', '24', '34', '', '12346', '', '126', '1236', ''],
             ['257', '2579', '', '267', '2368', '38', '', '2356', '269'], []]
    cand_xx5 = [['', '', '89', '89', '', '', '', '', ''],
                 ['', '', '68', '', '', '', '168', '18', ''],
                 ['569', '589', '', '', '89', '', '', '', '68'],
                 ['69', '89', '', '', '289', '', '', '268', ''],
                 ['', '', '4689', '89', '24589', '58', '68', '28', ''],
                 ['', '48', '', '', '48', '', '', '', ''],
                 ['', '', '', '', '18', '', '', '168', '68'],
                 ['', '45', '14', '', '15', '', '', '', ''],
                 ['59', '', '19', '', '', '58', '18', '', ''], []]

    cand_xx3 = [['19', '', '', '78', '', '78', '', '19', ''],
             ['', '13', '', '', '', '', '13', '', ''],
             ['', '', '39', '', '', '', '', '39', ''],
             ['', '', '', '', '', '', '', '', ''],
             ['', '', '19', '58', '58', '', '19', '', ''],
             ['19', '', '', '', '', '', '38', '38', '19'],
             ['', '79', '', '1578', '58', '78', '189', '', ''],
             ['', '13', '', '13', '', '', '', '', ''],
             ['', '79', '13', '1378', '', '', '', '189', '19'], []]
    cand_x1 = [['18', '18', '', '23579', '25', '3579', '79', '26', '23679'],
               ['', '', '', '', '', '39', '49', '', '349'],
               ['', '59', '59', '27', '', '', '', '', '27'],
               ['459', '', '359', '', '', '345', '1459', '', '149'],
               ['', '59', '', '245', '258', '458', '', '26', '2469'],
               ['458', '', '358', '2345', '', '', '45', '', '24'],
               ['59', '', '', '', '', '59', '', '', ''],
               ['', '18', '89', '79', '', '', '17', '', ''],
               ['15', '', '', '457', '58', '4578', '', '', '17'], []]
    cand_x2 = [['2467', '2456', '', '567', '', '247', '', '', '57'],
               ['2479', '245', '49', '357', '34', '2479', '', '', ''],
               ['', '', '69', '567', '', '79', '', '', '57'],
               ['', '', '', '', '', '', '', '', ''],
               ['469', '146', '469', '137', '34', '478', '', '', '38'],
               ['24', '124', '', '13', '', '48', '', '', '38'],
               ['', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', ''],
               ['46', '46', '', '', '', '', '', '', ''], []]

    def transpose(self, matrix_A, matrix_B):
        self.matrix_A = matrix_A
        self.matrix_B = matrix_B

        for x in range(9):
            for y in range(9):
                matrix_B[y][x] = matrix_A[x][y]
        return

    def find_x_wing_fish_for_num(self, fish_size, num, candidates):
        self.fish_size = fish_size
        self.num = num
        self.candidates = candidates

        # first create a matrix of 'True's denoting the cells where the number occurs
        occ_matrix = [[]]
        unmark_cellrange = []
        action_list = []
        x_axis_occ = [0] * 9
        for x in range(9):
            occ_matrix.append([])
            for y in range(9):
                if str(num) in set(candidates[x][y]):
                    occ_matrix[x].append(True)
                else:
                    occ_matrix[x].append(False)

        comb_list = []
        for x in range(9):
            x_axis_occ[x] = occ_matrix[x].count(True)
            if x_axis_occ[x] <= fish_size and x_axis_occ[x] > 0:
                comb_list.append(x)
        found_flag = False
        if len(comb_list) >= fish_size:  # the number of columns must be more than fish size
            # find the combinations
            comb = combinations(comb_list, fish_size)
            # Now create union of where all number occurs in this comb columns
            for comb_item in comb:
                row_entries_list = [False] * 9
                unmark_cellrange = []
                action_list = []

                for x in range(fish_size):
                    row_entries_list = [a or b for a, b in zip(row_entries_list, occ_matrix[comb_item[x]])]

                if row_entries_list.count(True) == fish_size:
                    found_flag = True
                    # Now check if the corresponding rows have the number occuring in other columns of same rows
                    # These can be eliminated
                    for x in range(9):
                        for y in range(9):
                            if x in comb_item and str(num) in set(candidates[x][y]):
                                unmark_cellrange.append([x, y])
                            if (not (x in comb_item)) and (str(num) in set(candidates[x][y])) and row_entries_list[y]:
                                action_list.append([num, x, y, 'R'])

                    if len(action_list) > 0:
                        return found_flag, unmark_cellrange, action_list
                    else:
                        found_flag = False

        if not found_flag:
            return found_flag, unmark_cellrange, action_list

    def find_x_wing(self, candidates):
        self.candidates = candidates

        for fish_size in [2,3,4]: # This variable holds the number of x_wing count.
                        # it is 2 for X-Wing, 3 for Sword Fish and 4 for Jelly Fish
            num = 0
            found_flag = False
            while num < 9:
                search_type = "Row wise"
                found_flag, unmark_cellrange, action_list = self.find_x_wing_fish_for_num(fish_size, num+1, candidates)
                if found_flag:
                    if fish_size == 2:
                        fish_type = 'X Wing'
                    elif fish_size == 3:
                        fish_type = 'Sword Fish'
                    else:
                        fish_type = 'Jelly Fish'
                    print(search_type, " Found ", fish_type, ' at ', unmark_cellrange)
                    print('Removing ', num+1, ' at ', action_list)
                found_flag = False
                if not found_flag:  # Now check in columns
                    search_type = "Column wise"
                    transpose_A = [['' for x in range(9)] for y in range(9)]
                    self.transpose(candidates, transpose_A)
                    found_flag, unmark_cellrange, action_list = self.find_x_wing_fish_for_num(fish_size, num+1, transpose_A)
                    if found_flag:      # Inverse the x, y coordinates to get back to original coordinates
                        for x in range(len(unmark_cellrange)):
                            temp = unmark_cellrange[x][0]
                            unmark_cellrange[x][0] = unmark_cellrange[x][1]
                            unmark_cellrange[x][1] = temp

                        for x in range(len(action_list)):
                            temp = action_list[x][1]
                            action_list[x][1] = action_list[x][2]
                            action_list[x][2] = temp

                    if found_flag:
                        if fish_size == 2:
                            fish_type = 'X Wing'
                        elif fish_size == 3:
                            fish_type = 'Sword Fish'
                        else:
                            fish_type = 'Jelly Fish'
                        print(search_type, " Found ", fish_type, ' at ', unmark_cellrange)
                        print('Removing ', num+1, ' at ', action_list)
                num += 1

a= sudoku()
a.find_x_wing(a.cand_xx4)
