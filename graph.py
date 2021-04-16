"""CSC111 Winter 2021 Final Project

Copyright (c) 2021 Abdus Shaikh, Jason Wang, Samraj Aneja, Kevin Wang
"""
from __future__ import annotations
from typing import Any, Union, Tuple


class _WeightedVertex:
    """A vertex in a weighted graph used to represent a strategy

    Instance Attributes:
        - item: The data stored in this vertex, representing a strategy.
        - neighbours: The vertices that are adjacent to this vertex, and the corresponding
                        edge weights

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
    """
    item: Any
    neighbours: dict[_WeightedVertex, dict[Any, Union[int, float]]]

    def __init__(self, item: Any) -> None:
        """Initialize a new vertex.

        This vertex is initialized with no neighbours.
        """
        self.item = item
        self.neighbours = {}

    # Do we need this??
    # def degree(self) -> int:
    #     """Return the degree of this vertex."""
    #     return len(self.neighbours)


class WeightedGraph:
    """A weighted graph used to store the results of match-ups between strategies.
    """
    # Private Instance Attributes:
    #     - _vertices:
    #         A collection of the vertices contained in this graph.
    #         Maps item to _WeightedVertex object.
    _vertices: dict[Any, _WeightedVertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}

    def add_vertex(self, item: Any) -> None:
        """Add a vertex with the given item and kind to this graph.

        The new vertex is not adjacent to any other vertices.
        Do nothing if the given item is already in this graph.
        """
        if item not in self._vertices:
            self._vertices[item] = _WeightedVertex(item)

    def add_edge(self, item_to_weight1: Tuple[Any, Union[int, float]],
                 item_to_weight2: Tuple[Any, Union[int, float]]) -> None:
        """Add an edge between the two vertices with the given items in this graph,
        with the given weight.

        The edge is a dictionary that stores the points of the vertices on either endpoint
        Preconditions:
            - item1 != item2
        """
        # Unpack the two tuples to make them easier to work with
        item1 = item_to_weight1[0]
        weight1 = item_to_weight1[1]

        item2 = item_to_weight2[0]
        weight2 = item_to_weight2[1]

        # Ensure item1 and item2 are vertices in the graph
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]

            # Create edge mapping with corresponding points
            weight = {item1: weight1, item2: weight2}

            v1.neighbours[v2] = weight
            v2.neighbours[v1] = weight
        else:
            # We didn't find an existing vertex for both items.
            raise ValueError

    def get_weight(self, item1: Any, item2: Any) -> dict:
        """Return the weight of the edge between the given items.

        Return 0 if item1 and item2 are not adjacent.

        Preconditions:
            - item1 and item2 are vertices in this graph
        """
        v1 = self._vertices[item1]
        v2 = self._vertices[item2]
        return v1.neighbours.get(v2, 0)

    def get_all_vertices(self) -> dict:
        """ Return a dictionary containing all vertices
        """
        return self._vertices


if __name__ == '__main__':
    import python_ta.contracts
    python_ta.contracts.check_all_contracts()

    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'extra-imports': [],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['E1136']
    })
