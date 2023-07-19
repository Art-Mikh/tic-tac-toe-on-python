'''
File containing the class TwoPlayers for playing together
'''
from class_main_game_logic import MainGameLogic, Label, GameStatus


class TwoPlayers(MainGameLogic):
    """
    Class responsible for the game of two players

    Args:
        MainGameLogic: Abstract class
            with the main logic of the game tic-tac-toe
    """

    def main_logic(self) -> None:
        game: dict = self.game_init()
        while game['game_status'] == GameStatus.CNTINUES.value:
            game['field_value_fill'] = self.get_input_from_user(game)
            game['game_map'] = self.make_move(game)
            game['winner'] = self.get_game_result(game)
            game['game_status'] = self.win_check(game['winner'])
            game['sign_of_move'] = self.get_player_symbol(game['player_turn'])
            game['player_turn'] = self.change_player_turn(game['player_turn'])
            game = self.check_for_draw(game)
        self.ending_game(game)

    def check_for_draw(self, game: dict) -> dict:
        """
        Method for checking the game for a draw

        Args:
            game (dict): dictionary with current game statuses

        Returns:
            dict: returns a dictionary with the completed
                game end marker
        """
        amount_filled_cells: int = self.get_number_filled_cells(game['game_map'])
        return self.fill_in_draw_fields(game, amount_filled_cells)

    def get_number_filled_cells(self, game_map: list) -> int:
        """
        Returns the number of cells filled by the players

        Args:
            game_map (list): dictionary with current game statuses

        Returns:
            int: the number of cells filled by players
        """
        amount_filled_cells: int = 0
        for cell in game_map:
            if cell in (Label.X.value, Label.O.value):
                amount_filled_cells += 1
        return amount_filled_cells

    def fill_in_draw_fields(
            self,
            game: dict,
            amount_filled_cells: int) -> dict:
        """
        returns a dictionary with filled
        flags to display "draw" status

        Args:
            game (dict): dictionary with current game statuses
            amount_filled_cells (int): the number
                of cells filled by players

        Returns:
            dict: dictionary with completed draw statuses
        """
        ret_game: dict = game
        if (
            amount_filled_cells == 9 and
            ret_game['game_status'] == GameStatus.CNTINUES.value
        ):
            print("Ничья!")
            ret_game['game_status'] = GameStatus.FINISHED.value
            ret_game['winner'] = "Ничья"
        return ret_game

    def win_check(self, winner: str) -> bool:
        """
        Checks if the flag of the winner is filled.
        If the winner is determined, we return
        the flag of the end of the game

        Args:
            winner (str): game winner flag

        Returns:
            bool: Game end flag
        """
        if winner != Label.NONE.value:
            return GameStatus.FINISHED.value
        return GameStatus.CNTINUES.value
