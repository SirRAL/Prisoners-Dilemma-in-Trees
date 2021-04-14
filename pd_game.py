"""CSC111 Winter 2021 Final Project

Copyright (c) 2021 Abdus Shaikh, Jason Wang, Samraj Aneja, Kevin Wang
"""


class PDGame:
    """A Prisoner's Dilemma game context holder.

    Instance Attributes:
      - num_rounds: number of rounds that will be played
      - curr_round: current round number
      - decisions: maps round number to (player1's decision, player2's decision)
      - is_p1_turn: True if player1 is making a decision, and False otherwise
    """
    num_rounds: int
    curr_round: int
    decisions: dict[int, tuple[bool, bool]]
    is_p1_turn: bool

    def __init__(self, num_rounds: int) -> None:
        self.num_rounds = num_rounds
        self.curr_round = 1
        self.decisions = {}
        self.is_p1_turn = True
