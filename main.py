"""CSC111 Winter 2021 Final Project

Copyright (c) 2021 Abdus Shaikh, Jason Wang, Samraj Aneja, Kevin Wang
"""
from pd_strategy import Strategy, get_all_strategies
from pd_game import PDGame
from Graph import WeightedGraph
from player import Player


class Main:
    """Main runner for Prisoner's Dilemma.
    """

    def run_game(self, game: PDGame, player1: Player, player2: Player) -> None:
        """Run a game between two computer strategies.
        """
        # player1.player_num = 1
        # player2.player_num = 2


        for i in range(0, game.num_rounds):
            game.is_p1_turn = True
            move1 = player1.make_move(game)
            game.is_p1_turn = False
            move2 = player2.make_move(game)

            round_results = game.resolve_points(move1, move2)
            player1.curr_points += round_results[0]
            player2.curr_points += round_results[1]

            game.decisions[game.curr_round] = (move1, move2)
            game.curr_round += 1

    def run_user_game(self, game: PDGame, player2: Player) -> None:
        """Run a game between a user and a computer strategy.
        """
        user = Player(strategy=None, player_num=1)
        for _ in range(0, game.num_rounds):
            game.is_p1_turn = True
            user_move = ...  # take user input
            game.is_p1_turn = False
            move2 = player2.make_move(game)

            round_results = game.resolve_points(user_move, move2)
            user.curr_points += round_results[0]
            player2.curr_points += round_results[1]

            game.decisions[game.curr_round] = (user_move, move2)
            game.curr_round += 1

    def run_tournament(self, game: PDGame, show_heatmap: bool = True) -> None:
        """Run a tournament between all strategies.

        If <show_heatmap> is set, then display a heatmap that shows the match-ups
        between the strategies.
        """
        all_strategies = get_all_strategies()
        # TODO: Change
        all_strategies_except_ai = get_all_strategies().copy().remove('Learning Strategy')
        if not show_heatmap:
            for strategy1 in all_strategies:
                new_game = PDGame(game.num_rounds)
                player1 = Player(strategy1, 1)
                for strategy2 in all_strategies_except_ai:
                    player2 = Player(strategy2, 2)
                    self.run_game(new_game, player1, player2)
        else:
            graph = WeightedGraph()

    # def resolve_round(self, decision1: bool, decision2: bool) -> None:
    #     """Takes Player 1's decision and Player 2's decision, determines
    #     each player's points gained or lost, and mutates each Player's
    #     curr_points to reflect it.
    #     """
    #     # TODO: implement this function
