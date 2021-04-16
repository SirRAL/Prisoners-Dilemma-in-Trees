"""CSC111 Winter 2021 Final Project

Module Description
==================

This module handles the main functionality of running a game of Prisoner's Dilemma,
including displaying and handling the user interface (UI).

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of TAs and instructors
involved with CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited.

Copyright (c) 2021 Abdus Shaikh, Jason Wang, Samraj Aneja, Kevin Wang
"""
from tkinter import Tk, Label, Button, Frame, StringVar, ttk, Listbox, messagebox
from typing import Any, Callable
from pd_strategy import get_all_strategies, LearningStrategy, JesusStrategy
from pd_game import PDGame, resolve_points
from graph import WeightedGraph
from player import Player
from heatmap import display_heatmap


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


def run_game(game: PDGame, player1: Player, player2: Player) -> None:
    """Run a game between two computer strategies.
    """
    for _ in range(0, int(game.num_rounds)):
        game.is_p1_turn = True
        move1 = player1.make_move(game)
        game.is_p1_turn = False
        move2 = player2.make_move(game)

        round_results = resolve_points(move1, move2)
        player1.curr_points += round_results[0]
        player2.curr_points += round_results[1]

        game.decisions[game.curr_round] = (move1, move2)

        if isinstance(player1.strategy, LearningStrategy):
            player1.strategy.update_game_tree_after_round(game)

        game.curr_round += 1


def create_and_run_game(num_rounds: int, player1: Player, player2: Player) -> None:
    """Create and run a new (non-persistent) game between two computer strategies.
    """

    if isinstance(player1.strategy, LearningStrategy):
        player1 = get_trained_learner(player2, num_rounds)

    game = PDGame(num_rounds)

    for _ in range(0, game.num_rounds):
        game.is_p1_turn = True
        move1 = player1.make_move(game)
        game.is_p1_turn = False
        move2 = player2.make_move(game)

        round_results = resolve_points(move1, move2)
        player1.curr_points += round_results[0]
        player2.curr_points += round_results[1]

        game.decisions[game.curr_round] = (move1, move2)

        if isinstance(player1.strategy, LearningStrategy):
            player1.strategy.update_game_tree_after_round(game)

        game.curr_round += 1

    ai_vs_ai_summary_screen(game, player1, player2)


def run_tournament(game: PDGame) -> None:
    """Run a tournament between all strategies.

    If <show_heatmap> is set, then display a heatmap that shows the match-ups
    between the strategies.
    """

    all_strategies = get_all_strategies()

    graph = WeightedGraph()
    for s1 in all_strategies:
        for s2 in all_strategies:
            new_game = PDGame(game.num_rounds)
            strategy1 = s1.__copy__()
            strategy2 = s2.__copy__()

            player1 = Player(strategy1, 1)
            player2 = Player(strategy2, 2)

            if isinstance(player1.strategy, LearningStrategy):
                player1 = get_trained_learner(player2, game.num_rounds)

            graph.add_vertex(player1.strategy.name)

            graph.add_vertex(player2.strategy.name)

            run_game(new_game, player1, player2)
            if strategy1.name == 'Learning Strategy' and strategy2.name == 'Learning Strategy':
                player1.curr_points, player2.curr_points = 0, 0

            graph.add_edge((player1.strategy.name, player1.curr_points),
                           (player2.strategy.name, player2.curr_points))

    display_heatmap(graph)


def draw_main_window() -> None:
    """Draws the starting menu for the user.
    Execute this function on startup of this module.
    """
    root = Tk()
    root.title('Prisoner\'s Dilemma')

    title_label = Label(root, text='Prisoner\'s Dilemma', font='TkHeadingFont:')

    title_label.grid(row=0, column=2)

    frame = Frame(root)

    frame.grid(row=4, column=2)

    instructions = Label(root, text='Welcome to Prisoner\'s Dilemma, a classic experiment '
                                    'in game theory that investigates how seemingly perfect,'
                                    ' rational decisions can be more harmful than helpful.')

    instructions.grid(row=1, column=2, padx=30)

    instructions1 = Label(root, text='\n The rules are simple: \n You and your opponent take turns '
                                     'choosing in secret to either cooperate or betray. '
                                     '\n If both of you choose to cooperate, you both '
                                     'benefit and gain points. \n If one of you cooperates '
                                     'and the other betrays, then the cooperator loses '
                                     'points while the betrayer gains points. \n If both of you '
                                     'betray each other, then everyone gets no points!')

    instructions1.grid(row=2, column=2)

    instructions2 = Label(root, text='On the left, you can make AI strategies compete against '
                                     'other AI strategies. One of them can also be a learning AI! '
                                     '\n In the middle, you can also test your wits and face off '
                                     'against one of the archetypes! \n '
                                     'On the right, you can make every predetermined strategy '
                                     'face off in a glorious tournament!')

    instructions2.grid(row=3, column=2)

    ai_v_ai_button = Button(frame, text='AI vs. AI',
                            command=lambda: destroy_and_open(root, draw_ai_vs_ai))
    player_v_ai_button = Button(frame, text='Player vs. AI',
                                command=lambda: destroy_and_open(root, draw_player_vs_ai))
    battle_royale_button = Button(frame, text='AI Battle Royale',
                                  command=lambda: destroy_and_open(root, draw_battle_royale))

    ai_v_ai_button.grid(row=1, column=1, padx=30, pady=20)
    player_v_ai_button.grid(row=1, column=2, padx=30, pady=20)
    battle_royale_button.grid(row=1, column=3, padx=30, pady=20)

    player_v_ai_button.place()
    root.mainloop()


def destroy_and_open(window: Tk, function: Callable) -> Any:
    """Destroys window and calls function."""
    window.destroy()
    function()


def draw_ai_vs_ai() -> None:
    """Draws the AI vs. AI interface."""
    root = Tk()

    # prevent window from being manually resized as it causes weird behaviour with labels
    root.resizable(False, False)

    root.title('AI vs. AI')

    title_label = Label(root, text='AI vs. AI', font='TkHeadingFont:')

    title_label.grid(row=1, column=2)

    instructions = Label(root, text='Here, you can select two AI strategies and '
                                    'pit them against each other to see who reigns supreme!',
                         padx=30)

    instructions.grid(row=2, column=2)

    # input number of rounds
    input_frame = Frame(root)
    input_frame.grid(row=3, column=2)
    instructions2 = Label(input_frame, text='Number of rounds to be played: ')
    instructions2.grid(row=1, column=1)

    num_rounds_possible = [str(x) for x in range(10, 26)]
    num_rounds = StringVar(root)
    num_rounds.set(num_rounds_possible[0])
    input_field = ttk.Combobox(input_frame, textvariable=num_rounds, values=num_rounds_possible,
                               state='readonly')
    input_field.grid(row=2, column=1, pady=10)

    game = PDGame(int(num_rounds.get()))
    game.is_p1_turn = False

    def game_update_rounds() -> None:
        """Updates the game's num_rounds to the latest choice made by the user."""
        game.num_rounds = int(num_rounds.get())

    input_field.bind('<<ComboboxSelected>>', game_update_rounds())

    # Matchup label
    matchup_label = Label(root, text='Matchup: ')
    matchup_label.grid(row=4, column=2, pady=15)

    # dropdown menus
    jesus = get_all_strategies()[0]
    lucifer = get_all_strategies()[1]
    tit_for_tat = get_all_strategies()[2]
    grim = get_all_strategies()[3]
    probability = get_all_strategies()[4]
    moody = get_all_strategies()[5]
    pavlov = get_all_strategies()[6]
    learning = get_all_strategies()[7]

    # initialize strategy info
    strategies_1 = [jesus, lucifer, tit_for_tat, grim, probability, moody, pavlov, learning]
    strategies_2 = strategies_1[:7]
    strategy_names = [strategy.name for strategy in strategies_1]
    strategy_names_2 = [strategy.name for strategy in strategies_2]
    name_to_desc = {strategy.name: strategy.desc for strategy in strategies_1}

    # create dropdown menu frame
    dropdown_frame = Frame(root)
    dropdown_frame.grid(row=5, column=2)

    player1_selection, player2_selection = StringVar(root), StringVar(root)

    # set initial menu selection to Jesus
    player1_selection.set(strategy_names[0])
    player2_selection.set(strategy_names[0])

    # set descriptions
    player1_desc = Label(dropdown_frame, text=name_to_desc[player1_selection.get()])
    player2_desc = Label(dropdown_frame, text=name_to_desc[player2_selection.get()])
    player1_desc.grid(row=2, column=1, padx=20)
    player2_desc.grid(row=2, column=3, padx=20)

    def change_strategy(event=None) -> None:
        """Updates the strategy descriptions to their latest state
        and updates the strategies accordingly."""
        if event is None:
            pass
        player1_desc.configure(text=name_to_desc[player1_selection.get()])
        player2_desc.configure(text=name_to_desc[player2_selection.get()])

        for strategy in strategies_1:
            if player1_selection.get() == strategy.name:
                player1.strategy = strategy.__copy__()
            if player2_selection.get() == strategy.name:
                player2.strategy = strategy.__copy__()

    # draw left dropdown menu
    player1_menu = ttk.Combobox(dropdown_frame, textvariable=player1_selection,
                                values=strategy_names, state='readonly')
    player1_menu.bind('<<ComboboxSelected>>', change_strategy)
    player1_menu.grid(row=1, column=1)

    # draw right dropdown menu
    player2_menu = ttk.Combobox(dropdown_frame, textvariable=player2_selection,
                                values=strategy_names_2, state='readonly')
    player2_menu.bind('<<ComboboxSelected>>', change_strategy)
    player2_menu.grid(row=1, column=3)

    # draw the "VS"
    versus_label = Label(dropdown_frame, text='VS.', font='TkHeadingFont:')
    versus_label.grid(row=1, column=2, padx=30)

    # Back button
    back_button = Button(root, text='Back',
                         command=lambda: destroy_and_open(root, draw_main_window))
    back_button.grid(row=6, column=0, padx=5)

    player1 = Player(JesusStrategy(), 1)
    player2 = Player(JesusStrategy(), 2)

    change_strategy()

    # start button
    start_button = Button(root, text='Start!',
                          command=lambda: destroy_and_open(
                              root, lambda: create_and_run_game(
                                  int(num_rounds.get()), player1, player2)), padx=10)

    start_button.grid(row=6, column=2, pady=10)

    root.mainloop()


def process_decision(decisions: dict[int, tuple[bool, bool]]) -> str:
    """Takes in a decision dictionary and outputs the next string to put in the decision log."""
    # Take the latest tuple and process it
    decision_tuple = decisions[len(decisions)]
    player_decision = decision_tuple[0]
    opponent_decision = decision_tuple[1]

    if player_decision is True:
        result = 'You chose to cooperate.'
    else:
        result = 'You chose to betray.'

    if opponent_decision is True:
        result += ' Your opponent chose to cooperate.'
    else:
        result += ' Your opponent chose to betray.'

    return result


def player_vs_ai_interface(game: PDGame, player2: Player) -> None:
    """The interface for a player to play with a strategy AI."""

    root = Tk()
    root.resizable(False, False)
    root.title('Player vs. AI Game')
    player2_name = player2.strategy.name
    title_label = Label(root, text='You vs. ' + player2_name, font='TkHeadingFont:')
    title_label.grid(row=1, column=2, pady=15)

    # interface_frame is high level frame
    interface_frame = Frame(root)
    interface_frame.grid(row=3, column=2)

    decision_log_label = Label(interface_frame, text='Decision Log')
    decision_log_label.grid(row=1, column=1)

    decision_dict = game.decisions

    decisions = StringVar(value=decision_dict)
    decision_log = Listbox(interface_frame, listvariable=decisions, height=20, width=75)
    decision_log.grid(row=2, column=1)

    def make_score_delta(game: PDGame) -> tuple[str, str]:
        """Returns a string tuple of
        (Player1 points gained, Player2 points gained) for the previous round.

        The points gained or loss have a corresponding sign added as a prefix for each string.
        """
        decisions = game.decisions
        latest_decision_tuple = decisions[game.curr_round - 1]
        player1_decision = latest_decision_tuple[0]
        player2_decision = latest_decision_tuple[1]
        int_tuple = resolve_points(player1_decision, player2_decision)
        if int_tuple[0] >= 0:
            str_player1_points = '+' + str(int_tuple[0])
        else:
            str_player1_points = '-' + str(int_tuple[0])

        if int_tuple[1] >= 0:
            str_player2_points = '+' + str(int_tuple[1])
        else:
            str_player2_points = '-' + str(int_tuple[1])

        return (str_player1_points, str_player2_points)

    def victory() -> None:
        """Shows a message box at player victory."""
        messagebox.showinfo('Victory!', 'Victory! \n\nPress OK to go back to the main menu.')
        root.destroy()
        draw_main_window()

    def defeat() -> None:
        """Shows a message box at player defeat."""
        messagebox.showinfo('Defeat!', 'You\'ve been defeated. '
                                       '\n\nPress OK to go back to the main menu.')
        root.destroy()
        draw_main_window()

    def draw() -> None:
        """Shows a message box at a game draw."""
        messagebox.showinfo('Draw!', 'Tie! \n\nPress OK to go back to the main menu.')
        root.destroy()
        draw_main_window()

    def insert_latest_decision(user_decision: bool) -> None:
        """Inserts a string representation of the latest round into the decision log."""

        if int(game.curr_round) < int(game.num_rounds):
            game.decisions[game.curr_round] = (user_decision, player2.strategy.make_move(game))
            decision_log.insert(len(decision_dict), process_decision(game.decisions))
            game.curr_round += 1
            play_round()

        if int(game.curr_round) >= int(game.num_rounds):
            if game.resolve_game(1, 2) == 1:
                victory()
            elif game.resolve_game(1, 2) == 2:
                defeat()
            else:
                draw()

    decision_window = Frame(interface_frame, bd=2)
    decision_window.grid(row=2, column=2)

    make_decision_label = Label(decision_window, text='Make Your Decision!', font='TkHeadingFont:')
    make_decision_label.grid(row=1, column=2)

    cooperate_button = Button(decision_window, text='COOPERATE',
                              command=lambda: insert_latest_decision(True))
    cooperate_button.grid(row=2, column=1, padx=10)

    betray_button = Button(decision_window, text='BETRAY',
                           command=lambda: insert_latest_decision(False))
    betray_button.grid(row=2, column=3, padx=10)

    def play_round() -> None:
        """Updates all UI scores to their latest values."""
        turn_label = Label(decision_window, text='Turn: ' + str(game.curr_round))
        turn_label.grid(row=3, column=2)

        your_score = Label(decision_window)
        opponent_score = Label(decision_window)
        if game.curr_round == 1:
            your_score.configure(text='Your score: 0')
            opponent_score.configure(text='Your opponent\'s score: 0')
        else:
            your_score.configure(text='Your score: ' + str(game.get_points_prev(1)) + ' (' +
                                      make_score_delta(game)[0] + ')')
            opponent_score.configure(text='Your opponent\'s score: ' + str(
                game.get_points_prev(2)) + ' (' + make_score_delta(game)[1] + ')')

        your_score.grid(row=4, column=2)
        opponent_score.grid(row=5, column=2)

    play_round()

    root.mainloop()


def draw_player_vs_ai() -> None:
    """Draws the Player vs. AI interface.
    """
    root = Tk()

    # prevent window from being manually resized as it causes weird behaviour with labels
    root.resizable(False, False)

    root.title('Player vs. AI')

    title_label = Label(root, text='Player vs. AI', font='TkHeadingFont:')

    title_label.grid(row=1, column=2)

    instructions = Label(root, text='Here, you can select a strategy to play against. Good luck!',
                         padx=30)

    instructions.grid(row=2, column=2)

    # input number of rounds
    input_frame = Frame(root)
    input_frame.grid(row=3, column=2)
    instructions2 = Label(input_frame, text='Number of rounds to be played: ')
    instructions2.grid(row=1, column=1)

    num_rounds_possible = [str(x) for x in range(10, 26)]
    num_rounds = StringVar(root)
    num_rounds.set(num_rounds_possible[0])
    input_field = ttk.Combobox(input_frame, textvariable=num_rounds, values=num_rounds_possible,
                               state='readonly')
    input_field.grid(row=2, column=1, pady=10)

    def update_rounds(event=None) -> None:
        """Updates the PDGame num_rounds to the latest version from the dropmenu."""
        if event is None:
            pass
        game.num_rounds = int(num_rounds.get())

    input_field.bind('<<ComboboxSelected>>', update_rounds)

    # dropdown menus

    jesus = get_all_strategies()[0]
    lucifer = get_all_strategies()[1]
    tit_for_tat = get_all_strategies()[2]
    grim = get_all_strategies()[3]
    probability = get_all_strategies()[4]
    moody = get_all_strategies()[5]
    pavlov = get_all_strategies()[6]
    # initialize strategy info

    strategies = [jesus, lucifer, tit_for_tat, grim, probability, moody, pavlov]
    strategy_names = [strategy.name for strategy in strategies]
    name_to_desc = {strategy.name: strategy.desc for strategy in strategies}

    # create dropdown menu frame

    dropdown_frame = Frame(root)
    dropdown_frame.grid(row=5, column=2)

    player2_selection = StringVar(root)

    # set initial menu selection to Jesus
    player2_selection.set(strategy_names[0])

    # set descriptions
    player2_desc = Label(dropdown_frame, text=name_to_desc[player2_selection.get()])
    player2_desc.grid(row=2, column=3, padx=20)

    def change_description(event=None) -> None:
        """Updates the strategy descriptions to their latest state."""
        if event is None:
            pass
        player2_desc.configure(text=name_to_desc[player2_selection.get()])

        for strategy in strategies:
            if player2_selection.get() == strategy.name:
                player2.strategy = strategy.__copy__()

    # draw YOU label
    you_label = Label(dropdown_frame, text='You')
    you_label.grid(row=1, column=1)

    # draw right dropdown menu
    player2_menu = ttk.Combobox(dropdown_frame, textvariable=player2_selection,
                                values=strategy_names, state='readonly')
    player2_menu.bind('<<ComboboxSelected>>', change_description)

    player2_menu.grid(row=1, column=3)

    # draw the "VS"
    versus_label = Label(dropdown_frame, text='VS.', font='TkHeadingFont:')

    versus_label.grid(row=1, column=2, padx=15)

    # Back button
    back_button = Button(root, text='Back',
                         command=lambda: destroy_and_open(root, draw_main_window))

    back_button.grid(row=6, column=0, padx=5)

    game = PDGame(num_rounds.get())
    game.is_p1_turn = False

    # default opponent to JesusStrategy
    player2 = Player(JesusStrategy(), 2)

    # start button
    start_button = Button(root, text='Start!',
                          command=lambda: destroy_and_open(
                              root, lambda: player_vs_ai_interface(game, player2)),
                          padx=10, pady=0)
    start_button.grid(row=6, column=2, pady=10)

    root.mainloop()


def draw_battle_royale() -> None:
    """Draws the tournament interface."""
    root = Tk()

    # prevent window from being manually resized as it causes weird behaviour with labels
    root.resizable(False, False)

    root.title('AI Battle Royale')

    title_label = Label(root, text='AI Battle Royale', font='TkHeadingFont:')

    title_label.grid(row=1, column=2)

    instructions = Label(root, text='Here, you get to witness the various strategies '
                                    'face off against one another!', padx=30)

    instructions.grid(row=2, column=2)

    # input number of rounds
    input_frame = Frame(root)
    input_frame.grid(row=3, column=2)
    instructions2 = Label(input_frame, text='Number of rounds to be played: ')
    instructions2.grid(row=1, column=1)

    num_rounds_possible = [str(x) for x in range(10, 26)]
    num_rounds = StringVar(root)
    num_rounds.set(num_rounds_possible[0])
    input_field = ttk.Combobox(input_frame, textvariable=num_rounds, values=num_rounds_possible,
                               state='readonly')
    input_field.grid(row=2, column=1, pady=10)

    game = PDGame(int(num_rounds.get()))
    game.is_p1_turn = False

    def game_update_num_rounds(event=None) -> None:
        """Updates game.num_rounds to its latest value inputted by the user."""
        if event is None:
            pass
        game.num_rounds = int(num_rounds.get())

    input_field.bind('<<ComboboxSelected>>', game_update_num_rounds)

    # Back button
    back_button = Button(root, text='Back',
                         command=lambda: destroy_and_open(root, draw_main_window))

    back_button.grid(row=6, column=0, padx=5)

    # start button
    start_button = Button(root, text='Start!',
                          command=lambda: battle_royale_summary_screen(game), padx=10, pady=0)
    start_button.grid(row=6, column=2, pady=10)

    root.mainloop()


def ai_vs_ai_summary_screen(game: PDGame, player1: Player, player2: Player) -> None:
    """Displays the summary of the aftermath of an AI vs AI game.
    """
    root = Tk()

    strategy_1 = player1.strategy.name
    strategy_2 = player2.strategy.name

    root.resizable(False, False)
    root.title('AI vs. AI Summary')
    title_label = Label(root, text=strategy_1 + ' vs. ' + strategy_2 + ' AI Game Summary',
                        font='TkHeadingFont:')
    title_label.grid(row=1, column=2, pady=15)

    # interface_frame is high level frame
    interface_frame = Frame(root)
    interface_frame.grid(row=3, column=2)

    match_summary_label = Label(interface_frame, text='Match Summary')
    match_summary_label.grid(row=1, column=1)

    statistics = ['Starting game...', 'Finishing...', 'Reporting outcomes...',
                  'Played a total of ' + str(game.num_rounds) + ' rounds.']

    winner = game.resolve_game(1, 2)

    player1_points = game.get_points_prev(1)
    player2_points = game.get_points_prev(2)

    statistics.append('Player 1 (' + str(strategy_1) + ') got: ' + str(player1_points) + ' points.')
    statistics.append('Player 2 (' + str(strategy_2) + ') got: ' + str(player2_points) + ' points.')

    if winner == 1:
        statistics.append('Player 1 won.')
    elif winner == 2:
        statistics.append('Player 2 won.')
    else:
        statistics.append('Both players tied.')

    # stats_so_far = StringVar(value=statistics)
    match_summary_log = Listbox(interface_frame, height=20, width=75)
    match_summary_log.grid(row=2, column=1)

    def insert_statistics() -> None:
        """Inserts string statistics into the match summary log."""
        for i in range(len(statistics)):
            match_summary_log.insert(i, statistics[i])

    decision_window = Frame(interface_frame, bd=2)
    decision_window.grid(row=2, column=2)

    make_decision_label = Label(decision_window, text='Other Options', font='TkHeadingFont:')
    make_decision_label.grid(row=1, column=2)

    exit_button = Button(decision_window, text='Go Back',
                         command=lambda: destroy_and_open(root, draw_main_window))
    exit_button.grid(row=2, column=2, padx=10)

    insert_statistics()

    root.mainloop()


def battle_royale_summary_screen(game: PDGame) -> None:
    """Displays the summary of the aftermath of a tournament game.
    """
    root = Tk()
    root.resizable(False, False)
    root.title('Battle Royale Summary')
    title_label = Label(root, text='Battle Royale Game Summary', font='TkHeadingFont:')
    title_label.grid(row=1, column=2, pady=15)

    # interface_frame is high level frame
    interface_frame = Frame(root)
    interface_frame.grid(row=3, column=2)

    match_summary_label = Label(interface_frame, text='Log')
    match_summary_label.grid(row=1, column=1)

    statistics = ['Starting game...', 'Finishing...', 'Awaiting user input...']

    # stats_so_far = StringVar(value=statistics)
    match_summary_log = Listbox(interface_frame, height=20, width=75)
    match_summary_log.grid(row=2, column=1)

    def insert_statistics() -> None:
        """Inserts string statistics into the match summary log."""
        for i in range(len(statistics)):
            match_summary_log.insert(i, statistics[i])

    decision_window = Frame(interface_frame, bd=2)
    decision_window.grid(row=2, column=2)

    visualization_label = Label(decision_window, text='Visualization', font='TkHeadingFont:')
    visualization_label.grid(row=1, column=1)

    heatmap_button = Button(decision_window, text='Open Heatmap',
                            command=lambda: run_tournament(game))
    heatmap_button.grid(row=2, column=1, padx=10, pady=15)

    insert_statistics()

    root.mainloop()


if __name__ == '__main__':
    draw_main_window()
