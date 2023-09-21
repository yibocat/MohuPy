#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/3/24 下午9:29
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: Mohusets

import numpy as np


def exists_path(Graph, u, v, start=True):
    """
    If there exits a path from u to v in G with length > 0: Return True
    Else                                                  : Return False
    Recursive method
    (Checks if there exists a path from any successor u' of u to v)

        Parameters:
            Graph (networkx.DiGraph)
            u     (string),  identifier of first node in Graph
            v     (string),  identifier of second node in Graph
            start (boolean), True  if u is the recursion start
                             False else

        Returns:
            (boolean) True  if there exits a path from u to v in G
                      False else

    Additional remark:
        If the execution of this function leads to an stack overflow
        this can indicate a faulty method for the evaluation of the
        relationships that might cause circles in the Graph.
    """
    # Trivial case 1: Reached v
    if u == v and not start:
        return True
    successors = [successor for successor in Graph.neighbors(u) if not ((successor == v) and start)]
    # Trivial case 2: u has no successors
    if len(successors) == 0:
        return False
    # Recursion
    successors_on_path = [exists_path(Graph, successor, v, start=False) for successor in successors]
    return True in successors_on_path


def transitivity_elimination(Graph):
    """
    Removes edges that are implied by transitivity of the partial order

        Parameters:
            Graph (networkx.DiGraph)

         Returns:

    Additional remark:
        If the execution of this function leads to an stack overflow
        this can indicate a faulty method for the evaluation of the
        relationships that might cause circles in the Graph.
    """
    edges_to_remove = []
    for edge in Graph.edges():
        if exists_path(Graph, edge[0], edge[1], start=True):
            edges_to_remove.append(edge)
    Graph.remove_edges_from(edges_to_remove)


def layer(positions, i):
    """
    Returns the positions of nodes at layer i in a dictionary

        Parameters:
            posititions (dictionary)
            i           (int)

        Returns:
            (dictionary) the positions of nodes at layer i in a dictionary
    """
    return {position[0]: position[1] for position in positions.items() if position[1][1] == i}


def y_positioning(Graph, positions, n=0):
    """
    """
    current_layer = layer(positions, n)
    final_layer = True
    for u in current_layer:
        for v in current_layer:
            if (u, v) in Graph.edges() and positions[v][1] == n:
                final_layer = False
                positions[v] = (positions[v][0], positions[v][1] + 1)
    if final_layer:
        return positions
    else:
        return y_positioning(Graph, positions, n=n + 1)


def y_positioning_by_function(Graph, positions, layer_function):
    """
    """
    for node in Graph.nodes():
        positions[node] = (0, layer_function(node))
    return positions


def number_of_layers(positions):
    """
    Returns the number of layers in the hasse-diagramm
    (i.e. the highest y-position value in positions)

        Parameters:
            positions (dictionary)

        Returns:
            (int)
    """
    return max([position[1][1] for position in positions.items()])


def max_layer_size(positions):
    """
    Returns the maximum numbber of nodes in any layer of the hasse-diagram

        Parameters:
            positions (dictionary)

        Returns:
            (int)
    """
    return max([len(layer(positions, i)) for i in range(number_of_layers(positions))])


def shift_x_positions(positions):
    """
    Shifts the layers alternately by half a unit to the left or right along the x-axis.

    Parameters:
        positions (dictionary)

    Returns:
        (dictionary)
    """
    y_positions = np.unique([positions[position][1] for position in positions])
    for i, y_position in enumerate(y_positions):
        for position in positions:
            if positions[position][1] == y_position:
                positions[position] = (positions[position][0] + 0.5 ** (i % 2), positions[position][1])
    return positions


def x_positioning(Graph, positions, shift_x=False):
    n = number_of_layers(positions)  # height
    w = max_layer_size(positions)  # width
    for i in range(n + 1):
        current_layer = layer(positions, i)
        for j, node in enumerate(current_layer):
            positions[node] = (1 + 2 * (j + 1) * w / (len(current_layer) + 1), positions[node][1])
    if shift_x:
        return shift_x_positions(positions)
    return positions


def layout(Graph, layer_function=None, shift_x=False):
    """
    Returns a dictionary with positions for the nodes of the graph
    """
    positions = {node: (0, 0) for node in Graph.nodes()}
    try:
        positions = y_positioning_by_function(Graph, positions, layer_function)
    except:
        positions = y_positioning(Graph, positions, n=0)
    positions = x_positioning(Graph, positions)
    if shift_x:
        positions = shift_x_positions(positions)
    return positions
