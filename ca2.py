import numpy as np
from collections import defaultdict
import random

d, t, course_cnt = 0, 0, 0
course_happiness = []
prof_cnt = 0
prof_course = {}
course_prof = defaultdict(list)
conflict_table = []

CHROMOSOME_CNT = 30

def course_is_safe(courses, course):
	for c in courses:
		if c[0] == course[0]:
			return False
	return True

def init():
	global d, t, course_cnt, course_happiness, prof_cnt, prof_course, conflict_table, CHROMOSOME_CNT
	result = []
	for i in xrange(0, CHROMOSOME_CNT):
		schedule = [[] for j in xrange(0, d*t)]
		courses = np.random.permutation([(random.choice(course_prof[i]), i) for i in xrange(1, course_cnt+1)]).tolist()
		# print "random per: ", courses
		for i in xrange(0, d*t):
			if course_is_safe(schedule[i], courses[-1]):
				schedule[i].append(courses[-1])
			courses.pop()
		result.append(schedule)
	# print "init result: ", result
	return result

def read_input():
	global d, t, course_cnt, course_happiness, prof_cnt, prof_course, conflict_table
	d, t = map(int, raw_input().split(' '))
	course_cnt = input()
	course_happiness = map(int, raw_input().split(' '))
	prof_cnt = input()
	for i in xrange(1, prof_cnt+1):
		courses = map(int, raw_input().split(' '))
		courses.pop(0)
		prof_course[i] = courses
		for j in courses:
			course_prof[j].append(i)
	conflict_table = [[0 for i in xrange(0, course_cnt)]]
	for i in xrange(0, course_cnt):
		points = map(int, raw_input().split(' '))
		points = [0] + points
		conflict_table.append(points)
	# print d, t
	# print course_cnt
	# print course_happiness
	# print prof_cnt
	print prof_course
	# print conflict_table
	print course_prof


def eval():
	pass

def selection():
	pass

def mutation():
	pass

def crossover():
	pass

def main():
	read_input()
	init()


main()