"""CSC111 Winter 2021 Final Project

Copyright (c) 2021 Abdus Shaikh, Jason Wang, Samraj Aneja, Kevin Wang
"""
import Player


class PDGame:
    """A Prisoner's Dilemma game context holder.

    Instance Attributes:
      - num_rounds: number of rounds that will be played
      - curr_round: current round number
      - player1: player which goes first
      - player2: player which goes second
      - decisions: maps round number to (player1's decision, player2's decision)
      - is_player_1_turn: True if player1 is making a decision, and False otherwise
    """
    num_rounds: int
    curr_round: int
    player1: Player
    player2: Player
    decisions: dict[int, tuple[bool, bool]]
    is_player_1_turn: bool

    def __init__(self, num_rounds: int, player1: Player, player2: Player):
        self.num_rounds = num_rounds
        self.player1 = player1
        self.player2 = player2
        self.decisions = {}

    def run_game(self) -> None:
        """Run a game between two computer strategies.
        """
        # TODO: implement this function

    def run_user_game(self) -> None:
        """Run a game between a user and a computer strategy.
        """
        # TODO: implement this function

    def run_tournament(self, show_heatmap: bool) -> None:
        """Run a tournament between all strategies.

        If <show_heatmap> is set, then display a heatmap that shows the match-ups
        between the strategies.
        """
        # TODO: implement this function

    def resolve_round(self, decision1: bool, decision2: bool) -> None:
        """Takes Player 1's decision and Player 2's decision, determines each player's points gained or lost,
         and mutates each Player's curr_points to reflect it."""

        # TODO: implement this function
