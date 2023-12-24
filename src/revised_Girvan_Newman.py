import networkx as nx
import random
import math

def approx_vertex_diameter(G):
    """
    Approximates the diameter of the graph using a random vertex.
    """
    node_number = G.number_of_nodes()
    random_vertex = random.choice(list(G.nodes))
    shortest_paths = nx.single_source_shortest_path(G, random_vertex)
    ordered_index = sorted(shortest_paths, key=lambda key: len(shortest_paths[key]))
    last_index = ordered_index[-1]
    last_index2 = ordered_index[-2]
    max_shortest1 = shortest_paths.get(last_index, [])
    max_shortest2 = shortest_paths.get(last_index2, [])
    diameter = len(max_shortest1) + len(max_shortest2)
    return diameter

def betweenness_centrality_approximation(G, epsilon=0.3, delta=0.5, universal_constant=0.5):
    """
    Approximates the betweenness centrality of edges in the graph.
    """
    bc = dict.fromkeys(G.edges, 0)
    edges = list(G.edges)
    vd = approx_vertex_diameter(G)
    r = (universal_constant / (epsilon * epsilon)) * (math.log((vd - 2), 2) + math.log(1 / delta))

    for _ in range(round(r + 1)):
        while True:
            sample_pair = random.sample(list(G.nodes()), 2)
            if nx.has_path(G, sample_pair[0], sample_pair[1]):
                break

        shortest_paths = nx.all_shortest_paths(G, source=sample_pair[0], target=sample_pair[1])
        shortest_paths = list(shortest_paths)
        sample_path = random.choice(shortest_paths)
        prev = sample_path[0]

        for j in range(1, len(sample_path)):
            try:
                bc[(sample_path[j], prev)] += 1 / r
            except KeyError:
                bc[(prev, sample_path[j])] += 1 / r
            prev = sample_path[j]

    sorted_bc = dict(sorted(bc.items(), key=lambda item: item[1], reverse=True))
    filtered_list = list(sorted_bc)
    return filtered_list

def remove_most_central_edges(G, most_valuable_edge, edge_number):
    """
    Removes the most central edges from the graph.
    """
    original_num_components = nx.number_connected_components(G)
    num_new_components = original_num_components
    limit = round(math.sqrt(G.number_of_edges()))
    edges = most_valuable_edge(G)

    while num_new_components <= original_num_components:
        edges_to_remove = edges[:limit]

        while edges_to_remove:
            edge = edges_to_remove[0]
            G.remove_edge(*edge)
            del edges_to_remove[0]

        new_components = tuple(nx.connected_components(G))
        num_new_components = len(new_components)
        edges = most_valuable_edge(G)

    return new_components

def revised_girvan_quick(G):
    if G.number_of_edges() == 0:
        yield tuple(nx.connected_components(G))
        return
    def most_valuable_edge(G):
        apprx = betweenness_centrality_approximation(G)
        return apprx
    # The copy of G here must include the edge weight data.
    g = G.copy().to_undirected()
    # Self-loops must be removed because their removal has no effect on
    # the connected components of the graph.
    g.remove_edges_from(nx.selfloop_edges(g))
    while g.number_of_edges() > 0:
        yield remove_most_central_edges(g, most_valuable_edge, g.number_of_edges())