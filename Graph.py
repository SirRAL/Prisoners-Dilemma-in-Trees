"""CSC111 Winter 2021 Final Project

Copyright (c) 2021 Abdus Shaikh, Jason Wang, Samraj Aneja, Kevin Wang
"""
from __future__ import annotations
from typing import Any, Union, Tuple


class _WeightedVertex:
    """A vertex in a weighted book review graph, used to represent a user or a book.

    Same documentation as _Vertex from Part 1, except now neighbours is a dictionary mapping
    a neighbour vertex to the weight of the edge to from self to that neighbour.
    Note that in Part 2, the weights will be integers between 1 and 5, but in Part 3 the
    weights will be floats.

    Instance Attributes:
        - item: The data stored in this vertex, representing a user or book.
        - kind: The type of this vertex: 'user' or 'book'.
        - neighbours: The vertices that are adjacent to this vertex, and their corresponding
            edge weights.

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
        - self.kind in {'user', 'book'}
    """
    item: Any
    # kind: str
    neighbours: dict[_WeightedVertex, dict[Any, Union[int, float]]]

    def __init__(self, item: Any) -> None:
        """Initialize a new vertex with the given item and kind.

        This vertex is initialized with no neighbours.

        Preconditions:
            - kind in {'user', 'book'}
        """
        self.item = item
        # self.kind = kind
        self.neighbours = {}

    def degree(self) -> int:
        """Return the degree of this vertex."""
        return len(self.neighbours)


class WeightedGraph:
    """A weighted graph used to represent a book review network that keeps track of review scores.

    Note that this is a subclass of the Graph class from Part 1, and so inherits any methods
    from that class that aren't overridden here.
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

        Preconditions:
            - kind in {'user', 'book'}
        """
        if item not in self._vertices:
            self._vertices[item] = _WeightedVertex(item)

    def add_edge(self, item_to_weight1: Tuple[Any, Union[int, float]],
                 item_to_weight2: Tuple[Any, Union[int, float]]) -> None:
        """Add an edge between the two vertices with the given items in this graph,
        with the given weight.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        # Unpack the two tuples to make them easier to work with
        item1 = item_to_weight1[0]
        weight1 = item_to_weight1[1]

        item2 = item_to_weight2[0]
        weight2 = item_to_weight2[1]
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
