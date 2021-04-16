import plotly.express as px
from Graph import WeightedGraph


def create_example_heatmap():
    data = [[1, 25, 30, 50, 1], [20, 1, 60, 80, 30], [30, 60, 1, 5, 20]]
    fig = px.imshow(data,
                    labels=dict(x="Day of Week", y="Time of Day", color="Win Rate"),
                    x=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
                    y=['Morning', 'Afternoon', 'Evening'],
                    color_continuous_scale=['floralwhite', 'lime']
                    )
    fig.update_xaxes(side="bottom")
    fig.show()


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
               'x_values': x_labels,
               'y_values': y_labels}
    return results


def create_heatmap(input_data: list, x_axis: list, y_axis: list) -> None:
    fig = px.imshow(input_data,
                    labels=dict(x="Strategy", y="Opponent", color="Points"),
                    x=x_axis,
                    y=y_axis,
                    color_continuous_scale=['floralwhite', 'lime']
                    )
    fig.update_xaxes(side="bottom")
    fig.show()
