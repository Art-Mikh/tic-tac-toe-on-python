"""
File containing the class GameWithComputer,
containing methods that implement the game of two people
"""
from class_main_game_logic import MainGameLogic, Label
from class_main_game_logic import GameStatus, PlayerTurn


class GameWithComputer(MainGameLogic):
    """
    The class contains methods that implement the game for two people.
    """
    def main_logic(self) -> None:
        game: dict = self.game_init()
        while game['game_status'] == GameStatus.CNTINUES.value:
            game['field_value_fill'] = self.choose_player_move(game)
            game = self.move_search(game)
            game['sign_of_move'] = self.get_player_symbol(game['player_turn'])
            game['player_turn'] = self.change_player_turn(game['player_turn'])
        self.ending_game(game)

    def move_search(self, game: dict) -> dict:
        """
        Method for finding a move If the computer has found where
        to a move, then we play. If not, then a draw.

        Args:
            game (dict): dictionary with current game statuses

        Returns:
            dict: dictionary with assigned draw values
        """
        found_game_move = dict(game)
        if found_game_move['field_value_fill'] != Label.NONE.value:
            found_game_move['game_map'] = self.make_move(found_game_move)
            found_game_move['winner'] = self.get_game_result(found_game_move)
            found_game_move['game_status'] = self.check_victory(found_game_move['winner'])
        else:
            found_game_move = self.assign_status_draw(found_game_move)
        return found_game_move

    def check_victory(self, winner: str) -> bool:
        """
        Sets the flag for the end
        of the game if a winner is found

        Args:
            winner (str): game winner flag

        Returns:
            bool: Game end flag
        """
        if winner != Label.NONE.value:
            return GameStatus.FINISHED.value
        return GameStatus.CNTINUES.value

    def assign_status_draw(self, game: dict) -> dict:
        """
        Filling in statuses for a draw

        Args:
            game (dict): dictionary with current game statuses

        Returns:
            dict: dictionary with affixed draw statuses
        """
        game_result: dict = dict(game)
        print('Ничья!')
        game_result['game_status'] = GameStatus.FINISHED.value
        game_result['winner'] = "Ничья"
        return game_result

    def choose_player_move(self, game: dict) -> int:
        """
        Changing the player's turn

        Args:
            game (dict): dictionary with current game statuses

        Returns:
            int: the position of the move made by the
                player or the computer
        """
        if game['player_turn'] == PlayerTurn.PLAYER_1.value:
            return self.get_input_from_user(game)
        print("Компьютер делает ход: ")
        return self.ai_choice_move(game)

    def ai_choice_move(self, game: dict) -> int:
        """
        Method that implements AI for choosing a move

        Args:
            game (dict): with current game statuses

        Returns:
            int: found computer move
        """
        step: int = Label.NONE.value
        step = self.complete_your_line(game)
        step = self.block_another_line(game, step)
        step = self.add_second_0(game, step)
        step = self.take_center(game, step)
        step = self.take_first_slot(game, step)
        return step

    def complete_your_line(self, game: dict) -> int:
        """
        Checking for filling inyour line,
        consisting of the same character

        Args:
            game (dict): dictionary with current game statuses

        Returns:
            int: cell number of the occupied field
        """
        return self.check_line(game, 2, 0)

    def block_another_line(self, game: dict, step: int) -> int:
        """
        Blocks someone else's line by placing his
        symbol if there is a line of two enemy symbols

        Args:
            game (dict): with current game statuses
            step (int): Previous move value

        Returns:
            int: cell number of the occupied field
        """
        if step == Label.NONE.value:
            return self.check_line(game, 0, 2)
        return step

    def add_second_0(self, game: dict, step: int) -> int:
        """
        The method appends the second 0

        Args:
            game (dict): dictionary with current game statuses
            step (int): Previous move value

        Returns:
            int: cell number of the occupied field
        """
        if step == Label.NONE.value:
            return self.check_line(game, 1, 0)
        return step

    def take_center(self, game: dict, step: int) -> int:
        """
        Method occupies the center of the field

        Args:
            game (dict): dictionary with current game statuses
            step (int): Previous move value

        Returns:
            int: cell number of the occupied field
        """
        if (
            step == Label.NONE.value and
            game['game_map'][4] != Label.X.value and
            game['game_map'][4] != Label.O.value
        ):
            return 5
        return step

    def take_first_slot(self, game: dict, step: int) -> int:
        """
        first cell method

        Args:
            game (dict): dictionary with current game statuses
            step (int): Previous move value

        Returns:
            int: cell number of the occupied field
        """
        if (
            step == Label.NONE.value and
            game['game_map'][0] != Label.X.value and
            game['game_map'][0] != Label.O.value
        ):
            return 1
        return step

    def check_line(self, game: dict, sum_x: int, sum_o: int) -> int:
        """
        Method for finding a line with the right amount of X and O on winning lines

        Args:
            game (dict): dictionary with current game statuses
            sum_x (int): quantity X
            sum_o (int): quantity 0

        Returns:
            int: returns the computer's progress
        """
        game_map: list = game['game_map']
        step = Label.NONE.value
        for line in game['winning_lines']:
            sum_labels: dict = self.find_number_labels(game_map, line)
            choose_list = self.create_dictionary_for_move_selection(game_map, line, sum_labels)
            step = self.choose_move(choose_list, sum_x, sum_o, step)
        return step

    def find_number_labels(self, game_map: list, checked_line: list) -> dict:
        """
        The method counts the number of X's and 0's in the field line

        Args:
            game_map (list): current playing field
            checked_line (list): tested line

        Returns:
            dict: dictionary with counted number of x's and 0's
        """
        sum_labels: dict = self.get_dictionary_sum_labels()
        for j in range(0, 3):
            if game_map[checked_line[j]] == Label.O.value:
                sum_labels['o'] += 1
            if game_map[checked_line[j]] == Label.X.value:
                sum_labels['x'] += 1
        return sum_labels

    def get_dictionary_sum_labels(self) -> dict:
        """
        Returns a dictionary to count the number of x and 0

        Returns:
            dict: dictionary to count the number of x's and 0's
        """
        return {'x': 0, 'o': 0}

    def create_dictionary_for_move_selection(
        self, game_map: list, checked_line: list, sum_labels: dict
    ) -> list:
        """
        The method creates a list to reduce the number of containers

        Args:
            game_map (list): current game map
            checked_line (list): tested line
            sum_labels (dict): dictionary sum of x and 0

        Returns:
            list: list to reduce the number of parameters
        """
        return [game_map, checked_line, sum_labels]

    def choose_move(self,
                    choose_list: list,
                    sum_x: int,
                    sum_o: int,
                    step: int) -> int:
        """
        Method selects the computer's move

        Args:
            choose_list (list): contains parameters:
                game_map: list
                checked_line: list
                sum_labels: dict
            sum_x (int): quantity X
            sum_o (int): quantity o
            step (int):

        Returns:
            int: found computer move
        """
        game_map: list = choose_list[0]
        checked_line: list = choose_list[1]
        sum_labels: dict = choose_list[2]
        ret_step = step
        if sum_labels['o'] == sum_o and sum_labels['x'] == sum_x:
            for j in range(0, 3):
                if (
                    game_map[checked_line[j]] != Label.O.value
                    and game_map[checked_line[j]] != Label.X.value
                ):
                    ret_step = game_map[checked_line[j]]
        return ret_step
