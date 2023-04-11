import random

a = random.randint(1,6)
counter = 0
dict = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0}

while counter < 123456:
    a = random.randint(1, 6)
    dict[a] += 1
    counter += 1
    print(dict)
    print(counter)
