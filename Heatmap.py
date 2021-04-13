import plotly.express as px
from Graph import WeightedGraph

def unpack_graph(graph: WeightedGraph) -> dict:
    data, x_values, y_values = [], [], []

    results = {'data': data,
               'x_values': x_values,
               'y_values': y_values}
    return results

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


def create_heatmap(input_data, x_axis, y_axis):
    data = input_data
    fig = px.imshow(data,
                    labels=dict(x="Day of Week", y="Time of Day", color="Win Rate"),
                    x=x_axis,
                    y=y_axis,
                    color_continuous_scale=['floralwhite', 'lime']
                    )
    fig.update_xaxes(side="bottom")
    fig.show()
