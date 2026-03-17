def delete_vertex(graph, vertex):
    for u in graph[vertex].copy():
        graph[vertex].remove(u)
        graph[u].remove(vertex)
    return graph