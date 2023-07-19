from class_two_players import TwoPlayers
from class_game_with_computer import GameWithComputer
from enum import Enum


class GameVariants(Enum):
    one_player: str = "1"
    two_player: str = "2"


class GameMenu:
    def __init__(self) -> None:
        self.load_game()

    def load_game(self) -> None:
        game_selection_flag = GameVariants.one_player.value
        while game_selection_flag in (
            GameVariants.one_player.value,
            GameVariants.two_player.value,
        ):
            game_selection_flag = self.enter_number()
            self.start_game(game_selection_flag)

    def enter_number(self) -> str:
        print(
            "Для игры с компьютером введите 1,"
            + " для игры вдвоем введите 2, "
            + "для выхода из игры нажмите любой другой символ:"
        )
        return input()

    def start_game(self, game_selection_flag: str) -> None:
        if game_selection_flag == GameVariants.one_player.value:
            GameWithComputer()
        elif game_selection_flag == GameVariants.two_player.value:
            TwoPlayers()


GameMenu()
