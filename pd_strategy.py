"""CSC111 Winter 2021 Final Project

Copyright (c) 2021 Abdus Shaikh, Jason Wang, Samraj Aneja, Kevin Wang
"""
from pd_game import PDGame
import random


class Strategy:
    """A PD strategy algorithm which dictates what decisions to make.

    Instance Attributes:
    - name: the name of this strategy
    - desc: a description of this strategy algorithm
    """
    name: str
    desc: str

    def get_opponent_num(self, game: PDGame) -> int:
        """Returns 1 if it is Player1's turn, and 0 if it is Player2's turn.
        """
        if game.is_p1_turn:
            return 1
        else:
            return 0

    def get_opponent_prev_move(self, game: PDGame) -> bool:
        """Return the previous move done by the opponent.

        Preconditions:
          - curr_round >= 2
        """
        opponent_num = self.get_opponent_num(game)
        prev_round_num = game.curr_round - 1
        prev_move = game.decisions[prev_round_num][opponent_num]
        return prev_move

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
            return self.get_opponent_prev_move(game)

            # Alternate Method:
            # opponent_player_num = int(not bool(self.assigned_player - 1))
            # prev_move = game.decisions[curr_round - 1][opponent_player_num]
            # return prev_move
            #
            # Version without self.assigned_player:
            # if game.is_player_1_move:
            #     p2_prev_move = game.decisions[curr_round - 1][1]
            #     return p2_prev_move
            # else:  # currently player2's move
            #     p1_prev_move = game.decisions[curr_round - 1][0]
            #     return p1_prev_move


class GrimStrategy(Strategy):
    """A strategy that cooperates until its opponent has betrayed once, and betrays
    the rest of the game.
    """
    # Private Instance Attributes:
    #   - _been_betrayed: True if this player has been betrayed before, False otherwise

    _been_betrayed: bool

    def __init__(self) -> None:
        self.name = 'Grim Strategy'
        self.desc = 'Cooperates until its opponent has betrayed once, and betrays the rest of the game'
        self._been_betrayed = False

    def make_move(self, game: PDGame) -> bool:
        """Cooperates until its opponent has betrayed once, and betrays the rest of the game.
        Always cooperates on the first round.

        Returns True if this strategy cooperates, or returns False otherwise (betrays).
        """
        curr_round = game.curr_round

        # always cooperates on round 1 (required since we can't check prev decisions)
        if curr_round == 1:
            return True
        elif self._been_betrayed:
            return False
        else:
            prev_move = self.get_opponent_prev_move(game)
            if prev_move is False:
                self._been_betrayed = True
                return False
            else:
                return True

            # Version without self.assgined_player

            # # update self.been_betrayed
            # if game.is_player_1_move:
            #     p2_prev_move = game.decisions[curr_round - 1][1]
            #     if p2_prev_move is False:  # opponent betrayed last round
            #         self._been_betrayed = True
            #         return False
            # else:
            #     p1_prev_move = game.decisions[curr_round - 1][0]
            #     if p1_prev_move is False:
            #         self._been_betrayed = True
            #         return False
            #
            # # getting here means that the opponent did not betray yet
            # return True


class ProbabilityStrategy(Strategy):
    """A strategy that cooperates based on a fixed probability p.
    """
    chance_of_coop: float

    def __init__(self, chance_of_coop: float) -> None:
        self.name = 'Probability Strategy'
        self.desc = 'Cooperates based on a fixed probability.'
        self.chance_of_coop = chance_of_coop

    def make_move(self, game: PDGame) -> bool:
        """Cooperates based on a probability chance. If it succeeds, this strategy will
        cooperate, and will betray otherwise.
        """
        rand_num = random.randint(1, 100)
        if rand_num <= self.chance_of_coop:
            return True
        else:
            return False


class MoodyStrategy(Strategy):
    """A strategy that cooperates if the opponent cooperates often. Will betray otherwise.

    Instance Attributes:
      - mood: this strategy's current mood value
      - mood_threshold: the threshold to which this strategy will cooperate if its mood
                        is underneath it

    Representation Invariants:
      - 0 <= mood <= 100.0
      - 0 <= mood_threshold <= 100.0
    """
    mood: float
    mood_threshold: float

    def __init__(self, mood_threshold: float, initial_mood: float = 50.0) -> None:
        """Creates a Moody strategy with an initial mood.

        The initial mood defaults to 50.0 if no initial_mood is passed as an argument.
        """
        self.name = 'Moody Strategy'
        self.desc = 'Cooperates more often if its opponent cooperates often.'
        self.mood = initial_mood
        self.mood_threshold = mood_threshold

    def make_move(self, game: PDGame) -> bool:
        """Cooperates if this player is in a good-enough mood. Betrays otherwise.

        Will also update this player's current mood based on the previous round (if
        the current round is higher than 1).
        """
        mood_threshold = self.mood_threshold
        mood = self.mood

        # Very unsure about this implementation
        # If mood goes above the threshold once, it will never come back down
        if mood < mood_threshold:
            if mood - (10 / game.curr_round) >= 0:
                mood -= 10 / game.curr_round
            return True
        else:
            if mood + (10 / game.curr_round) <= 100:
                mood += (10 / game.curr_round)
            return False


class PavlovStrategy(Strategy):
    """A strategy that cooperates if the opponent makes the same move as it, betrays otherwise.
    """

    def __init__(self) -> None:
        self.name = 'Pavlov Strategy'
        self.desc = 'Cooperates if opponent makes the same moves. Betray otherwise'

    def make_move(self, game: PDGame) -> bool:
        """If the opponent made the same decision last round as this player, then this
        player will cooperate. Otherwise, it will betray.

        Will always cooperate on round 1.
        """
        curr_round = game.curr_round
        # Always cooperate first round because there is no previous move to check
        if curr_round == 1:
            return True
        else:
            prev_move_tuple = game.decisions[curr_round - 1]
            if prev_move_tuple[0] == prev_move_tuple[1]:  # Check move equality
                return True
            return False
