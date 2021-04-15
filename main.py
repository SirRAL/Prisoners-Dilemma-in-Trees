"""CSC111 Winter 2021 Final Project

Copyright (c) 2021 Abdus Shaikh, Jason Wang, Samraj Aneja, Kevin Wang
"""
from pd_strategy import Strategy
from pd_game import PDGame
from Graph import WeightedGraph
from player import Player

class Main:
    """Main runner for Prisoner's Dilemma.
    """

    def run_game(self, game: PDGame, player1: Player, player2: Player) -> None:
        """Run a game between two computer strategies.
        """
        # while game.curr_round <= game.num_rounds ?
        for i in range(0, game.num_rounds):
            # How do we update is_p1_turn ??
            move1 = player1.make_move(game)
            move2 = player2.make_move(game)

            round_results = game.resolve_points(move1, move2)
            player1.curr_points += round_results[0]
            player2.curr_points += round_results[1]

            game.decisions[game.curr_round] = (move1, move2)
            game.curr_round += 1


    def run_user_game(self) -> None:
        """Run a game between a user and a computer strategy.
        """
        # TODO: implement this function

    def run_tournament(self, show_heatmap: bool = True) -> None:
        """Run a tournament between all strategies.

        If <show_heatmap> is set, then display a heatmap that shows the match-ups
        between the strategies.
        """
        all_strategies = []

    # def resolve_round(self, decision1: bool, decision2: bool) -> None:
    #     """Takes Player 1's decision and Player 2's decision, determines
    #     each player's points gained or lost, and mutates each Player's
    #     curr_points to reflect it.
    #     """
    #     # TODO: implement this function
