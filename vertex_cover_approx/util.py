def delete_vertex(graph, v):
    for i, u in enumerate(graph[v].copy()):
        graph[u].remove(v)
        graph[v].remove(u)
    return graph

def argmax(lst, key):
    highest, idx = [], 0
    for i, item in enumerate(lst):
        if key(item, highest):
            highest, idx = item, i
    return idx
