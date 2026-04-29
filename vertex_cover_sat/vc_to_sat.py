from dimacs import loadGraph, isVC
from pysat.solvers import Glucose3

def index( i, j, offset):
  return int((i+j)*(i+j+1)/2+i + offset + 1)


def solve_vc(graph: list[set], k: int) -> list[int] | None:
    """
    Function reducing vertex cover to SAT and solving it.
    :param graph: Adjacency list.
    :param k: Max number of vertices to take.
    :return: List of vertices to take in order to cover all edges.
    """
    solver = Glucose3()

    for i, vertex in enumerate(graph):
        for neighbor in vertex:
            if i < neighbor:
                solver.add_clause([i, neighbor])

    for i, _ in enumerate(graph):
        solver.add_clause([index(i, 0, len(graph))])
        if i != 0:
            solver.add_clause([-index(0, i, len(graph))])

    for i in range(1, len(graph) + 1):
        for j in range(1, len(graph) + 1):
            solver.add_clause([-index(i - 1, j, len(graph)), index(i, j, len(graph))])
            solver.add_clause([-index(i - 1, j - 1, len(graph)), -i, index(i, j, len(graph))])

    solver.add_clause([index(len(graph), 0, len(graph))])
    solver.add_clause([-index(0, len(graph) + 1, len(graph))])

    solver.add_clause([-index(len(graph), k + 1, len(graph))])

    if solver.solve():
        return [i for i in solver.get_model()[:len(graph)] if i > 0]
    return None

graph_name = input("Select graph: ")
k = int(input("Select k: "))
graph = loadGraph(f"graph\\{graph_name}")
solution = solve_vc(graph, k)
if solution is None:
    print("No solution found")
else:
    print("Vertices to take: ", solution, sep="\n")
    edge_list = []
    for i, vertex in enumerate(graph):
        for neigh in vertex:
            edge_list.append((i, neigh))
    print("Solution correct" if isVC(edge_list, set(solution)) else "Solution incorrect")
