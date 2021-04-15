"""CSC111 Winter 2021 Final Project

Copyright (c) 2021 Abdus Shaikh, Jason Wang, Samraj Aneja, Kevin Wang
"""
from pd_strategy import JesusStrategy, LuciferStrategy, TitForTatStrategy, GrimStrategy, \
    ProbabilityStrategy, MoodyStrategy, PavlovStrategy
from tkinter import Tk, Label, Button, Entry, Frame, OptionMenu, StringVar, ttk, Listbox
from typing import Callable

# TODO: ADD LEARNING AI TO LIST OF STRATEGIES TO BE CHOSEN IN AI vs. AI
# Perhaps only allow LearningStrategy to be chosen for Player 1


class Main:
    """Main runner for Prisoner's Dilemma.
    """

    def run_game(self) -> None:
        """Run a game between two computer strategies.
        """
        # TODO: implement this function

    def run_user_game(self) -> None:
        """Run a game between a user and a computer strategy.
        """
        # TODO: implement this function

    def run_tournament(self, show_heatmap: bool) -> None:
        """Run a tournament between all strategies.

        If <show_heatmap> is set, then display a heatmap that shows the match-ups
        between the strategies.
        """
        # TODO: implement this function

    def resolve_round(self, decision1: bool, decision2: bool) -> None:
        """Takes Player 1's decision and Player 2's decision, determines
        each player's points gained or lost, and mutates each Player's
        curr_points to reflect it.
        """
        # TODO: implement this function


def draw_main_window() -> None:
    """Draws the starting menu for the user.
    Execute this function on startup of this module.
    """
    root = Tk()
    root.title('Prisoner\'s Dilemma')
    # root.geometry('1280x720')

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


def destroy_and_open(window: Tk, function: Callable) -> None:
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

    num_rounds_possible = [str(x) for x in range(10, 100)]
    num_rounds = StringVar(root)
    num_rounds.set(num_rounds_possible[0])
    input_field = ttk.Combobox(input_frame, textvariable=num_rounds, values=num_rounds_possible,
                               state='readonly')
    input_field.grid(row=2, column=1, pady=10)

    # Matchup label

    matchup_label = Label(root, text='Matchup: ')
    matchup_label.grid(row=4, column=2, pady=15)

    # dropdown menus
    jesus = JesusStrategy()
    lucifer = LuciferStrategy()
    tit_for_tat = TitForTatStrategy()
    grim = GrimStrategy()
    probability = ProbabilityStrategy(0.0)
    moody = MoodyStrategy(0)
    pavlov = PavlovStrategy()

    # initialize strategy info

    strategies = [jesus, lucifer, tit_for_tat, grim, probability, moody, pavlov]
    strategy_names = [strategy.name for strategy in strategies]
    name_to_desc = {strategy.name: strategy.desc for strategy in strategies}

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

    def change_description(event=None) -> None:
        """Updates the strategy descriptions to their latest state."""
        player1_desc.configure(text=name_to_desc[player1_selection.get()])
        player2_desc.configure(text=name_to_desc[player2_selection.get()])

    # draw left dropdown menu

    player1_menu = ttk.Combobox(dropdown_frame, textvariable=player1_selection,
                                values=strategy_names, state='readonly')
    player1_menu.bind('<<ComboboxSelected>>', change_description)

    player1_menu.grid(row=1, column=1)

    # draw right dropdown menu

    player2_menu = ttk.Combobox(dropdown_frame, textvariable=player2_selection,
                                values=strategy_names, state='readonly')
    player2_menu.bind('<<ComboboxSelected>>', change_description)

    player2_menu.grid(row=1, column=3)

    # draw the "VS"
    versus_label = Label(dropdown_frame, text='VS.', font='TkHeadingFont:')

    versus_label.grid(row=1, column=2, padx=30)

    # Back button
    back_button = Button(root, text='Back',
                         command=lambda: destroy_and_open(root, draw_main_window))

    back_button.grid(row=6, column=0, padx=5)

    # start button
    # TODO: FILL IN COMMAND TO SET STRATEGIES AND CALL A RUNNER
    # For example, use player1_selection and player2_selection to find which Strategy each chose,
    # and num_rounds
    start_button = Button(root, text='Start!', command=..., padx=10, pady=0)
    start_button.grid(row=6, column=2, pady=10)

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

    num_rounds_possible = [str(x) for x in range(10, 100)]
    num_rounds = StringVar(root)
    num_rounds.set(num_rounds_possible[0])
    input_field = ttk.Combobox(input_frame, textvariable=num_rounds, values=num_rounds_possible,
                               state='readonly')
    input_field.grid(row=2, column=1, pady=10)

    # dropdown menus

    jesus = JesusStrategy()
    lucifer = LuciferStrategy()
    tit_for_tat = TitForTatStrategy()
    grim = GrimStrategy()
    probability = ProbabilityStrategy(0.0)
    moody = MoodyStrategy(0)
    pavlov = PavlovStrategy()

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
        player2_desc.configure(text=name_to_desc[player2_selection.get()])

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

    # start button
    # TODO: FILL IN COMMAND TO SET STRATEGIES AND CALL A RUNNER
    # For example, use player1_selection and player2_selection to find which Strategy each chose
    # and num_rounds
    start_button = Button(root, text='Start!',
                          command=lambda: destroy_and_open(root, player_vs_ai_interface),
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

    num_rounds_possible = [str(x) for x in range(10, 100)]
    num_rounds = StringVar(root)
    num_rounds.set(num_rounds_possible[0])
    input_field = ttk.Combobox(input_frame, textvariable=num_rounds, values=num_rounds_possible,
                               state='readonly')
    input_field.grid(row=2, column=1, pady=10)

    # Back button
    back_button = Button(root, text='Back',
                         command=lambda: destroy_and_open(root, draw_main_window))

    back_button.grid(row=6, column=0, padx=5)

    # start button
    # TODO: FILL IN COMMAND TO SET STRATEGIES AND CALL A RUNNER
    start_button = Button(root, text='Start!', command=..., padx=10, pady=0)
    start_button.grid(row=6, column=2, pady=10)

    root.mainloop()


def player_vs_ai_interface() -> None:
    """The interface for a player to play with a strategy AI."""

    root = Tk()
    root.resizable(False, False)
    root.title('Player vs. AI Game')
    title_label = Label(root, text='Player vs. AI', font='TkHeadingFont:')
    title_label.grid(row=1, column=2, pady=15)

    interface_frame = Frame(root)
    interface_frame.grid(row=3, column=2)

    decision_log_label = Label(interface_frame, text='Decision Log')
    decision_log_label.grid(row=1, column=1)



    decision_list = [str(x + 999999999999999999999999999999999999999999999999) for x in range(100)]
    decisions = StringVar(value=decision_list)
    decision_log = Listbox(interface_frame, listvariable=decisions, height=20, width=50)
    decision_log.grid(row=2, column=1)

    decision_window = Frame(interface_frame, bd=2)
    decision_window.grid(row=2, column=2)

    make_decision_label = Label(decision_window, text='Make Your Decision!', font='TkHeadingFont:')
    make_decision_label.grid(row=1, column=2)

    cooperate_button = Button(decision_window, text='COOPERATE')
    cooperate_button.grid(row=2, column=1, padx=10)

    betray_button = Button(decision_window, text='BETRAY')
    betray_button.grid(row=2, column=3, padx=10)

    turn_label = Label(decision_window, text='Turn: ' + '1')
    turn_label.grid(row=3, column=2)

    your_score = Label(decision_window, text='Your score: ' + '1')
    your_score.grid(row=4, column=2)

    opponent_score = Label(decision_window, text='Your opponent\'s score: ' + '1')
    opponent_score.grid(row=5, column=2)

    root.mainloop()




draw_main_window()
