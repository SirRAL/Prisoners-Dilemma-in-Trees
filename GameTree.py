"""CSC111 Winter 2021 Final Project

Copyright (c) 2021 Abdus Shaikh, Jason Wang, Samraj Aneja, Kevin Wang
"""
from PDGame import PDGame
from typing import Union

GAME_START_MOVE = '*'


class GameTree:
    """A decision tree which stores game decisions (cooperate or betray) as Boolean
    values.

    Instance Attributes:
      - curr_move: the current decision made, or '*' if it is the start of the game
      - ai_win_chance: the probability that this AI will win from the current state of
                       the game, assuming that this AI always picks the best move

    Representation Invariants:
      - curr_move in {True, False, '*'}
      - 0 <= ai_win_chance <= 100.0
    """
    curr_move: Union[bool, str]
    ai_win_chance: float
