"""
Main game launch file
"""
from enum import Enum
from class_two_players import TwoPlayers
from class_game_with_computer import GameWithComputer


class GameVariants(Enum):
    """
    Enumeration containing options for
    playing with a computer or together
    """
    ONE_PLAYER: str = "1"
    TWO_PLAYER: str = "2"


class GameMenu:
    """
    Class for working with the menu
    for choosing the type of game
    """

    def __init__(self) -> None:
        self.load_game()

    def load_game(self) -> None:
        """
        Method to call the game menu
        """
        game_selection_flag = GameVariants.ONE_PLAYER.value
        while game_selection_flag in (
            GameVariants.ONE_PLAYER.value,
            GameVariants.TWO_PLAYER.value,
        ):
            game_selection_flag = self.enter_number()
            self.start_game(game_selection_flag)

    def enter_number(self) -> str:
        """
        Method to get the game type flag from the player

        Returns:
            str: game mode flag
        """
        return input(
            "Для игры с компьютером введите 1, \n"
            + "для игры вдвоем введите 2, \n"
            + "для выхода из игры нажмите любой другой символ: "
        )

    def start_game(self, game_selection_flag: str) -> None:
        """
        Method to launch the game mode that the user has selected

        Args:
            game_selection_flag (str): game mode selection flag
        """
        if game_selection_flag == GameVariants.ONE_PLAYER.value:
            GameWithComputer()
        elif game_selection_flag == GameVariants.TWO_PLAYER.value:
            TwoPlayers()


GameMenu()
