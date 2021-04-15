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

    def resolve_points(self, decision1: bool, decision2: bool) -> tuple[int, int]:
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

    def resolve_round(self, round_num: int) -> tuple[int, int]:
        """Returns (p1_points, p2_points) according to the results of the round
        specified by <round_num>.

        If <round_num> is illegal, raise a ValueError.
        """
        if round_num not in self.decisions:
            raise ValueError('Tried to find results of a non-existent round!')
        else:
            decisions = self.decisions[round_num]
            return self.resolve_points(decisions[0], decisions[1])

    # def get_points(self, player_num: int) -> int:
    #     """Returns the number of points gained by the specified player up to the
    #     current round.
    #     """
    #     return sum(self.resolve_round(round_num)[player_num - 1]
    #                for round_num in range(1, self.curr_round + 1)
    #                )

    def get_points_prev(self, player_num: int) -> int:
        """Returns the number of points gained by the specified player up to the
        previous round.
        """
        return sum(self.resolve_round(round_num)[player_num - 1]
                   for round_num in range(1, self.curr_round)
                   )
