import string
import random
from pprint import pprint
import itertools

# adding comment

# print('h' in 'hello')



# Exercise: 
# Generate a random Password which meets the following conditions
# Password length must be 10 characters long.
# It must contain at least 2 upper case letters, 1 digit, and 1 special symbol.

def generate_random_password(length = 10, upper_case = 2, digit = 1, special_symbol = 1):
    psswrd = ''
    res = random.sample(range(length), upper_case+digit+special_symbol)
    for x in range(length):
        psswrd += random.choice(string.ascii_lowercase)
    psswrd_lst = list(psswrd)
    for x in range(len(psswrd)):
        if x in res[:upper_case]:
            psswrd_lst[x] = psswrd[x].upper()
        elif x in res[upper_case:][:digit]:
            psswrd_lst[x] = str(random.randint(0,9))
        elif x in res[upper_case+digit:]:
            psswrd_lst[x] = random.choice(string.punctuation)
    psswrd = ''.join(psswrd_lst)
    return psswrd

# # testing
# print(generate_random_password())
# print(generate_random_password(special_symbol=3))
# print(generate_random_password(upper_case=5))
# print(generate_random_password(length=14))
# print(generate_random_password(digit=3))
# print(generate_random_password(length=15, upper_case=4, digit=3, special_symbol=3))

# Exercise:
# Write a function named format_number that takes a non-negative number as its only parameter.
# Your function should convert the number to a string and add commas as a thousands separator.
# For example, calling format_number(1000000) should return "1,000,000".

def format_number(num):
    if num >= 0:
        num = str(num)
        place_ = 0
        for x in range(len(num),0,-1):
            if place_ % 3 == 0 and place_ != 0:
                num = num[:x]+','+num[x:]
            place_ +=1
        return num
    else:
        return 'Error: number must be non-negative'

# teststing
# print(format_number(12345))
# print(format_number(1234567))
# print(format_number(1234567891011))
# print(format_number(-1000))

# Execise: 
# -- One line
# Writing short code
# Define a function named convert that takes a list of numbers as its only parameter and returns a list of each number converted to a string.
# For example, the call convert([1, 2, 3]) should return ["1", "2", "3"].
# What makes this tricky is that your function body must only contain a single line of code.

def convert(lst):
    return [str(x) for x in lst]

# testing
# print(convert([1,2,3]))


# Exercise:
# The description for the sudoku solver is a little more involved than the previous problems:
# Sudoku Solver (sudokusolve.py)
# Given a string in SDM format, described below, write a program to find and return the solution for the sudoku puzzle in the string. The solution should be returned in the same SDM format as the input.
# Some puzzles will not be solvable. In that case, return the string “Unsolvable”.
# The general SDM format is described here.
# For our purposes, each SDM string will be a sequence of 81 digits, one for each position on the sudoku puzzle. Known numbers will be given, and unknown positions will have a zero value.
# For example, assume you’re given this string of digits:
# 004006079000000602056092300078061030509000406020540890007410920105000000840600100
# The string represents this starting sudoku puzzle:

# 0 0 4   0 0 6   0 7 9
# 0 0 0   0 0 0   6 0 2
# 0 5 6   0 9 2   3 0 0

# 0 7 8   0 6 1   0 3 0
# 5 0 9   0 0 0   4 0 6
# 0 2 0   5 4 0   8 9 0

# 0 0 7   4 1 0   9 2 0
# 1 0 5   0 0 0   0 0 0
# 8 4 0   6 0 0   1 0 0

# The provided unit tests may take a while to run, so be patient.
# Note: A description of the sudoku puzzle can be found on Wikipedia.
# You can see that you’ll need to deal with reading and writing to a particular format as well as generating a solution. 
# Part 2: convert to either a Flask or Django App. 

def grid_dict_builder(rows):
    """
    Function to get all of the possible positions for each grid and build that information
    into a dictionary where the key is the grid and it contains a list of nested tuples for
    the position
    """
    box_dict = {}
    break_lst1 = []
    break_lst2 = []
    break_lst3 = []
    # loop through the grid
    for row_index in range(len(rows)):
        # building the first three grids
        if row_index < 3:
            break_lst1 += [(row_index, x) for x in range(len(rows[row_index][:3]))]
            break_lst2 += [(row_index, x+3) for x in range(len(rows[row_index][3:6]))]
            break_lst3 += [(row_index, x+6) for x in range(len(rows[row_index][6:]))]
            if row_index == 2:
                box_dict['grid1'] = break_lst1
                box_dict['grid2'] = break_lst2
                box_dict['grid3'] = break_lst3
                break_lst1 = []
                break_lst2 = []
                break_lst3 = []
        # building the second three grids
        elif row_index < 6:
            break_lst1 += [(row_index, x) for x in range(len(rows[row_index][:3]))]
            break_lst2 += [(row_index, x+3) for x in range(len(rows[row_index][3:6]))]
            break_lst3 += [(row_index, x+6) for x in range(len(rows[row_index][6:]))]
            if row_index == 5:
                box_dict['grid4'] = break_lst1
                box_dict['grid5'] = break_lst2
                box_dict['grid6'] = break_lst3
                break_lst1 = []
                break_lst2 = []
                break_lst3 = []
        # building the last grids
        elif row_index < 9:
            break_lst1 += [(row_index, x) for x in range(len(rows[row_index][:3]))]
            break_lst2 += [(row_index, x+3) for x in range(len(rows[row_index][3:6]))]
            break_lst3 += [(row_index, x+6) for x in range(len(rows[row_index][6:]))]
            if row_index == 8:
                box_dict['grid7'] = break_lst1
                box_dict['grid8'] = break_lst2
                box_dict['grid9'] = break_lst3
                break_lst1 = []
                break_lst2 = []
                break_lst3 = []
    return box_dict

def solving_logic(rows, possible_dict):
    """
    The brain of the operation that takes the possible dict and uses it to make the decisions on what will
    work to be filled in. It first checks the things with one possibility then trys to determine by process
    of elimination.
    """
    things_changed = 0
    # loop through possibilities
    for k, v in possible_dict.items():
        # check if only one possible
        if len(v) == 1:
            rows[k[0]][k[1]] = str(v[0])
            things_changed += 1
        # if more than one try process of elimination
        else:
            list_of_keys = [tupe for tupe in possible_dict.keys() if str(k[0]) in str(tupe[0]) or str(k[1]) in str(tupe[1])]
            for num in v:
                place_ = 0
                for key in list_of_keys:
                    if num not in possible_dict[key]:
                        place_ +=1
                if place_ == len(list_of_keys) - 2:
                    rows[k[0]][k[1]] = str(num)
                    things_changed += 1
    # print('things changed: ', things_changed)
    return (rows, things_changed)

def grid_poss_finder(rows, box_dict):
    """
    Function that gets the possible numbers for the grid to be used with getting possible dict
    """
    grid_nums_used = {}
    # loop through rows to get y
    for row_index in range(len(rows)):
        # loop through lists to get x
        for x in range(len(rows[row_index])):
            y_x = (row_index, x)
            if y_x in box_dict['grid1']:
                if rows[y_x[0]][y_x[1]] != '0':
                    if 'grid1' not in grid_nums_used:
                        grid_nums_used['grid1'] = rows[y_x[0]][y_x[1]]
                    else:
                        grid_nums_used['grid1'] += rows[y_x[0]][y_x[1]]
            if y_x in box_dict['grid2']:
                if rows[y_x[0]][y_x[1]] != '0':
                    if 'grid2' not in grid_nums_used:
                        grid_nums_used['grid2'] = rows[y_x[0]][y_x[1]]
                    else:
                        grid_nums_used['grid2'] += rows[y_x[0]][y_x[1]]
            if y_x in box_dict['grid3']:
                if rows[y_x[0]][y_x[1]] != '0':
                    if 'grid3' not in grid_nums_used:
                        grid_nums_used['grid3'] = rows[y_x[0]][y_x[1]]
                    else:
                        grid_nums_used['grid3'] += rows[y_x[0]][y_x[1]]
            if y_x in box_dict['grid4']:
                if rows[y_x[0]][y_x[1]] != '0':
                    if 'grid4' not in grid_nums_used:
                        grid_nums_used['grid4'] = rows[y_x[0]][y_x[1]]
                    else:
                        grid_nums_used['grid4'] += rows[y_x[0]][y_x[1]]
            if y_x in box_dict['grid5']:
                if rows[y_x[0]][y_x[1]] != '0':
                    if 'grid5' not in grid_nums_used:
                        grid_nums_used['grid5'] = rows[y_x[0]][y_x[1]]
                    else:
                        grid_nums_used['grid5'] += rows[y_x[0]][y_x[1]]
            if y_x in box_dict['grid6']:
                if rows[y_x[0]][y_x[1]] != '0':
                    if 'grid6' not in grid_nums_used:
                        grid_nums_used['grid6'] = rows[y_x[0]][y_x[1]]
                    else:
                        grid_nums_used['grid6'] += rows[y_x[0]][y_x[1]]
            if y_x in box_dict['grid7']:
                if rows[y_x[0]][y_x[1]] != '0':
                    if 'grid7' not in grid_nums_used:
                        grid_nums_used['grid7'] = rows[y_x[0]][y_x[1]]
                    else:
                        grid_nums_used['grid7'] += rows[y_x[0]][y_x[1]]
            if y_x in box_dict['grid8']:
                if rows[y_x[0]][y_x[1]] != '0':
                    if 'grid8' not in grid_nums_used:
                        grid_nums_used['grid8'] = rows[y_x[0]][y_x[1]]
                    else:
                        grid_nums_used['grid8'] += rows[y_x[0]][y_x[1]]
            if y_x in box_dict['grid9']:
                if rows[y_x[0]][y_x[1]] != '0':
                    if 'grid9' not in grid_nums_used:
                        grid_nums_used['grid9'] = rows[y_x[0]][y_x[1]]
                    else:
                        grid_nums_used['grid9'] += rows[y_x[0]][y_x[1]]
    return grid_nums_used


def possible_dict_builder(zero_spots, known_dict, box_dict, grid_nums_used):
    """
    Builds a dictionary for all of the zero spots that has a list of all possible numbers for each
    zero spot.
    """
    possible_dict = {}
    # loop through zero spots
    for check in zero_spots:
        y = check[0]
        x = check[1]
        y_x = (y, x)
        y_lst = []
        x_lst = []
        # checks y axis and x axis for existing numbers using known dict
        for check_x_and_y in range(9):
            if (check_x_and_y, x) in known_dict.keys():
                x_lst.append(known_dict[(check_x_and_y, x)])
            if (y, check_x_and_y) in known_dict.keys():
                y_lst.append(known_dict[(y, check_x_and_y)])
        # find what grid y_x is on
        for box_key, box_value in box_dict.items():
            if y_x in box_value:
                grid_spot = box_key
                break
        # check grid for known numbers
        grid_str = grid_nums_used[grid_spot]
        poss_lst = []
        # try to make every number between 1-9 work
        for poss in range(1, 10):
            if str(poss) not in x_lst and str(poss) not in y_lst and str(poss) not in grid_str:
                poss_lst.append(poss)
        possible_dict[tuple(check)] = poss_lst
    return possible_dict


def sudoku_solver(sdm_str):
    """
    Main function that pieces it together to recursivly solve the sudoku if possible. Will keep trying
    untill zero things have been changed on last run.
    """
    # builds the initial grid with nested loops
    rows = [[sdm_str[y] for y in range(x*9, x*9+9)] for x in range(0, 9)]
    # pprint(rows)
    known_dict = {}
    zero_spots = []
    things_changed = 0
    box_dict = grid_dict_builder(rows)
    grid_nums_used = grid_poss_finder(rows, box_dict)
    # builds zero spots and known dict... used with possible dict builder
    for row_index in range(len(rows)):
        for num_index in range(len(rows[row_index])):
            if rows[row_index][num_index] == '0':
                zero_spots.append([row_index, num_index])
            else:
                known_dict[(row_index, num_index)] = rows[row_index][num_index]
    possible_dict = possible_dict_builder(zero_spots, known_dict, box_dict, grid_nums_used)
    rows, things_changed = solving_logic(rows, possible_dict)
    # change back to a string
    back_to_string = ''.join(list(itertools.chain.from_iterable(rows)))
    # if falls here recusivly do it again
    if '0' in back_to_string and things_changed > 0:
        return sudoku_solver(back_to_string)
    # if falls here cannot be solved
    elif '0' in back_to_string and things_changed == 0:
        'Sudoku not able to be solved'
    # else it will return the finished string
    return back_to_string
print(sudoku_solver('004006079000000602056092300078061030509000406020540890007410920105000000840600100'))
