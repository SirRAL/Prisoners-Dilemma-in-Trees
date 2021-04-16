"""CSC111 Winter 2021 Final Project

Module Description
==================

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of TAs and instructors
involved with CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited.

Copyright (c) 2021 Abdus Shaikh, Jason Wang, Samraj Aneja, Kevin Wang
"""
from __future__ import annotations
import random
from pd_game import PDGame
from game_tree import GameTree


def get_all_strategies() -> list:
    """ Return a list of all strategies
    """
    return [JesusStrategy(), LuciferStrategy(), TitForTatStrategy(),
            GrimStrategy(), ProbabilityStrategy(50), MoodyStrategy(),
            PavlovStrategy(), LearningStrategy(0.0)]


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

    def __copy__(self) -> Strategy:
        """Returns a copy of this strategy."""
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

    def __copy__(self) -> JesusStrategy:
        """"""
        return JesusStrategy()


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

    def __copy__(self) -> LuciferStrategy:
        """"""
        return LuciferStrategy()


class TitForTatStrategy(Strategy):
    """A strategy that cooperates the first round, then reciprocates the
    opponent's previous move indefinitely.
    """

    def __init__(self) -> None:
        self.name = 'Tit for Tat Strategy'
        self.desc = 'Cooperates the first round, \n then reciprocates the \n' \
                    'opponent\'s previous move indefinitely.'

    def make_move(self, game: PDGame) -> bool:
        """Cooperate if round 1, or reciprocate opponent's previous move otherwise.
        """
        curr_round = game.curr_round
        if curr_round == 1:
            return True
        else:
            return get_opponent_prev_move(game)

    def __copy__(self) -> TitForTatStrategy:
        """"""
        return TitForTatStrategy()


class GrimStrategy(Strategy):
    """A strategy that cooperates until its opponent has betrayed once, and betrays
    the rest of the game.
    """
    def __init__(self) -> None:
        self.name = 'Grim Strategy'
        self.desc = 'Cooperates until its opponent has betrayed \n' \
                    ' once, and betrays the rest of the game.'

    def _been_betrayed(self, game: PDGame) -> bool:
        """Return whether the opponent has betrayed this game or not.
        """
        return False in [decision[get_opponent_num(game)] for decision in
                         game.decisions.values()]

    def make_move(self, game: PDGame) -> bool:
        """Cooperates until its opponent has betrayed once, and betrays the rest of the game.
        Always cooperates on the first round.

        Returns True if this strategy cooperates, or returns False otherwise (betrays).
        """
        curr_round = game.curr_round

        # always cooperates on round 1 (required since we can't check prev decisions)
        if curr_round == 1:
            return True

        if self._been_betrayed(game):
            return False
        else:
            return True

    def __copy__(self) -> GrimStrategy:
        """"""
        return GrimStrategy()


class ProbabilityStrategy(Strategy):
    """A strategy that cooperates based on a fixed probability p.
    """
    chance_of_coop: float

    def __init__(self, chance_of_coop: float) -> None:
        self.name = 'Probability Strategy'
        self.desc = 'Cooperates and betrays randomly.'
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

    def __copy__(self) -> ProbabilityStrategy:
        return ProbabilityStrategy(self.chance_of_coop)


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

    def __init__(self) -> None:
        """Creates a Moody strategy with an initial mood.

        The initial mood defaults to 50.0 if no initial_mood is passed as an argument.
        """
        self.name = 'Moody Strategy'
        self.desc = 'Cooperates more often if its opponent cooperates often.'

    def make_move(self, game: PDGame) -> bool:
        """Cooperates if this player is in a good-enough mood. Betrays otherwise.

        Will also update this player's current mood based on the previous round (if
        the current round is higher than 1).
        """
        # will cooperate first round as mood will be 0
        mood = get_mood(game)
        if mood >= 0:
            return True
        else:
            return False

    def __copy__(self) -> MoodyStrategy:
        """"""
        return MoodyStrategy()


class PavlovStrategy(Strategy):
    """A strategy that cooperates if the opponent makes the same move as it, betrays otherwise.
    """

    def __init__(self) -> None:
        self.name = 'Pavlov Strategy'
        self.desc = 'Cooperates if its opponent makes the same moves. \n Will betray otherwise.'

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

    def __copy__(self) -> PavlovStrategy:
        """"""
        return PavlovStrategy()


class LearningStrategy(Strategy):
    """A strategy which adapts to its opponent's strategy.
    """
    _game_tree: GameTree
    _temp_tree: GameTree
    _exploration_chance: float

    def __init__(self, exploration_chance: float, game_tree: GameTree = GameTree()) -> None:
        self.name = 'Learning Strategy'
        self.desc = 'Chooses decisions based on what it believes will net it the most points.'
        self._game_tree = game_tree
        self._temp_tree = self._game_tree
        self._exploration_chance = exploration_chance

    def update_game_tree_after_round(self, game: PDGame) -> None:
        """Update game_tree to the latest information, as well as update
        temp_tree to have the most recent moves as its root.

        Run this after every round.
        """
        # Because self._temp_tree references self._game_tree,
        # mutating self._temp_tree in this way will also mutate self._game_tree.
        self._temp_tree.update_after_round(game)
        self._temp_tree = self._temp_tree.find_subtree_by_moves(game.decisions[game.curr_round])

    def update_game_tree_after_game(self, game: PDGame) -> None:
        """Update game_tree to the latest information, as well as reset temp_tree.

        Run this after every game.
        """
        # updates the leaf representing the final round with the actual points gained
        self._temp_tree.avg_pts_gained = game.get_points_prev(1)
        # update avg_pts_gained for all nodes in the tree
        self._game_tree.update_after_game(game)
        # reset temp_tree
        self._temp_tree = self._game_tree

    def make_move(self, game: PDGame) -> bool:
        """Make a decision based on the "best" decision as decided by its tree, or make
        a random move if it is learning.
        """
        if self._temp_tree.get_subtrees() == []:
            return _get_random_move()

        # random float which determines if player will explore
        rand_check = random.uniform(0, 1)

        # explore
        if rand_check < self._exploration_chance:
            return _get_random_move()
        # don't explore
        else:
            return self._temp_tree.get_best_move()

    def __copy__(self) -> LearningStrategy:
        return LearningStrategy(self._exploration_chance)


def get_opponent_prev_move(game: PDGame) -> bool:
    """Return the previous move done by the opponent.

    Preconditions:
      - curr_round >= 2
    """
    opponent_num = get_opponent_num(game)
    prev_round_num = game.curr_round - 1
    prev_move = game.decisions[prev_round_num][opponent_num]
    return prev_move


def get_opponent_num(game: PDGame) -> int:
    """Returns 1 if it is Player1's turn, and 0 if it is Player2's turn.
    """
    if game.is_p1_turn:
        return 1
    else:
        return 0


def _get_random_move() -> bool:
    """Return a random decision.
    """
    return random.choice([True, False])


def get_mood(game: PDGame) -> int:
    """Return current mood for moody"""
    current_mood = 0
    opponent = get_opponent_num(game)
    if opponent == 0:
        moody = 1
    else:
        moody = 0

    # go through all the rounds of the game and sum up current mood
    for round_num in game.decisions:
        if game.decisions[round_num][opponent] is True:
            # if opponent cooperates, mood is better
            current_mood += 5
        else:  # the opponent betrays
            if round_num > 1 and game.decisions[round_num - 1][opponent] is False \
                    and game.decisions[round_num - 1][moody] is True:
                # if the opponent betrayed while moody cooperates, he is extra mad
                current_mood -= 15
            else:
                current_mood -= 10

    return current_mood


if __name__ == '__main__':
    import python_ta.contracts
    python_ta.contracts.check_all_contracts()

    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['pd_game', 'game_tree', 'random'],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['E1136']
    })
