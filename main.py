"""CSC111 Winter 2021 Final Project

Copyright (c) 2021 Abdus Shaikh, Jason Wang, Samraj Aneja, Kevin Wang
"""
from tkinter import Tk, Label, Grid, Button, Entry, Frame

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


def draw_main_window():
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

    instructions.grid(row=1, column=2)

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

    ai_v_ai_button = Button(frame, text='AI vs. AI', command=...)
    player_v_ai_button = Button(frame, text='Player vs. AI', command=...)
    battle_royale_button = Button(frame, text='AI Battle Royale', command=...)

    ai_v_ai_button.grid(row=1, column=1, padx=30, pady=20)
    player_v_ai_button.grid(row=1, column=2, padx=30, pady=20)
    battle_royale_button.grid(row=1, column=3, padx=30, pady=20)

    player_v_ai_button.place()
    root.mainloop()


draw_main_window()

