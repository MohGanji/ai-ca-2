import numpy as np
from collections import defaultdict
import random

from tqdm import tqdm 
from colorama import Fore, Back, Style

# CONSTANTS:
MUTATION_PROB = 0.5
SELECTION_RATE = 0.5
CHROMOSOME_CNT = 1000
GENERATION_CNT = 5000

# GLOBALS
d, t, course_cnt = 0, 0, 0
course_happiness = []
prof_cnt = 0
prof_course = {}
course_prof = defaultdict(list)
conflict_table = []


def course_is_safe(course_list, courses, course):
	for c in courses:
		if c[0] == course[0]:
			return False
	return not ((course[1] in course_list) and course_list[course[1]])

def init():
	global d, t, course_cnt, course_happiness, prof_cnt, prof_course, conflict_table, CHROMOSOME_CNT
	result = []
	for i in xrange(0, CHROMOSOME_CNT):
		schedule = [[] for j in xrange(0, d*t)]
		course_list = {}
		rand_period = [(random.choice(course_profs), course_ind) 
			for course_ind, course_profs in course_prof.iteritems()]
		courses = np.random.permutation(rand_period).tolist()
		while(len(courses)):
			for k in xrange(0, d*t):
				if not len(courses):
					break
				random_course = courses.pop()
				if course_is_safe(course_list, schedule[k], random_course):
					schedule[k].append(random_course)
					course_list[random_course[1]] = True
		result.append({'schedule': schedule, 'course_list': course_list})
	# print "init result: ", result
	return result

def read_input():
	global d, t, course_cnt, course_happiness, prof_cnt, prof_course, conflict_table
	d, t = map(int, raw_input().split())
	course_cnt = input()
	course_happiness = [0] + map(int, raw_input().split())
	prof_cnt = input()
	for i in xrange(1, prof_cnt+1):
		courses = map(int, raw_input().split())
		courses.pop(0)
		prof_course[i] = courses
		for j in courses:
			course_prof[j].append(i)
	conflict_table = [[0 for i in xrange(0, course_cnt)]]
	for i in xrange(0, course_cnt):
		points = map(int, raw_input().split())
		points = [0] + points
		conflict_table.append(points)
	# print d, t
	# print course_cnt
	# print course_happiness
	# print prof_cnt
	# print prof_course
	# print conflict_table
	# print course_prof

def evaluate(schedule):
	""" schedule: 
	[
		[(p, c), ...], => day 
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
	# res = sum(course_happiness)
	res = 0
	for day in schedule['schedule']:
		# print "Sss: ", day
		for ind, course1 in enumerate(day):
			# print(course1)
			res += course_happiness[course1[1]]			
			for course2 in day[ind:]:
				if not course1[1] == course2[1]:
					res -= conflict_table[course1[1]][course2[1]]
	# print
	return res

def evaluate_schedules(schedules):
	""" sorting schedules by their evaluation value
	"""
	sorted_schedules = sorted(schedules, key=evaluate )
	min_val = evaluate(sorted_schedules[0])
	# sorted_schedules = [(s, evaluate(s)) for s in sorted_schedules]
	return min_val, sorted_schedules

def selection(schedules):
	""" selecting SELECTION_RATE of schedules for crossover
	"""
	upper_bound = int(len(schedules)*SELECTION_RATE)
	if upper_bound % 2:
		upper_bound += 1
	return schedules[:upper_bound]

def choose_best_day(schedule):
	best_ind = -1
	best_len = 10**100
	for ind, day in enumerate(schedule['schedule']):
		if len(day) < best_len:
			best_len = len(day)
			best_ind = ind
	return ind

def mutate(schedule):
	global d, t, course_cnt, course_happiness, prof_cnt, prof_course, course_prof, conflict_table	
	""" mutate a schedule: 
		change place of a course from a time-slot to another
	"""
	limit = 10
	course_to_change = (-1, -1)
	while(limit):
		first_timeslot = random.choice(schedule['schedule'])
		second_timeslot = random.choice(schedule['schedule'])
		if not first_timeslot == second_timeslot and len(first_timeslot) > 0:
			course_to_change = first_timeslot.pop()
			if course_is_safe(schedule['course_list'], second_timeslot, course_to_change):
				second_timeslot.append(course_to_change)	
				break
			else:
				first_timeslot.append(course_to_change)
		limit -= 1

	# if limit == 0 and course_to_change[1] != -1 and len(first_timeslot):
	# 	first_timeslot.pop()		
	# 	schedule['course_list'][course_to_change[1]] = False
	
	for i in range(1, course_cnt+1):
		# print(course_prof)
		if not (i in schedule['course_list']) or \
			schedule['course_list'][i] == False:
			if len(course_prof[i]):
				schedule['schedule'][choose_best_day(schedule)].append((random.choice(course_prof[i]), i))
				schedule['course_list'][i] = True
				break
			
	return schedule

def mutation(schedules):
	""" mutate schedules with probability of MUTATION_PROB
	"""
	new_schedules = []
	for schedule in schedules:
		if random.uniform(0, 1) < MUTATION_PROB:
			# print Fore.RED,'\n', schedule
			m = mutate(schedule)
			new_schedules.append(m)
			# print Fore.BLUE, m, Fore.WHITE
		else:
			new_schedules.append(schedule)
			# print 'HERE'
	return new_schedules

def suitable_day(schedule, day, first_course_list):
	day = [d[1] for d in day]
	# print 'Day: ',day
	# print 'Schedule: ',schedule
	intersections = [filter(lambda x: x[1] in day, day2) for day2 in schedule ]
	not_empty_cnt = 0
	res = 0
	# print "INTER: ", intersections
	for ind, day2 in enumerate(intersections):
		if len(day2):
			not_empty_cnt += 1
			res = ind
		if not_empty_cnt > 1:
			return -1
	# print 'RES: ',intersections
	
	for course in schedule[res]:
		if course not in intersections[res] and \
		(course[1] in first_course_list) or \
		((course[1] in first_course_list) and first_course_list[course[1]] == False):
			res = -1
			break

	return res

def crossover(schedule_a, schedule_b):
	""" crossover between schedules a and b,
		selecting upper bound with CROSSOVER_BOUND
	"""
	for ind, day in enumerate(schedule_a['schedule']):

		ind_b = suitable_day(schedule_b['schedule'], day, schedule_a['course_list'])
		# print 'ind_b: ', ind_b
		# print 'a: ', schedule_a['schedule'][ind]
		# print 'b: ', schedule_b['schedule'][ind_b]
		if ind_b != -1:
			# print 'B: ', Fore.RED, schedule_b['schedule'][ind_b], Fore.WHITE, schedule_b['course_list']
			# print 'A: ', Fore.RED, schedule_a['schedule'][ind], Fore.WHITE, schedule_a['course_list']
			for course in schedule_b['schedule'][ind_b]:
				schedule_b['course_list'][course[1]] = False
			for course in schedule_a['schedule'][ind]:
				schedule_a['course_list'][course[1]] = False

			schedule_b['schedule'][ind_b], schedule_a['schedule'][ind] = schedule_a['schedule'][ind], schedule_b['schedule'][ind_b]

			for course in schedule_b['schedule'][ind_b]:
				schedule_b['course_list'][course[1]] = True
			for course in schedule_a['schedule'][ind]:
				schedule_a['course_list'][course[1]] = True

			# print 'B: ',Fore.RED,schedule_b['schedule'][ind_b], Fore.WHITE, schedule_b['course_list']
			# print 'A: ',Fore.RED,schedule_a['schedule'][ind], Fore.WHITE, schedule_a['course_list']
			# print

		# print 'A:'
		# for key, val in schedule_a.iteritems():
		# 	print key, val
		# print 'B:'
		# for key, val in schedule_b.iteritems():
		# 	print key, val
		
		# print
		# print
			


	return schedule_a, schedule_b

def pretty_print(desc, objs):
	print Fore.GREEN, "{}:".format(desc), Fore.WHITE
	for obj in objs:
		print obj
	return

def check(schedule):
	flat_sched = [item for sublist in schedule['schedule'] for item in sublist]
	for course in flat_sched:
		if not (course[1] in schedule['course_list'] and schedule['course_list'][course[1]]):
			print course
			print schedule
			exit()

def main():
	global d, t, course_cnt, course_happiness, prof_cnt, prof_course, conflict_table, CHROMOSOME_CNT	
	final_result_schedule = []
	final_result = -10**100
	# pretty_print('before read_input', [d, t, course_cnt, course_happiness, prof_cnt, prof_course, conflict_table, CHROMOSOME_CNT])
	read_input()
	# pretty_print('after read_input', [d, t, course_cnt, course_happiness, prof_cnt, prof_course, conflict_table, CHROMOSOME_CNT])	
	schedules = init()
	# pretty_print('Schedules',[schedules])
	for i in xrange(0, GENERATION_CNT):
		best_val, sorted_schedules = evaluate_schedules(schedules)
		#
		if best_val == sum(course_happiness):
			final_result_schedule = sorted_schedules[0]
			final_result = best_val
			break
		elif best_val > final_result:
			final_result_schedule = sorted_schedules[0]
			final_result = best_val
			
		# pretty_print('sorted_schedules', sorted_schedules)
		selected = selection(sorted_schedules)
		for i in xrange(0, len(selected), 2):
			sorted_schedules[i], sorted_schedules[i+1] = crossover(selected[i], selected[i+1])
		
		# pretty_print('crossed_over', sorted_schedules)
		schedules = mutation(sorted_schedules)
		# pretty_print('mutated', mutated_schedules)
		check(final_result_schedule)

	print final_result_schedule
	print final_result,
	print 'of', sum(course_happiness)
	for ind, day in enumerate(final_result_schedule['schedule']):
		for ind_course, course in enumerate(day):
			print int(ind/d)+1, ind%d + 1, course[1], course[0]
	# print sum([ len(i) for i in final_result_schedule['schedule']])
	# print len(final_result_schedule['course_list'])
		

main()