from abc import ABC, abstractmethod
from enum import Enum


class GameStatus(Enum):
    сontinues: bool = True
    finished: bool = False


class PlayerTurn(Enum):
    player_1: bool = True
    player_2: bool = False


class Label(Enum):
    x: str = ("X",)
    o: str = ("0",)
    none: str = ""


class PlayerMoveValidation(Enum):
    correct_value: bool = True
    invalid_value: bool = False


class MainGameLogic(ABC):
    def __init__(self):
        self.main_logic()

    @abstractmethod
    def main_logic(self) -> None:
        pass

    def game_init(self) -> dict:
        return {
            'game_map': self.map_initialization(),
            'winning_lines': self.initialize_winning_positions(),
            'game_status': GameStatus.сontinues.value,
            'player_turn': PlayerTurn.player_1.value,
            'sign_of_move': Label.x.value,
            'winner': '',
            'field_value_fill': ''
        }

    def map_initialization(self) -> list:
        game_map = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        return game_map

    def initialize_winning_positions(self) -> list:
        winning_lines = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6],
        ]
        return winning_lines

    def make_move(self, game: dict) -> list:
        ret_map: list = game['game_map']
        ind = ret_map.index(game['field_value_fill'])
        ret_map[ind] = game['sign_of_move']
        return ret_map

    def get_game_result(self, game: dict) -> str:
        winner: str = Label.none.value
        for line in game['winning_lines']:
            winner = self.check_win(winner, game['game_map'], line)
        return winner

    def check_win(self, winner: str, game_map: list, winning_line: list) -> str:
        winner_symbol: str = winner
        if (
            game_map[winning_line[0]]
            == game_map[winning_line[1]]
            == game_map[winning_line[2]]
            == Label.x.value
        ):
            winner_symbol = Label.x.value
        elif (
            game_map[winning_line[0]]
            == game_map[winning_line[1]]
            == game_map[winning_line[2]]
            == Label.o.value
        ):
            winner_symbol = Label.o.value
        return winner_symbol

    def get_input_from_user(self, game: dict) -> int:
        self.print_map(game['game_map'])
        valid_flag = PlayerMoveValidation.invalid_value.value
        while valid_flag != PlayerMoveValidation.correct_value.value:
            symbol = input("Ход игрока " + game['sign_of_move'][0] + ": ")
            valid_flag = self.check_player_move(symbol, game)
        return int(symbol)

    def check_player_move(self, symbol: str, game: dict) -> bool:
        valid_flag = PlayerMoveValidation.invalid_value.value
        valid_flag = self.number_check(symbol, game)
        return valid_flag

    def number_check(self, symbol: str, game: dict) -> bool:
        if symbol.isdigit():
            numder = int(symbol)
            return self.validating_number_within_field(numder, game)
        else:
            print("Введите номер поля для хода! Введите номер другой ячейки:")
            return PlayerMoveValidation.invalid_value.value

    def validating_number_within_field(self, numder: int, game: dict) -> bool:
        if 0 < numder < 10:
            return self.cell_not_busy(numder, game['game_map'])
        else:
            print("Введите номер поля для хода от 1 до 9!:")
            return PlayerMoveValidation.invalid_value.value

    def cell_not_busy(self, numder: int, game_map: list) -> bool:
        if (
            game_map[numder - 1] != Label.x.value and
            game_map[numder - 1] != Label.o.value
        ):
            return PlayerMoveValidation.correct_value.value
        else:
            print("Эта клетка занята! Введите номер другой ячейки: ")
            return PlayerMoveValidation.invalid_value.value

    def get_player_symbol(self, player_turn: bool) -> str:
        if player_turn == PlayerTurn.player_1.value:
            return Label.o.value
        else:
            return Label.x.value

    def change_player_turn(self, player_turn: bool) -> bool:
        if player_turn == PlayerTurn.player_1.value:
            return PlayerTurn.player_2.value
        else:
            return PlayerTurn.player_1.value

    def ending_game(self, game: dict) -> None:
        self.print_map(game['game_map'])
        print("Победил", self.change_symbol(game['winner']))

    def print_map(self, game_map: list) -> None:
        out_map = self.change_output_map(game_map)
        self.print_first_line_map(out_map)
        self.print_second_line_map(out_map)
        self.print_third_line_map(out_map)

    def change_output_map(self, game_map: list) -> list:
        return [
            self.change_symbol(item)
            for item in game_map
        ]

    def change_symbol(self, symbol: tuple) -> str:
        if symbol == Label.x.value:
            return "X"
        elif symbol == Label.o.value:
            return "0"
        else:
            return symbol

    def print_first_line_map(self, out_map: list) -> None:
        print(out_map[0], end=" ")
        print(out_map[1], end=" ")
        print(out_map[2])

    def print_second_line_map(self, out_map: list) -> None:
        print(out_map[3], end=" ")
        print(out_map[4], end=" ")
        print(out_map[5])

    def print_third_line_map(self, out_map: list) -> None:
        print(out_map[6], end=" ")
        print(out_map[7], end=" ")
        print(out_map[8])
