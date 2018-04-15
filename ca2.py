
from tqdm import tqdm 
import numpy as np
from colorama import Fore, Back, Style

# CONSTANTS:
MUTATION_PROB = 0.1
CROSSOVER_BOUND = 0.5
SELECTION_RATE = 0.5

d, t, course_cnt = 0, 0, 0
course_happiness = []
prof_cnt = 0
prof_course = {}
conflict_table = []

def init():
	pass

def read_input():
	global d, t, course_cnt, course_happiness, prof_cnt, prof_course, conflict_table
	d, t = map(int, raw_input().split(' '))
	course_cnt = input()
	course_happiness = map(int, raw_input().split(' '))
	prof_cnt = input()
	for i in xrange(0, prof_cnt):
		courses = map(int, raw_input().split(' '))
		courses.pop(0)
		prof_course[i+1] = courses
	conflict_table = [[0 for i in xrange(0, course_cnt)]]
	for i in xrange(0, course_cnt):
		points = map(int, raw_input().split(' '))
		points = [0] + points
		conflict_table.append(points)
	# print d, t
	# print course_cnt
	# print course_happiness
	# print prof_cnt
	# print prof_course
	# print conflict_table

def evaluate(pred):
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

def evaluate_schedules(schedules):
	sortedList = sorted(schedules, key=evaluate, reverse=True )
	return sortedList


def selection(schedules):
	upper_bound = int(len(schedules)*SELECTION_RATE)
	return schedules[:upper_bound]

def mutation(schedules):
	""" mutate schedules with probability of MUTATION_PROB
	"""
	pass

def crossover(a, b):
	""" crossover between schedules a and b, selecting upper bound with CROSSOVER_BOUND
	"""
	pass

def main():
	read_input()

	schedules = []
	schedules = evaluate_schedules(schedules)	


main()