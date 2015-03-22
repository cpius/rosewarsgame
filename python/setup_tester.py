from setup import get_units
from collections import Counter
from time import time


def show_time(t):
    return str(round(time() - t, 3))

nsets = 10000
t = time()
unit_sets = []
for i in range(nsets):
    unit_sets.append(get_units())

print(str(nsets), " sets generated in ", show_time(t), " seconds")


unit_counts = Counter()

for unit_set in unit_sets:
    units = [unit.name for position, unit in unit_set.items()]
    c = Counter(units)
    unit_counts += c


for element, value in unit_counts.most_common():
    print(element, value)





