"""CSC111 Winter 2021 Final Project

Copyright (c) 2021 Abdus Shaikh, Jason Wang, Samraj Aneja, Kevin Wang
"""
import Strategy
from PDGame import PDGame


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
    strategy: Strategy.Strategy
    player_num: int

    def __init__(self, strategy: Strategy.Strategy, player_num: int):
        self.curr_points = 0
        self.strategy = strategy
        self.player_num = player_num
        self.strategy.assigned_player = player_num
        # Assign the strategy a player number to access the decision tuple more easily

    def make_move(self, game: PDGame) -> bool:
        """Return True if this player cooperates, and False otherwise.
        """
        return self.strategy.make_move(game)
