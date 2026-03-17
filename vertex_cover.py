import dimacs
from itertools import combinations
import os
import time
from util import *

def vertex_cover_brute(graph):
    start_time = time.time()
    edge_list = dimacs.edgeList(graph)

    for k in range(1, len(graph)):
        for comb in combinations(edge_list, k):
            vertices = set()
            for vertex_a, vertex_b in comb:
                vertices.add(vertex_a)
                vertices.add(vertex_b)
                if dimacs.isVC(edge_list, vertices):
                    return True, vertices
                elif time.time() - start_time > 5:
                    return False, None
    return False, None

def vertex_cover_2k(graph):
    def vertex_cover_rec_2k(edge_list, k, cover_set):

        for vertex_a, vertex_b in edge_list:
            if vertex_a not in cover_set and vertex_b not in cover_set:
                selected_vec_a, selected_vec_b = vertex_a, vertex_b
                break
        else:
            return True, cover_set

        if k == 0:
            return False, set()

        cover_set.add(selected_vec_a)
        result_1, cover_set_1 = vertex_cover_rec_2k(delete_vertex(edge_list.copy(), selected_vec_a), k - 1, cover_set.copy())
        cover_set.remove(selected_vec_a)
        cover_set.add(selected_vec_b)
        result_2, cover_set_2 = vertex_cover_rec_2k(delete_vertex(edge_list.copy(), selected_vec_b), k - 1, cover_set.copy())

        if result_1:
            return True, cover_set_1
        if result_2:
            return True, cover_set_2
        return False, set()

    start_time = time.time()
    edge_list = dimacs.edgeList(graph)
    for k in range(1, len(graph)):
        result, cover_set = vertex_cover_rec_2k(edge_list, k, set())
        if result:
            return result, cover_set
        elif time.time() - start_time > 5:
            break
    return False, set()



if __name__ == "__main__":
    functions = {"brute": vertex_cover_brute, "rec_2k": vertex_cover_2k}
    func_name = input("Select algorithm (brute, rec_2k) or pair (algorithm file): ")

    func_name = func_name.split()
    if len(func_name) == 1:
        func_name = func_name[0]
        for file in os.listdir("graph\\"):
           filename = os.fsdecode(file)
           if not filename.endswith(".sol"):
               graph = dimacs.loadGraph("graph\\" + filename)

               result, cover_set = functions[func_name](graph)
               if result:
                    dimacs.saveSolution("graph\\" + filename + ".sol", cover_set)
                    print(f"Graph {filename} solved")
               else:
                   print(f"Graph {filename} can't find solution or took too much time")
    else:
        graph = dimacs.loadGraph("graph\\" + func_name[1])
        result, cover_set = functions[func_name[0]](graph)
        if result:
            dimacs.saveSolution("graph\\" + func_name[1] + ".sol", cover_set)
            print(f"Graph {func_name[1]} solved")
        else:
            print(f"Graph {func_name[1]} can't find solution or took too much time")
