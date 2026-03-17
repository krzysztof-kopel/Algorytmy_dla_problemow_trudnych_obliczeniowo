def delete_vertex(edge_list, edge_mask, vertex):
    deleted = []
    for i, (vertex_a, vertex_b) in enumerate(edge_list):
        if vertex_a == vertex or vertex_b == vertex:
            edge_mask[i] = False
            deleted.append(i)
    return deleted
