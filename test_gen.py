import random
a = input()

for i in range(a):
    for j in range(a):
        if i == j:
            print 0,
        else:
            print random.randint(0, 9),
    print
