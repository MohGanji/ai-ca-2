
from tqdm import tqdm 
import numpy as np
from colorama import Fore, Back, Style

# for i in tqdm(range(10000000)):
#     pass
#     # if i % 1000000:
#         # print(Fore.RED + 'some orange text')


d, t = 0, 0
course_cnt = 0
course_happiness = []
prof_cnt = 0
prof_course = {}
conflict_table = []

def init():
	pass

def read_input():
	pass
	# global d, t, c
	# d, t = map(int, raw_input().split(' '))
	# course_cnt = input()
	# course_happiness = map(int, raw_input().)


def eval(pred):
	""" pred: 
	{
		(d,t): [(p, c), ...] 
	}
	"""
	# pred = {
	# 	(1, 1): [(1, 1), (2, 2), (3,3)],
	# 	(1, 2): [(1,1)],
	# 	(1, 3): [(1, 1), (2,2)]
	# }
	# conflict_table = [
	# 	[0, 0, 0, 0],
	# 	[0, 0, 2, 1],
	# 	[0, 1, 0, 1],
	# 	[0, 1, 1, 0]
	# ]
	res = 0
	for key, val in pred.iteritems():
		for ind, course1 in enumerate(val):
			for course2 in val[ind:]:
				if not course1[1] == course2[1]:
					res += conflict_table[course1[1]][course2[1]]

	return res

def selection():
	pass

def mutation():
	pass

def crossover():
	pass

def main():
	read_input()


main()