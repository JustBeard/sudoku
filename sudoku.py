import numpy
import pdb
import sys
from numpy import *

def choise_test():
	choise = raw_input('Choise test (1, 2, 3): ')
	if choise == '3':
		sudo = array([[0, 9, 0, 3, 8, 0, 0, 0, 0], \
				[0, 0, 0, 0, 0, 0, 4, 0, 0], [7, 0, 0, 0, 0, 0, 6, 0, 0], \
				[3, 2, 0, 0, 0, 0, 0, 0, 4], [6, 0, 0, 7, 0, 5, 0, 0, 2], \
				[5, 0, 0, 0, 0, 0, 0, 1, 9], [0, 0, 4, 0, 0, 0, 0, 0, 8], \
				[0, 0, 5, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 2, 0, 7, 0]], int)
	elif choise == '2':
		sudo = array([[0, 1, 2, 0, 0, 0, 0, 0, 0], \
				[0, 0, 0, 6, 3, 5, 0, 0, 0], [7, 0, 0, 0, 0, 0, 4, 0, 9], \
				[0, 0, 0, 1, 0, 0, 0, 3, 0], [0, 5, 4, 0, 0, 0, 8, 2, 0], \
				[0, 6, 0, 0, 0, 7, 0, 0, 0], [9, 0, 8, 0, 0, 0, 0, 0, 3], \
				[0, 0, 0, 3, 2, 4, 0, 0, 0], [0, 0, 0, 0, 0, 0, 5, 7, 0]], int)
	else:
		sudo = array([[0, 0, 5, 0, 7, 0, 3, 0, 0], \
				[0, 0, 0, 0, 0, 2, 0, 6, 0], [0, 0, 0, 0, 0, 1, 0, 0, 8], \
				[0, 0, 0, 0, 3, 6, 0, 1, 0], [0, 4, 7, 0, 0, 0, 5, 3, 0], \
				[0, 9, 0, 2, 5, 0, 0, 0, 0], [2, 0, 0, 9, 0, 0, 0, 0, 0], \
				[0, 1, 0, 8, 0, 0, 0, 0, 0], [0, 0, 3, 0, 6, 0, 4, 0, 0]], int)
	return sudo

def user_set_sudoku():
	sudo = numpy.zeros((9, 9), int)
	for i in range(0, 9):
		one_row = raw_input('Sudoku row(' + str(i+1) + '):')
		k = 0
		for j in one_row:
			if j != "0":
				sudo[i, k] = int(j)
			k += 1
	return sudo

def start_array_singleton(sudo):
	result = ones((9, 9, 10), int)
	for i in range(0, 9):
		for j in range(0, 9):
			if sudo[i, j] == 0:
				result[i, j, 0] = 9
			else:
				result[i, j, 0] = 0
	return result

def start_hide_singleton(sudo):
	result = ones((9, 9, 9), int)
	for i in range(0, 9):
		result[i] = sudo
	return result
	
def del_candidate(x, y, candidate, single):
	single[x, y, 0] -= 1
	single[x, y, candidate] = 0
	if single[x, y, 0] == 1:
		fifo_single.append([x, y])
#candidate = 1 - 9
def put_mask(x, y, candidate, one_mask, single):
	block_x = (x / 3) * 3
	block_y = (y / 3) * 3
	for i in range(0, 9):
		if one_mask[x, i] == 0:
			del_candidate(x, i, candidate, single)
		one_mask[x, i] = 10
	for i in range(0, 9):
		if one_mask[i, y] == 0:
			del_candidate(i, y, candidate, single)
		one_mask[i, y] = 10
	for i in range(block_x, block_x + 3):
		for j in range(block_y, block_y + 3):
			if one_mask[i, j] == 0:
				del_candidate(i, j, candidate, single)
			one_mask[i, j] = 10

def start_mask(sudo, mask, single):
	for i in range(0, 9):
		for j in range(0, 9):
			if sudo[i, j] != 0:
				put_mask(i, j, sudo[i, j], mask[sudo[i, j] - 1], single)

def yes_single(sudo, single, mask, fifo_rec):
	if fifo_rec:
		sudo[fifo_single[0][0], fifo_single[0][1]] = fifo_single[0][2]
		single[fifo_single[0][0], fifo_single[0][1], 0] = 0
		verify_mask(fifo_single[0][0], fifo_single[0][1], mask)
		put_mask(fifo_single[0][0], fifo_single[0][1], 
				fifo_single[0][2], mask[fifo_single[0][2]-1], single)
		del fifo_rec[:]
	else:
		for i in range(1, 10):
			if single[fifo_single[0][0], fifo_single[0][1], i] == 1:
				break
		sudo[fifo_single[0][0], fifo_single[0][1]] = i
		put_mask(fifo_single[0][0], fifo_single[0][1], i, mask[i-1], single)
	x = fifo_single[0][0]
	y = fifo_single[0][1]
	del fifo_single[0]
	return x, y
	
def seek_hide_in_one(one_mask):
	for row in range(0, 9):
		count_empty = 0
		for column in range(0, 9):
			if one_mask[row, column] == 0:
				count_empty += 1
				x = row
				y = column
		if count_empty == 1:
			return [x, y]
	for column in range(0, 9):
		count_empty = 0
		for row in range(0, 9):
			if one_mask[row, column] == 0:
				count_empty += 1
				x = row
				y = column
		if count_empty == 1:
			return [x, y]
	for horiz_reg in range(0, 9, 3):
		for vert_reg in range(0, 9, 3):
			count_empty = 0
			for row in range(horiz_reg, horiz_reg + 3):
				for column in range(vert_reg, vert_reg + 3):
					if one_mask[row, column] == 0:
						count_empty += 1
						x = row
						y = column
			if count_empty == 1:
				return [x, y]
	return False

def verify_mask(x, y, mask):
	for j in range(0, 9):
		if mask[j, x, y] == 0:
			if j not in fifo_hide:
				fifo_hide.append(j)
			mask[j, x, y] = 10	
			
def seek_hide_single(sudo, single, mask):
	coord = []
	while fifo_hide:
		result_seek = seek_hide_in_one(mask[fifo_hide[0]])
		if result_seek:
			coord.append(result_seek)
			sudo[result_seek[0], result_seek[1]] = fifo_hide[0] + 1
			single[result_seek[0], result_seek[1], 0] = 0
			verify_mask(result_seek[0], result_seek[1], mask)
			put_mask(result_seek[0], result_seek[1], fifo_hide[0] + 1, 
						mask[fifo_hide[0]], single)
			if fifo_single:
				break
		else:
			del fifo_hide[0]
	return coord

def is_sudoku_full(sudo):
	count_zero = 0
	for i in range(0, 9):
		for j in range(0,9):
			if sudo[i, j] == 0:
				count_zero += 1
	if count_zero == 0:
		return True
	else:
		return False
		
def min_count_candidate(single, prev):
	buffer = []
	result = []
	x_list = -1
	for i in range(0, 9):
		buffer = buffer + list(single[i, 0:9, 0])
	for pr in prev:
		buffer[pr[0]*9 + pr[1]] = 0
	for j in range(2, 10):
		try:
			x_list = buffer.index(j)
			break
		except ValueError:
			continue
	if x_list != -1:
		x = x_list / 9
		y = x_list % 9
		for k in range(1, 10):
			if single[x, y, k] == 1:
				result.append([x, y, k])
		return result, j
	else:
		return [], j
	
def is_right(x, y, sudo):
	block_x = (x / 3) * 3
	block_y = (y / 3) * 3
	rule = [1, 1, 1, 1, 1, 1, 1, 1, 1]
	check = rule[:]
	for i in range(0, 9):
		if sudo[x, i] != 0:
			check[sudo[x, i] - 1] -= 1
	if min(check) < 0:
		return False
	check = rule[:]
	for j in range(0, 9):
		if sudo[j, y] != 0:
			check[sudo[j, y] - 1] -= 1
	if min(check) < 0:
		return False
	check = rule[:]
	for i in range(block_x, block_x + 3):
		for j in range(block_y, block_y + 3):
			if sudo[i, j] != 0:
				check[sudo[i, j] - 1] -= 1
	if min(check) < 0:
		return False
	return True
	
def solve_sudoku(sudoku, single, hide_single, fifo_recurs = []):
	var_sudoku = sudoku.copy()
	var_single = single.copy()
	var_hide_single = hide_single.copy()
	var_fifo_recurs = fifo_recurs[:]
	while fifo_single or fifo_hide:
		while fifo_single:
			x, y = yes_single(var_sudoku, var_single, var_hide_single, var_fifo_recurs)
			if fifo_recurs:
				if not is_right(x, y, var_sudoku):
					del fifo_single[:]
					del fifo_hide[:]
					return sudoku
		coord_list = seek_hide_single(var_sudoku, var_single, var_hide_single)
		if fifo_recurs:
			while coord_list:
				if not is_right(coord_list[0][0], coord_list[0][1], var_sudoku):
					del fifo_single[:]
					del fifo_hide[:]
					return sudoku
				del coord_list[0]
	if not is_sudoku_full(var_sudoku):
		exit_rec = 0
		attempt_list = []
		while exit_rec < 9:
			fifo_min, exit_rec = min_count_candidate(var_single, attempt_list)
			if fifo_min:
				attempt_list.append([fifo_min[0][0], fifo_min[0][1]])
			while fifo_min:
				#pdb.set_trace()
				fifo_single.append(fifo_min[0])
				recurs_sudoku = solve_sudoku(var_sudoku, var_single, 
										var_hide_single, fifo_min)
				del fifo_min[0]
				if is_sudoku_full(recurs_sudoku):
					return recurs_sudoku
	return var_sudoku

def main():
	sys.setrecursionlimit(1000)
	global exit_recurs
	global fifo_single
	global fifo_hide
	print 'Hello! This is magic program Sudoku-Solver!'
	choise = raw_input('Test Sudoku(1) or Other(2): ')
	if choise == '1':
		suDoku = choise_test()
	else:
		suDoku = user_set_sudoku()
	fifo_single = []
	fifo_hide = range(0, 9)
	single = start_array_singleton(suDoku)
	hide_single = start_hide_singleton(suDoku)
	start_mask(suDoku, hide_single, single)
	suDoku = solve_sudoku(suDoku, single, hide_single)
	print ('\n!!!Sudoku solved!!!')
	print suDoku
	raw_input()

main()