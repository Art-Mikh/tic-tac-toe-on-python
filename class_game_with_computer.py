from class_main_game_logic import MainGameLogic, Label
from class_main_game_logic import GameStatus, PlayerTurn


class GameWithComputer(MainGameLogic):
    def main_logic(self) -> None:
        game: dict = self.game_init()
        while game['game_status'] == GameStatus.сontinues.value:
            game['field_value_fill'] = self.choose_player_move(game)
            game = self.move_search(game)
            game['sign_of_move'] = self.get_player_symbol(game['player_turn'])
            game['player_turn'] = self.change_player_turn(game['player_turn'])
        self.ending_game(game)

    def move_search(self, game: dict) -> dict:
        # 3. Если компьютер нашел куда сделать ход, то играем. Если нет, то ничья.
        found_game_move = dict(game)
        if found_game_move['field_value_fill'] != Label.none.value:
            found_game_move['game_map'] = self.make_move(found_game_move)
            found_game_move['winner'] = self.get_game_result(found_game_move)
            found_game_move['game_status'] = self.check_victory(found_game_move['winner'])
        else:
            found_game_move = self.assign_status_draw(found_game_move)
        return found_game_move

    def check_victory(self, winner: str) -> bool:
        if winner != Label.none.value:
            return GameStatus.finished.value
        else:
            return GameStatus.сontinues.value

    def assign_status_draw(self, game: dict) -> dict:
        game_result: dict = dict(game)
        print('Ничья!')
        game_result['game_status'] = GameStatus.finished.value
        game_result['winner'] = "Ничья"
        return game_result

    def choose_player_move(self, game: dict) -> int:
        if game['player_turn'] == PlayerTurn.player_1.value:
            return self.get_input_from_user(game)
        else:
            print("Компьютер делает ход: ")
            return self.AI_choice_move(game)

    def AI_choice_move(self, game: dict) -> int:
        step: int = Label.none.value
        step = self.complete_your_line(game)
        step = self.block_another_line(game, step)
        step = self.add_second_0(game, step)
        step = self.take_center(game, step)
        step = self.take_first_slot(game, step)
        return step

    def complete_your_line(self, game: dict) -> int:
        return self.check_line(game, 2, 0)

    def block_another_line(self, game: dict, step: int) -> int:
        if step == Label.none.value:
            return self.check_line(game, 0, 2)
        return step

    def add_second_0(self, game: dict, step: int) -> int:
        if step == Label.none.value:
            return self.check_line(game, 1, 0)
        return step

    def take_center(self, game: dict, step: int) -> int:
        if (
            step == Label.none.value and
            game['game_map'][4] != Label.x.value and
            game['game_map'][4] != Label.o.value
        ):
            return 5
        return step

    def take_first_slot(self, game: dict, step: int) -> int:
        if (
            step == Label.none.value and
            game['game_map'][0] != Label.x.value and
            game['game_map'][0] != Label.o.value
        ):
            return 1
        return step

    # Искусственный интеллект: поиск линии с нужным количеством X и O на победных линиях
    def check_line(self, game: dict, sum_X: int, sum_O: int) -> int:
        game_map: list = game['game_map']
        step = Label.none.value
        for line in game['winning_lines']:
            sum_labels: dict = self.find_number_labels(game_map, line)
            step = self.choose_move(game_map, line, sum_labels, sum_X, sum_O, step)
        return step

    def find_number_labels(self, game_map: list, checked_line: list) -> dict:
        sum_labels: dict = self.get_dictionary_sum_labels()
        for j in range(0, 3):
            if game_map[checked_line[j]] == Label.o.value:
                sum_labels['o'] += 1
            if game_map[checked_line[j]] == Label.x.value:
                sum_labels['x'] += 1
        return sum_labels

    def get_dictionary_sum_labels(self) -> dict:
        return {'x': 0, 'o': 0}

    def choose_move(self,
                    game_map: list,
                    checked_line: list,
                    sum_labels: dict,
                    sum_X: int,
                    sum_O: int,
                    step: int) -> int:
        ret_step = step
        if sum_labels['o'] == sum_O and sum_labels['x'] == sum_X:
            for j in range(0, 3):
                if (
                    game_map[checked_line[j]] != Label.o.value
                    and game_map[checked_line[j]] != Label.x.value
                ):
                    ret_step = game_map[checked_line[j]]
        return ret_step
