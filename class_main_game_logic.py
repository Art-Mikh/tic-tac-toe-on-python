"""
The file with the abstract class
MainGameLogic and contains the
main methods of the game tic-tac-toe
"""
from abc import ABC, abstractmethod
from enum import Enum


class GameStatus(Enum):
    """
    Class for storing game status.
    Is the game in progress or over
    """
    CNTINUES: bool = True
    FINISHED: bool = False


class PlayerTurn(Enum):
    """
    class containing the player's turn queue flag
    """
    PLAYER_1: bool = True
    PLAYER_2: bool = False


class Label(Enum):
    """
    Class containing characters to move
    """
    X: str = ("X",)
    O: str = ("0",)
    NONE: str = ""


class PlayerMoveValidation(Enum):
    """
    Class contains markers of correctness of the player's move
    """
    CORRECT_VALUE: bool = True
    INVALID_VALUE: bool = False


class MainGameLogic(ABC):
    """
    The abstract class contains the core
    logic of the tic-tac-toe game
    """
    def __init__(self):
        self.main_logic()

    @abstractmethod
    def main_logic(self) -> None:
        """
        The basic logic of tic-tac-toe.
        This method will be different for
        playing with a computer and for two
        """

    def game_init(self) -> dict:
        """
        Dictionary initialization method
        containing all the start flags
        and labels for the game
        """
        return {
            'game_map': self.map_initialization(),
            'winning_lines': self.initialize_winning_positions(),
            'game_status': GameStatus.CNTINUES.value,
            'player_turn': PlayerTurn.PLAYER_1.value,
            'sign_of_move': Label.X.value,
            'winner': '',
            'field_value_fill': ''
        }

    def map_initialization(self) -> list:
        """
        Method returning an empty playing field
        """
        game_map = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        return game_map

    def initialize_winning_positions(self) -> list:
        """
        Method that returns all possible
        paylines to win the game
        """
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
        """
        The method marks the player's turn on the map

        Args:
            game (dict): dictionary containing all game tags

        Returns:
            list: updated game map with marked moves
        """
        ret_map: list = game['game_map']
        ind = ret_map.index(game['field_value_fill'])
        ret_map[ind] = game['sign_of_move']
        return ret_map

    def get_game_result(self, game: dict) -> str:
        """
        the method returns the winner of
        the game if one of the players won

        Args:
            game (dict): dictionary containing all game tags

        Returns:
            str: game winner player symbol
        """
        winner: str = Label.NONE.value
        for line in game['winning_lines']:
            winner = self.check_win(winner, game['game_map'], line)
        return winner

    def check_win(self, winner: str, game_map: list, winning_line: list) -> str:
        """
        The method checks if a winning
        position has been created on
        one of the winning lines

        Args:
            winner (str): symbol of the winner
            game_map (list): current game map
            winning_line (list): winning line to check

        Returns:
            str: _description_
        """
        winner_symbol: str = winner
        if (
            game_map[winning_line[0]]
            == game_map[winning_line[1]]
            == game_map[winning_line[2]]
            == Label.X.value
        ):
            winner_symbol = Label.X.value
        elif (
            game_map[winning_line[0]]
            == game_map[winning_line[1]]
            == game_map[winning_line[2]]
            == Label.O.value
        ):
            winner_symbol = Label.O.value
        return winner_symbol

    def get_input_from_user(self, game: dict) -> int:
        """
        The method returns the number
        of the cell in which the move was made

        Args:
            game (dict): dictionary containing all game tags

        Returns:
            int: the number of the cell in which the move was made
        """
        self.print_map(game['game_map'])
        valid_flag = PlayerMoveValidation.INVALID_VALUE.value
        while valid_flag != PlayerMoveValidation.CORRECT_VALUE.value:
            symbol = input("Ход игрока " + game['sign_of_move'][0] + ": ")
            valid_flag = self.check_player_move(symbol, game)
        return int(symbol)

    def check_player_move(self, symbol: str, game: dict) -> bool:
        """
        Сhecking the player's move

        Args:
            symbol (str): character entered by the player
            game (dict): dictionary containing all game tags

        Returns:
            bool: flag - the result of checking
                the character entered by the player
        """
        valid_flag = PlayerMoveValidation.INVALID_VALUE.value
        valid_flag = self.number_check(symbol, game)
        return valid_flag

    def number_check(self, symbol: str, game: dict) -> bool:
        """
        the character entered by the player
        is checked for the presence of a number

        Args:
            symbol (str): character entered by the player
            game (dict): dictionary containing all game tags

        Returns:
            bool: flag - the result of checking
                the character entered by the player
        """
        if symbol.isdigit():
            numder = int(symbol)
            return self.validating_number_within_field(numder, game)
        print("Введите номер поля для хода! Введите номер другой ячейки:")
        return PlayerMoveValidation.INVALID_VALUE.value

    def validating_number_within_field(self, numder: int, game: dict) -> bool:
        """
        The method checks if the number
        entered by the player is between 1 and 9

        Args:
            numder (int): character entered by the player
            game (dict): dictionary containing all game tags

        Returns:
            bool: flag - the result of checking
                the character entered by the player
        """
        if 0 < numder < 10:
            return self.cell_not_busy(numder, game['game_map'])
        print("Введите номер поля для хода от 1 до 9!:")
        return PlayerMoveValidation.INVALID_VALUE.value

    def cell_not_busy(self, numder: int, game_map: list) -> bool:
        """
        Checking if a cell is already occupied or not

        Args:
            numder (int): character entered by the player
            game (dict): dictionary containing all game tags

        Returns:
            bool: flag - the result of checking
                the character entered by the player
        """
        if (
            game_map[numder - 1] != Label.X.value and
            game_map[numder - 1] != Label.O.value
        ):
            return PlayerMoveValidation.CORRECT_VALUE.value
        print("Эта клетка занята! Введите номер другой ячейки: ")
        return PlayerMoveValidation.INVALID_VALUE.value

    def get_player_symbol(self, player_turn: bool) -> str:
        """
        Returns the character of the player in his turn

        Args:
            player_turn (bool): player turn flag

        Returns:
            str: player symbol
        """
        if player_turn == PlayerTurn.PLAYER_1.value:
            return Label.O.value
        return Label.X.value

    def change_player_turn(self, player_turn: bool) -> bool:
        """
        Passes the current turn to the next player

        Args:
            player_turn (bool): player turn flag

        Returns:
            bool: next player turn flag
        """
        if player_turn == PlayerTurn.PLAYER_1.value:
            return PlayerTurn.PLAYER_2.value
        return PlayerTurn.PLAYER_1.value

    def ending_game(self, game: dict) -> None:
        """
        The method of displaying information at the end of the game

        Args:
            game (dict): dictionary containing all game tags
        """
        self.print_map(game['game_map'])
        print("Победил", self.change_symbol(game['winner']))

    def print_map(self, game_map: list) -> None:
        """
        Playing field display method

        Args:
            game_map (list): dictionary containing all game tags
        """
        out_map = self.change_output_map(game_map)
        self.print_first_line_map(out_map)
        self.print_second_line_map(out_map)
        self.print_third_line_map(out_map)

    def change_output_map(self, game_map: list) -> list:
        """
        The method changes the playing field
        for pretty output. The method changes
        tuples to string characters

        Args:
            game_map (list): Game card for withdrawal

        Returns:
            list: new map to display on the screen
        """
        return [
            self.change_symbol(item)
            for item in game_map
        ]

    def change_symbol(self, symbol: tuple) -> str:
        """
        Method reverses the player's
        symbol to reverse the player's turn order

        Args:
            symbol (tuple): current game symbol

        Returns:
            str: new game symbol
        """
        if symbol == Label.X.value:
            return "X"
        if symbol == Label.O.value:
            return "0"
        return symbol

    def print_first_line_map(self, out_map: list) -> None:
        """
        Displays the first line of the map

        Args:
            out_map (list): game map
        """
        print(out_map[0], end=" ")
        print(out_map[1], end=" ")
        print(out_map[2])

    def print_second_line_map(self, out_map: list) -> None:
        """
        Displays the second line of the map

        Args:
            out_map (list): game map
        """
        print(out_map[3], end=" ")
        print(out_map[4], end=" ")
        print(out_map[5])

    def print_third_line_map(self, out_map: list) -> None:
        """
        Displays the third line of the map

        Args:
            out_map (list): game map
        """
        print(out_map[6], end=" ")
        print(out_map[7], end=" ")
        print(out_map[8])
