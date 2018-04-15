
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


main()