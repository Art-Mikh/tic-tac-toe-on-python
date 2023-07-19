from class_main_game_logic import MainGameLogic, Label, GameStatus


class TwoPlayers(MainGameLogic):
    def main_logic(self) -> None:
        game: dict = self.game_init()
        while game['game_status'] == GameStatus.сontinues.value:
            game['field_value_fill'] = self.get_input_from_user(game)
            game['game_map'] = self.make_move(game)
            game['winner'] = self.get_game_result(game)
            game['game_status'] = self.win_check(game['winner'])
            game['sign_of_move'] = self.get_player_symbol(game['player_turn'])
            game['player_turn'] = self.change_player_turn(game['player_turn'])
            game = self.check_for_draw(game)
        self.ending_game(game)

    def check_for_draw(self, game: dict) -> dict:
        amount_filled_cells: int = self.get_number_filled_cells(game['game_map'])
        return self.fill_in_draw_fields(game, amount_filled_cells)

    def get_number_filled_cells(self, game_map: list) -> int:
        amount_filled_cells: int = 0
        for cell in game_map:
            if cell in (Label.x.value, Label.o.value):
                amount_filled_cells += 1
        return amount_filled_cells

    def fill_in_draw_fields(
            self,
            game: dict,
            amount_filled_cells: int) -> dict:
        ret_game: dict = game
        if (
            amount_filled_cells == 9 and
            ret_game['game_status'] == GameStatus.сontinues.value
        ):
            print("Ничья!")
            ret_game['game_status'] = GameStatus.finished.value
            ret_game['winner'] = "Ничья"
        return ret_game

    def win_check(self, win: str) -> bool:
        if win != Label.none.value:
            return GameStatus.finished.value
        else:
            return GameStatus.сontinues.value
