"""CSC111 Winter 2021 Final Project

Copyright (c) 2021 Abdus Shaikh, Jason Wang, Samraj Aneja, Kevin Wang
"""
import plotly.express as px
from graph import WeightedGraph


def unpack_graph(graph: WeightedGraph) -> dict:
    """
    Takes graph and returns a dictionary with data used to create a heatmap
    """
    data, x_labels, y_labels = [], [], []

    # Generate all axis titles
    for vertex in graph.get_all_vertices():
        x_labels.append(vertex)
        y_labels.append(vertex)

    assert len(x_labels) == len(y_labels)

    # Loop over all values and assign scores to corresponding blocks in the heatmap
    for i in range(0, len(y_labels)):
        data.append([])
        for item in x_labels:
            score = graph.get_weight(item, y_labels[i])
            data[i].append(score[item])

    results = {'data': data,
               'x values': x_labels,
               'y values': y_labels}

    return results


def display_heatmap(graph: WeightedGraph) -> None:
    """ Display a heatmap with data from graph
    """
    unpacked_graph = unpack_graph(graph)
    fig = px.imshow(unpacked_graph['data'],
                    labels=dict(x="Strategy", y="Opponent", color="Points"),
                    x=unpacked_graph['x values'],
                    y=unpacked_graph['y values'],
                    color_continuous_scale=['floralwhite', 'lime']
                    )
    fig.update_xaxes(side="bottom")
    fig.show()


if __name__ == '__main__':
    import python_ta.contracts
    python_ta.contracts.check_all_contracts()

    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['plotly.express', 'graph'],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['E1136']
    })
