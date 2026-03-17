def delete_vertex(edge_list, vertex):
    final_edge_list = []
    for u, v in edge_list:
        if vertex != u and vertex != v:
            final_edge_list.append((u, v))
    return final_edge_list
