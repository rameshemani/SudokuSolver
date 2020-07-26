from tkinter import *
from tkinter import ttk, StringVar
from tkinter import font as tkFont
import tkinter.messagebox

from itertools import combinations



cand_xx4 = [['145', '14589', '', '456', '134569', '1349', '', '1456', '468'],
         ['', '1459', '459', '', '12459', '', '125', '1245', ''],
         ['1457', '', '4578', '2456', '12456', '14', '12568', '', '2468'],
         ['', '478', '478', '', '489', '', '689', '467', ''],
         ['1245', '12458', '', '45', '', '489', '', '24', '2489'],
         ['', '24578', '4578', '', '458', '', '28', '247', ''],
         ['2457', '', '34579', '247', '1234', '134', '1259', '', '29'],
         ['', '24', '34', '', '12346', '', '126', '1236', ''],
         ['257', '2579', '', '267', '2368', '38', '', '2356', '269'], []]
cand1_xx4 = [['', '', '89', '89', '', '', '', '', ''],
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
fish_size = 4
comb = combinations([1,2,3,4,5], fish_size)
for x in comb:
    print(x)
    for y in x:
        print(y)
num = 8

# first create a matrix of 1s denoting the cells where the number occurs
occ_matrix = [[]]
for x in range(9):
    occ_matrix.append([])
    for y in range(9):
        if str(num) in set(cand1_xx4[x][y]):
            occ_matrix[x].append(True)
        else:
            occ_matrix[x].append(False)
    print(occ_matrix[x])
    print(occ_matrix)
# First doing the search over columns
col_list = []
row_entries_list = [False]*9
loop_over = False
found_flag = False
x = 0
# while not (loop_over or found_flag):
#     print("Starting base ", row_num, row_entries_list)
#     comboNum = []
#     for y in range(9):
#
#
#
#
#
#     while not loop_over:
#         if sum(bool(x) for x in [a or b for a, b in zip(row_entries_list, occ_matrix[next_col])]) <= fish_size:
#             row_entries_list = [a or b for a, b in zip(row_entries_list, occ_matrix[next_col])]
#             col_list.append(next_col)
#         print(base_col, next_col, occ_matrix[next_col], ':', row_entries_list, '-',
#               sum(bool(x) for x in row_entries_list))
#
#         next_col += 1
#         if next_col > 8:
#             if sum(bool(x) for x in row_entries_list) == fish_size:
#                 found_flag = True
#
#     base_col += 1
#     next_col = base_col
#     if base_col > (9 - fish_size): # This means there are not enough columns to search
#         loop_over = True
#     else:
#         row_entries_list = [0] * 9  # reset the row entries count list
# if found_flag:
#     print("Found ", col_list)



