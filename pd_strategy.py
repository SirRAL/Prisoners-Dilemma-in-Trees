"""CSC111 Winter 2021 Final Project

Copyright (c) 2021 Abdus Shaikh, Jason Wang, Samraj Aneja, Kevin Wang
"""
from pd_game import PDGame
from game_tree import GameTree
from typing import Optional
import random
import plotly.graph_objects as go
from plotly.subplots import make_subplots


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


class LearningStrategy(Strategy):
    """A strategy which adapts to its opponent's strategy.
    """
    _game_tree: GameTree
    _temp_tree: GameTree
    _exploration_chance: float

    def __init__(self, exploration_chance: float, game_tree: GameTree = GameTree()) -> None:
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
        self._temp_tree.avg_pts_gained = game.get_points(1)
        # update avg_pts_gained for all nodes in the tree
        self._game_tree.update_after_game(game)
        # reset temp_tree
        self._temp_tree = self._game_tree

    def make_move(self, game: PDGame) -> bool:
        """Make a decision based on the "best" decision as decided by its tree, or make
        a random move if it is learning.
        """
        if self._temp_tree.get_subtrees() == []:
            return self._get_random_move()

        # random float which determines if player will explore
        rand_check = random.uniform(0, 1)

        # explore
        if rand_check < self._exploration_chance:
            return self._get_random_move()
        # don't explore
        else:
            return self._temp_tree.get_best_move()

    def _get_random_move(self) -> bool:
        """Return a random decision.
        """
        return random.choice([True, False])


def plot_game_statistics(results: list[str]) -> None:
    """Plot the outcomes and points won for each player for a given list of PD game results.
    """
    outcomes = [1 if result == 'White' else 0 for result in results]

    cumulative_win_probability = [sum(outcomes[0:i]) / i for i in range(1, len(outcomes) + 1)]
    rolling_win_probability = \
        [sum(outcomes[max(i - 50, 0):i]) / min(50, i) for i in range(1, len(outcomes) + 1)]

    fig = make_subplots(rows=2, cols=1)
    fig.add_trace(go.Scatter(y=outcomes, mode='markers',
                             name='Outcome (1 = White win, 0 = Draw/Black win)'),
                  row=1, col=1)
    fig.add_trace(go.Scatter(y=cumulative_win_probability, mode='lines',
                             name='White win percentage (cumulative)'),
                  row=2, col=1)
    fig.add_trace(go.Scatter(y=rolling_win_probability, mode='lines',
                             name='White win percentage (most recent 50 games)'),
                  row=2, col=1)
    fig.update_yaxes(range=[0.0, 1.0], row=2, col=1)

    fig.update_layout(title='Minichess Game Results', xaxis_title='Game')
    fig.show()


def test(self):
    """Test"""
    strat = LearningStrategy(0)

    # game 1
    game = PDGame(2)
    move = strat.make_move(game)
    game.decisions[game.curr_round] = (True, True)
    strat.update_game_tree_after_round(game)
    game.curr_round += 1

    move = strat.make_move(game)
    game.decisions[game.curr_round] = (True, False)
    strat.update_game_tree_after_round(game)
    strat.update_game_tree_after_game(game)

    # game 2
    game = PDGame(2)
    move = strat.make_move(game)
    game.decisions[game.curr_round] = (True, True)
    strat.update_game_tree_after_round(game)
    game.curr_round += 1

    move = strat.make_move(game)
    game.decisions[game.curr_round] = (True, True)
    strat.update_game_tree_after_round(game)
    strat.update_game_tree_after_game(game)

    # game 3
    game = PDGame(2)
    move = strat.make_move(game)
    game.decisions[game.curr_round] = (False, True)
    strat.update_game_tree_after_round(game)
    game.curr_round += 1

    move = strat.make_move(game)
    game.decisions[game.curr_round] = (False, False)
    strat.update_game_tree_after_round(game)
    strat.update_game_tree_after_game(game)


