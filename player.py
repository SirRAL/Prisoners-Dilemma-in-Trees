"""CSC111 Winter 2021 Final Project

This module handles Player, which represents any decision-maker in a game of
Prisoner's Dilemma.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of TAs and instructors
involved with CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited.

Copyright (c) 2021 Abdus Shaikh, Jason Wang, Samraj Aneja, Kevin Wang
"""
from __future__ import annotations
from typing import Optional
import pd_strategy
from pd_game import PDGame


class Player:
    """A player of Prisoner's Dilemma.

    Instance Attributes:
      - strategy: the strategy algorithm which this player uses
      - curr_points: the number of points this player has so far
      - player_num: 1 if this player is Player 1 or 2 if this player is Player 2

    Representation Invariants:
      - player_num in {1, 2}
    """
    curr_points: int
    strategy: Optional[pd_strategy.Strategy]
    player_num: int

    def __init__(self, strategy: Optional[pd_strategy.Strategy], player_num: int) -> None:
        self.curr_points = 0
        self.strategy = strategy
        self.player_num = player_num

    def __copy__(self) -> Player:
        """Create a new copy of this Player.
        """
        return Player(self.strategy.__copy__(), self.player_num)

    def make_move(self, game: PDGame) -> bool:
        """Return True if this player cooperates, and False otherwise.
        """
        return self.strategy.make_move(game)


if __name__ == '__main__':
    import python_ta.contracts
    python_ta.contracts.check_all_contracts()

    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['pd_strategy', 'pd_game'],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['E1136']
    })
