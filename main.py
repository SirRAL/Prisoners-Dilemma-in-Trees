"""CSC111 Winter 2021 Final Project

Copyright (c) 2021 Abdus Shaikh, Jason Wang, Samraj Aneja, Kevin Wang
"""
from pd_strategy import get_all_strategies, LearningStrategy
from pd_game import PDGame
from Graph import WeightedGraph
from player import Player


def run_game(game: PDGame, player1: Player, player2: Player) -> None:
    """Run a game between two computer strategies.
    """
    for _ in range(0, game.num_rounds):
        game.is_p1_turn = True
        move1 = player1.make_move(game)
        game.is_p1_turn = False
        move2 = player2.make_move(game)

        round_results = game.resolve_points(move1, move2)
        player1.curr_points += round_results[0]
        player2.curr_points += round_results[1]

        game.decisions[game.curr_round] = (move1, move2)

        if isinstance(player1.strategy, LearningStrategy):
            player1.strategy.update_game_tree_after_round(game)

        game.curr_round += 1


def run_user_game(game: PDGame, player2: Player) -> None:
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


def run_tournament(game: PDGame, show_heatmap: bool = True) -> None:
    """Run a tournament between all strategies.

    If <show_heatmap> is set, then display a heatmap that shows the match-ups
    between the strategies.
    """
    all_strategies = get_all_strategies()
    all_strategies_except_ai = get_all_strategies()[:7]
    if not show_heatmap:
        for strategy1 in all_strategies:
            new_game = PDGame(game.num_rounds)
            player1 = Player(strategy1, 1)
            for strategy2 in all_strategies_except_ai:
                player2 = Player(strategy2, 2)
                run_game(new_game, player1, player2)
    else:
        graph = WeightedGraph()
        for strategy1 in all_strategies:
            new_game = PDGame(game.num_rounds)
            player1 = Player(strategy1, 1)
            graph.add_vertex(player1.strategy.name)
            for strategy2 in all_strategies_except_ai:
                player2 = Player(strategy2, 2)
                graph.add_vertex(player2.strategy.name)
                run_game(new_game, player1, player2)
                graph.add_edge((player1.strategy.name, player1.curr_points),
                               (player2.strategy.name, player2.curr_points))


def get_trained_learner(player2: Player, num_rounds: int) -> Player:
    """Return a "trained" Player using a LearningStrategy against another Player using
    a specific Strategy.

    Preconditions:
      - player2.player_num == 2
    """
    num_games = 300

    exploration_chance = 1.0
    learner = LearningStrategy(exploration_chance)
    learner_player = Player(learner, 1)

    for i in range(num_games):
        learner._exploration_chance = 1.0 - (i / num_games)
        game = PDGame(num_rounds)
        run_game(game, learner_player, player2)
        learner.update_game_tree_after_game(game)

        learner_player.curr_points = 0
        player2.curr_points = 0

    return learner_player
