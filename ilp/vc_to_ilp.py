from dimacs import loadGraph
import pulp as pl

POWER = 0

graph_name = input("Graph name: ")
graph = loadGraph(f"graph\\{graph_name}")

model = pl.LpProblem("vc_to_sat")

variables = [model.add_variable(str(i), lowBound=0, upBound=1, cat="Continuous") for i in range(len(graph))]
model += sum([ver * len(graph[i]) ** POWER for i, ver in enumerate(variables)])

for ver_id, vertex in enumerate(graph):
    for neigh in vertex:
        model += variables[ver_id] + variables[neigh] >= 1

model.solve(pl.PULP_CBC_CMD(msg=False))
print("Solution: ")
print(*[f"x{i} = {var.varValue or 0}" for i, var in enumerate(variables)], sep="\n")
print(f"Total vertices: {len([var for var in variables if (var.varValue or 0) >= 0.5])}")

