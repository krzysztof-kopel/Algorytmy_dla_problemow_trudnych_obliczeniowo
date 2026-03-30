import random
from pysat.solvers import Glucose3
import matplotlib.pyplot as plt

def create_random_k_sat(k: int, claus_num: int, var_num: int) -> Glucose3:
    solver = Glucose3()
    neg = [-1, 1]
    clause = list(range(1, var_num))
    for _ in range(claus_num):
        solver.add_clause([random.choice(clause) * random.choice(neg) for _ in range(k)])
    return solver


k = 1 # SAT k-CNF
variables_num = 10
a = 0.5
success_dict = {}
while a <= 10:
    success_count = 0
    for _ in range(100):
        random_sat = create_random_k_sat(k, round(a * variables_num), variables_num)
        if random_sat.solve():
            success_count += 1
    success_dict[a] = success_count / 100
    a += 0.1 * a
plt.scatter(success_dict.keys(), success_dict.values())
plt.title(f"Size vs success (k = {k}; var_num = {variables_num})")
plt.xlabel("Size (a)")
plt.ylabel("Success rate")
plt.show()
