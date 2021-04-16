"""CSC111 Winter 2021 Final Project

Copyright (c) 2021 Abdus Shaikh, Jason Wang, Samraj Aneja, Kevin Wang
"""
from __future__ import annotations
from typing import Union, Optional
import random
from pd_game import PDGame


class _Branch:
    """A group of GameTrees which share that the player makes the same decision in
    each.

    # Instance Attributes:
    #  - times_picked: the number of times this branch was picked
    #  - trees: the trees in this branch
    #  - avg_pts_gained: the average points gained by the AI by picking this branch

    # Representation Invariants:
    #  - if trees is not empty, then trees[0].moves[0] == trees[1].moves[0]
    """
    times_picked: int
    avg_pts_gained: float
    trees: Union[tuple[GameTree, GameTree], tuple[()]]

    def __init__(self) -> None:
        self.times_picked = 0
        self.trees = ()
        self.avg_pts_gained = 0

    def is_empty(self) -> bool:
        """Return whether this branch has any subtrees.
        """
        return self.trees == ()

    def add_moves(self, tree1: GameTree, tree2: GameTree) -> None:
        """Add two subtrees to this branch if this branch is empty.
        """
        if self.trees == ():
            self.trees = (tree1, tree2)

    def update_pick_chance(self) -> None:
        """Recalculate the pick chance for each subtree in this branch.

        This function should be called after every ROUND is played.
        """
        for tree in self.trees:
            tree.pick_chance = tree.times_picked / self.times_picked

    def update_avg_pts_gained(self, game: PDGame) -> None:
        """Recalculate the pick chance and average points gained for
        entering this branch for the AI.

        This function should be called after every GAME is played.
        """
        # avg points gained is the weighted average points of its composite trees
        for tree in self.trees:
            tree.update_avg_pts_gained(game)

        self.avg_pts_gained = sum(game_tree.pick_chance * game_tree.avg_pts_gained
                                  for game_tree in self.trees)


class GameTree:
    """A decision tree which stores game decisions (cooperate or betray) as Boolean
    values. Decisions are stored in a binary tree, where each node represents a
    round's decisions by both Player1 and Player2.

    Instance Attributes:
      - moves: the decisions made in a (AI_Move, Opponent_Move) tuple, or () if it is the
               start of the game. This is the root of the tree.
      - times_picked: the number of times this tree was entered (this decision was made)
      - pick_chance: the probability that the opponent picks Opponent_Move
      - avg_pts_gained: this tree's estimated average number of points to gain
    """
    moves: tuple[bool, bool]
    times_picked: int
    pick_chance: float
    avg_pts_gained: float
    # Private Instance Attributes:
    #  - _c_branch: the branch where the AI cooperates
    #  - _b_branch: the branch where the AI betrays
    _c_branch: _Branch
    _b_branch: _Branch

    def __init__(self, moves: tuple[bool, bool] = ()) -> None:
        self.times_picked = 0
        self.moves = moves
        self.avg_pts_gained = 0.0
        self.pick_chance = 0.0
        self._c_branch = _Branch()
        self._b_branch = _Branch()

    def get_subtrees(self) -> list[GameTree]:
        """Return the subtrees of this game tree as a list."""
        return list(self._c_branch.trees + self._b_branch.trees)

    def find_subtree_by_moves(self, moves: tuple[bool, bool]) -> Optional[GameTree]:
        """Return the subtree corresponding to the given moves.

        Return None if no subtree corresponds to that moves.
        """
        for subtree in self.get_subtrees():
            if subtree.moves == moves:
                return subtree

        return None

    def __str__(self) -> str:
        """Return a string representation of this tree.
        """
        return self._str_indented(0)

    def _str_indented(self, depth: int) -> str:
        """Return an indented string representation of this tree.

        The indentation level is specified by the <depth> parameter.
        """
        move_desc = str(self.moves) + '\n'
        s = '  ' * depth + move_desc
        if self.get_subtrees() == []:
            return s
        else:
            for subtree in self.get_subtrees():
                s += subtree._str_indented(depth + 1)
            return s

    def add_decision_branch(self, ai_decision: bool) -> None:
        """Add this AI move and its corresponding possible opponent
        moves to this tree as a branch if it does not exist.

        Increment the number of times this branch was picked.
        """
        if ai_decision is True:  # ai chose to cooperate
            self._c_branch.times_picked += 1
            if self._c_branch.is_empty():
                subtree = GameTree((ai_decision, True))
                inv_subtree = GameTree((ai_decision, False))
                self._c_branch.add_moves(subtree, inv_subtree)
        else:  # ai chose to betray
            self._b_branch.times_picked += 1
            if self._b_branch.is_empty():
                subtree = GameTree((ai_decision, True))
                inv_subtree = GameTree((ai_decision, False))
                self._b_branch.add_moves(subtree, inv_subtree)

    def update_avg_pts_gained(self, game: PDGame) -> None:
        """Recalculate the average points gained for entering this tree for the AI.
        Should be called AFTER update_pick_chance.

        This function should be called after every GAME.
        """
        # if we just ended the game, do not update any leaves
        # (we would've update the leaf's avg_pts_gained earlier)
        if self.get_subtrees() == []:
            return
        else:
            self._c_branch.update_avg_pts_gained(game)
            self._b_branch.update_avg_pts_gained(game)

            # find max win percentage of branches
            self.avg_pts_gained = max([self._c_branch.avg_pts_gained,
                                       self._b_branch.avg_pts_gained]
                                      )

    def get_best_move(self) -> bool:
        """Return the move with the highest points gained by this owner of this tree.
        If there is a tie, choose randomly.
        """
        cooperate_avg_pts = self._c_branch.avg_pts_gained
        betray_avg_pts = self._b_branch.avg_pts_gained
        if cooperate_avg_pts > betray_avg_pts:
            return True
        elif cooperate_avg_pts < betray_avg_pts:
            return False
        else:
            return random.choice([True, False])

    def update_after_round(self, game: PDGame) -> None:
        """Updates all properties of the tree needed after every round.
        """
        self.add_decision_branch(game.decisions[game.curr_round][0])
        added_subtree = self.find_subtree_by_moves(game.decisions[game.curr_round])
        added_subtree.times_picked += 1

        branch_entered = self._c_branch if game.decisions[game.curr_round][0] is True else \
            self._b_branch
        branch_entered.update_pick_chance()

    def update_after_game(self, game: PDGame) -> None:
        """Updates all properties of the tree needed after every round.
        """
        self.update_avg_pts_gained(game)


if __name__ == '__main__':
    import python_ta.contracts
    python_ta.contracts.check_all_contracts()

    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['pd_game', 'random'],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['E1136']
    })
