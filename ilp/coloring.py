from dimacs import loadGraph
import pulp as pl

def flatten(array):
    res = []
    for sub in array:
        res.extend(sub)
    return res

POWER = 0

graph_name = input("Graph name: ")
colors = int(input("Number of colors: "))
graph = loadGraph(f"graph\\{graph_name}")

model = pl.LpProblem("coloring", pl.LpMinimize)

variables = [[model.add_variable(str(i) + "#" + str(k), lowBound=0, upBound=1, cat="Binary")
              for k in range(colors)]
              for i in range(len(graph))]

model += sum(flatten(variables))

for vertex_row in variables:
    model += sum(vertex_row) == 1

for ver_id, vertex in enumerate(graph):
    for neigh in vertex:
        for c in range(colors):
            model += variables[ver_id][c] + variables[neigh][c] <= 1

sol = model.solve(pl.PULP_CBC_CMD(msg=False))

if sol == -1:
    print("No solution")
    exit(1)

print("Solution: ")
for i, vertex_row in enumerate(variables):
    for k, var in enumerate(vertex_row):
        if var.varValue == 1:
            print(f"Vertex {i} has color {k}")
