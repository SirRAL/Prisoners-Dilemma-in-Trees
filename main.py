"""CSC111 Winter 2021 Final Project

Copyright (c) 2021 Abdus Shaikh, Jason Wang, Samraj Aneja, Kevin Wang
"""
from pd_strategy import JesusStrategy, LuciferStrategy, TitForTatStrategy, GrimStrategy, \
    ProbabilityStrategy, MoodyStrategy, PavlovStrategy
from tkinter import Tk, Label, Button, Entry, Frame, OptionMenu, StringVar, ttk
from typing import Callable

# TODO: ADD LEARNING AI TO LIST OF STRATEGIES TO BE CHOSEN IN AI vs. AI


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
    # root.geometry('640x480')

    title_label = Label(root, text='Prisoner\'s Dilemma', font='TkHeadingFont:')

    title_label.grid(row=0, column=2)

    frame = Frame(root)

    frame.grid(row=4, column=2)

    instructions = Label(root, text='Welcome to Prisoner\'s Dilemma, a classic experiment '
                                    'in game theory that investigates how perfectly rational '
                                    'decisions can lead to overall loss.')

    instructions.grid(row=1, column=2, padx=30)

    instructions1 = Label(root, text='\n The rules are simple: \n You and your opponent take turns '
                                     'choosing in secret to either cooperate or betray. '
                                     '\n If both of you choose to cooperate, you both '
                                     'benefit and gain points. \n If one of you cooperates '
                                     'and the other betrays, then the cooperator loses '
                                     'points while the betrayer gains points. \n If both of you '
                                     'betray each other, then everyone gets no points!')

    instructions1.grid(row=2, column=2)

    instructions2 = Label(root, text='Here, you can see how a learning AI performs '
                                     'against several predetermined AI archetypes. \n You can also '
                                     'test your wits and face off against one of the archetypes! '
                                     '\n Good luck! \n')

    instructions2.grid(row=3, column=2)

    ai_v_ai_button = Button(frame, text='AI vs. AI',
                            command=lambda: destroy_and_open(root, draw_ai_v_ai))
    player_v_ai_button = Button(frame, text='Player vs. AI', command=...)
    battle_royale_button = Button(frame, text='AI Battle Royale', command=...)

    ai_v_ai_button.grid(row=1, column=1, padx=30, pady=20)
    player_v_ai_button.grid(row=1, column=2, padx=30, pady=20)
    battle_royale_button.grid(row=1, column=3, padx=30, pady=20)

    player_v_ai_button.place()
    root.mainloop()


def destroy_and_open(window: Tk, function: Callable) -> None:
    """Destroys window and calls function."""
    window.destroy()
    function()


def draw_ai_v_ai() -> None:
    """Draws the AI vs. AI window."""
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
    input_field = ttk.Combobox(input_frame, textvariable=num_rounds, values=num_rounds_possible)
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
    player1_menu = OptionMenu(dropdown_frame, player1_selection, *strategy_names,
                              command=change_description)

    player1_menu.grid(row=1, column=1)

    # draw right dropdown menu
    player2_menu = OptionMenu(dropdown_frame, player2_selection, *strategy_names,
                              command=change_description)

    player2_menu.grid(row=1, column=3)

    # draw the "VS"
    versus_label = Label(dropdown_frame, text='VS.')

    versus_label.grid(row=1, column=2, padx=30)

    # Back button
    back_button = Button(root, text='Back',
                         command=lambda: destroy_and_open(root, draw_main_window))

    back_button.grid(row=6, column=0)

    # start button
    # TODO: FILL IN COMMAND TO SET STRATEGIES AND CALL A RUNNER
    # For example, use player1_selection and player2_selection to find which Strategy each chose
    start_button = Button(root, text='Start!', command=..., padx=10, pady=0)
    start_button.grid(row=6, column=2, pady=10)

    root.mainloop()


draw_main_window()
