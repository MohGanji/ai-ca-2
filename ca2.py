
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

def evaluate(schedules):
	""" schedules: 
	[
		[(p, c), ...], => schedule 
		[(p, c), ...], 
		[(p, c), ...] 
	]
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
	for schedule in schedules:
		for ind, course1 in enumerate(schedule):
			for course2 in schedule[ind:]:
				if not course1[1] == course2[1]:
					res += conflict_table[course1[1]][course2[1]]
	return res

def evaluate_schedules(schedules):
	""" sorting schedules by their evaluation value
	"""
	sortedList = sorted(schedules, key=evaluate, reverse=True )
	return sortedList


def selection(schedules):
	""" selecting SELECTION_RATE of schedules for crossover
	"""
	upper_bound = int(len(schedules)*SELECTION_RATE)
	return schedules[:upper_bound]

def mutate(schedule):
	""" mutate a schedule: 
		change place of a course from a time-slot to another
	"""
	limit = 10
	while(limit)
		first_timeslot = random.choice(schedule)
		second_timeslot = random.choice(schedule)
		if not first_timeslot == second_timeslot and len(first_timeslot) > 0:
			course_to_change = first_timeslot.pop()
			if course_is_safe(second_timeslot, course_to_change):
				second_timeslot.append(course_to_change)
				return schedule
			else:
				first_timeslot.append(course_to_change)
		limit -= 1
	return schedule

def mutation(schedules):
	""" mutate schedules with probability of MUTATION_PROB
	"""
	new_schedules = []
	for schedule in schedules:
		if random.uniform(0, 1) < MUTATION_PROB:
			schedules.append(mutate(schedule))
		else:
			schedules.append(schedule)
	return schedules

def crossover(schedule_a, schedule_b):
	""" crossover between schedules a and b,
		selecting upper bound with CROSSOVER_BOUND
	"""
	upper_bound = int(len(schedule_a)*CROSSOVER_BOUND)
	new_a = schedule_a[:upper_bound] + schedule_b[upper_bound:]
	new_b = schedule_b[:upper_bound] + schedule_a[upper_bound:]
	return new_a, new_b

	pass

def main():
	read_input()

	schedules = []
	schedules = evaluate_schedules(schedules)	


main()