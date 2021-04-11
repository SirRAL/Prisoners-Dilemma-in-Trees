"""CSC111 Winter 2021 Final Project

Copyright (c) 2021 Abdus Shaikh, Jason Wang, Samraj Aneja, Kevin Wang
"""
import PDGame, random


class Strategy:
    """A PD strategy algorithm which dictates what decisions to make.

    Instance Attributes:
    - name: the name of this strategy
    - desc: a description of this strategy algorithm
    """
    name: str
    desc: str

    def make_move(self, game: PDGame) -> bool:
        """Return True if this Strategy cooperates, or False if this Strategy betrays."""
        raise NotImplementedError


class JesusStrategy(Strategy):
    """A strategy that cooperates indefinitely.
    """

    def __init__(self) -> None:
        self.name = 'Jesus Strategy'
        self.desc = 'Always cooperates.'

    def make_move(self, game: PDGame) -> bool:
        """Always cooperate (returns True).
        """
        return True


class LuciferStrategy(Strategy):
    """A strategy that betrays indefinitely.
    """

    def __init__(self) -> None:
        self.name = 'Lucifer Strategy'
        self.desc = 'Always betrays.'

    def make_move(self, game: PDGame) -> bool:
        """Always betray (returns False).
        """
        return False


class TitForTatStrategy(Strategy):
    """A strategy that cooperates the first round, then reciprocates the
    opponent's previous move indefinitely.
    """

    def __init__(self) -> None:
        self.name = 'Tit for Tat Strategy'
        self.desc = 'Cooperate the first round, then reciprocates the ' \
                    'opponent\'s previous move indefinitely.'

    def make_move(self, game: PDGame) -> bool:
        """Cooperate if round 1, or reciprocate opponent's previous move otherwise.
        """
        curr_round = game.curr_round
        if curr_round == 1:
            return True
        else:
            if game.is_player_1_move:
                p2_prev_move = game.decisions[curr_round - 1][1]
                return p2_prev_move
            else:  # currently player2's move
                p1_prev_move = game.decisions[curr_round - 1][0]
                return p1_prev_move


class GrimStrategy(Strategy):
    """A strategy that cooperates until its opponent has betrayed once, and betrays the rest of the game.
    """
    # Private Instance Attributes:
    #   - _been_betrayed: True if this player
    been_betrayed: bool

    def __init__(self) -> None:
        self.name = 'Grim Strategy'
        self.desc = 'Cooperates until its opponent has betrayed once, and betrays the rest of the game'
        self.been_betrayed = False

    def make_move(self, game: PDGame) -> bool:
        """Cooperates until its opponent has betrayed once, and betrays the rest of the game.
        """
        curr_round = game.curr_round

        if curr_round == 1:
            return True
        elif self.been_betrayed:
            return False
        else:
            # update self.been_betrayed
            if game.is_player_1_move:
                p2_prev_move = game.decisions[curr_round - 1][1]
                if p2_prev_move is False:
                    self.been_betrayed = True
            else:
                p1_prev_move = game.decisions[curr_round - 1][0]
                if p1_prev_move is False:
                    self.been_betrayed = True

            # TODO: complete the rest of this function


class ProbabilityStrategy(Strategy):
    """A strategy that cooperates based on a fixed probability p.
    """
    chance_of_coop: float

    def __init__(self, chance_of_coop: float) -> None:
        self.name = 'Probability Strategy'
        self.desc = 'Cooperates based on a fixed probability'
        self.chance_of_coop = chance_of_coop

    def make_move(self, game: PDGame) -> bool:
        lower_bound = random.random()
        if lower_bound >= self.chance_of_coop:
            return False
        else:
            return True


class PavlovStrategy(Strategy):
    """A strategy that cooperates if the opponent makes the same move as it, betrays otherwise.
    """

    def __init__(self) -> None:
        self.name = 'Grim Strategy'
        self.desc = 'Cooperate\'s until its opponent has defected once, and betrays the rest of the game'

    def make_move(self, game: PDGame) -> bool:
        previous_move = game.decisions
