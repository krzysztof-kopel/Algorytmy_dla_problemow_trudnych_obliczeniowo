import dimacs
import os
from time import time
from util import delete_vertex, argmax

def runner(function, arguments):
    result, cover_set = False, set()
    start_time = time()
    arguments.append(0)
    while result != True and time() - start_time < 5:
        result, cover_set = function(*arguments)
        arguments[-1] += 1
    return result, cover_set

def vertex_cover_logn(graph, k):
    graph = [v.copy() for v in graph]
    cover_set = set()
    while any([len(i) > 0 for i in graph]):
        max_vertex = argmax(graph, lambda x, y: len(x) > len(y))
        graph = delete_vertex(graph, max_vertex)
        cover_set.add(max_vertex)
        if len(cover_set) > k:
            return False, set()
    return True, cover_set

def vertex_cover_2(graph, k):
    graph = [v.copy() for v in graph]
    cover_set = set()
    for v_idx, v_set in enumerate(graph):
        for u_idx in v_set:
            graph = delete_vertex(graph, u_idx)
            graph = delete_vertex(graph, v_idx)
            cover_set.add(v_idx)
            cover_set.add(u_idx)
            if len(cover_set) > k:
                return False, set()
            break
    else:
        return True, cover_set


if __name__ == "__main__":
    functions = {"logn": vertex_cover_logn, "2": vertex_cover_2}
    func_name = input("Select algorithm (logn, 2) or pair (algorithm, file): ")

    func_name = func_name.split(", ")
    if len(func_name) == 1:
        func_name = func_name[0]
        for file in os.listdir("graph\\"):
            if os.fsdecode(file).endswith(".sol"):
                os.remove("graph\\" + file)
        for file in os.listdir("graph\\"):
           filename = os.fsdecode(file)
           if not filename.endswith(".sol"):
               graph = dimacs.loadGraph("graph\\" + filename)
               # print(graph)

               result, cover_set = runner(functions[func_name], [graph])
               if result and len(cover_set) > 0:
                    dimacs.saveSolution("graph\\" + filename + ".sol", cover_set)
                    print(f"Graph {filename} solved")
               else:
                   print(f"Graph {filename} took too much time")
    else:
        graph = dimacs.loadGraph("graph\\" + func_name[1])
        result, cover_set = runner(functions[func_name[0]], [graph])
        if result:
            dimacs.saveSolution("graph\\" + func_name[1] + ".sol", cover_set)
            print(f"Graph {func_name[1]} solved")
        else:
            print(f"Graph {func_name[1]} took too much time")