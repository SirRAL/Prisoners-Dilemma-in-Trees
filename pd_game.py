"""CSC111 Winter 2021 Final Project

This module creates the PDGame (Prisoner's Dilemma Game) object class which keeps track of our game
object along with the functions associated with the PDGame class.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of TAs and instructors
involved with CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited.

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

    def resolve_round(self, round_num: int) -> tuple[int, int]:
        """Returns (p1_points, p2_points) according to the results of the round
        specified by <round_num>.

        If <round_num> is illegal, raise a ValueError.
        """
        if round_num not in self.decisions:
            raise ValueError('Tried to find results of a non-existent round!')
        else:
            decisions = self.decisions[round_num]
            return resolve_points(decisions[0], decisions[1])

    def get_points_prev(self, player_num: int) -> int:
        """Returns the number of points gained by the specified player up to the
        previous round.
        """
        return sum(self.resolve_round(round_num)[player_num - 1]
                   for round_num in range(1, self.curr_round)
                   )

    def resolve_game(self, player1_num: int, player2_num: int) -> int:
        """Returns the winner of this game. If a tie, returns 3."""
        player1_score = self.get_points_prev(player1_num)
        player2_score = self.get_points_prev(player2_num)
        if player1_score > player2_score:
            return 1
        elif player1_score < player2_score:
            return 2
        else:  # Tie
            return 3


def resolve_points(decision1: bool, decision2: bool) -> tuple[int, int]:
    """Return (p1_points, p2_points) according to the decisions made.
    """
    if decision1 is True:
        if decision2 is True:
            return (5, 5)
        else:
            return (0, 15)
    else:
        if decision2 is True:
            return (15, 0)
        else:
            return (0, 0)


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
