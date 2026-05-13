from pulp import LpProblem, LpMinimize, LpVariable, PULP_CBC_CMD

solver = PULP_CBC_CMD(msg=0)

int_model = LpProblem("ex1", LpMinimize)

x = LpVariable("x", cat="Integer")
y = LpVariable("y", cat="Integer")

int_model += x + y

int_model += y >= x - 1
int_model += y >= -4 * x + 4
int_model += y <= -0.5 * x + 3

int_model.solve(solver)
print(f"Integer solutions:\nx = {x.value()}, y = {y.value()}")

model = LpProblem("ex1", LpMinimize)

x = LpVariable("x", cat="Continuous")
y = LpVariable("y", cat="Continuous")

model += x + y

model += y >= x - 1
model += y >= -4 * x + 4
model += y <= -0.5 * x + 3

model.solve(solver)
print(f"Continuous solutions:\nx = {x.value()}, y = {y.value()}")
