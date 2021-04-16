"""CSC111 Winter 2021 Final Project

Copyright (c) 2021 Abdus Shaikh, Jason Wang, Samraj Aneja, Kevin Wang
"""
from __future__ import annotations
import pd_strategy
from pd_game import PDGame
from typing import Optional


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

    def __init__(self, strategy: Optional[pd_strategy.Strategy], player_num: int):
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
