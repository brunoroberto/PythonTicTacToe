#!/usr/bin/python


class Player:

    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

    def __eq__(self, other):
        return self.symbol == other.symbol

    def get_move(self):
        print(f'\n{self.name}\'s turn! Symbol: {self.symbol}')

        is_valid_input = False
        while not is_valid_input:
            row = int(input('Row number (1 to 3): '))
            is_valid_input = 1 <= row <= 3

        is_valid_input = False
        while not is_valid_input:
            col = int(input('Column number (1 to 3): '))
            is_valid_input = 1 <= col <= 3

        return row - 1, col - 1


class Board:

    def __init__(self):
        self.remaining_positions = 9
        self.board = [
            [' ', ' ', ' '],
            [' ', ' ', ' '],
            [' ', ' ', ' ']
        ]

    def print_board(self):
        print('\nBoard:')
        print('\n  1    2    3')
        board_size = len(self.board)
        for row in range(0, board_size):
            print(f'{row + 1} {self.board[row][0]}    {self.board[row][1]}    {self.board[row][2]}')

    def is_position_valid(self, row, col):
        return self.board[row][col] == ' '

    def is_board_full(self):
        return self.remaining_positions == 0

    def make_move(self, row, col, player):
        self.board[row][col] = player.symbol
        self.remaining_positions -= 1

    def check_winner(self, player):
        lines = self.__check_lines(player)
        columns = self.__check_columns(player)
        diagonals = self.__check_diagonals(player)
        return lines or columns or diagonals

    def __check_lines(self, player):
        board_size = len(self.board)
        for row in range(0, board_size):
            if self.board[row][0] == player.symbol and self.board[row][1] == player.symbol \
                    and self.board[row][2] == player.symbol:
                return True
        return False

    def __check_columns(self, player):
        board_size = len(self.board)
        for col in range(0, board_size):
            if self.board[0][col] == player.symbol and self.board[1][col] == player.symbol \
                    and self.board[2][col] == player.symbol:
                return True
        return False

    def __check_diagonals(self, player):
        primary_diagonal = self.board[0][0] == player.symbol and self.board[1][1] == player.symbol and \
                           self.board[2][2] == player.symbol
        secondary_diagonal = self.board[0][2] == player.symbol and self.board[1][1] == player.symbol and \
                             self.board[2][0] == player.symbol
        return primary_diagonal or secondary_diagonal


class TicTacToe:

    MAX_PLAYERS = 2

    def __init__(self, player_one, player_two):
        self.round = 0
        self.stopped = False
        self.board = Board()
        self.players = [player_one, player_two]

    def __is_winner(self, player):
        if self.round < 5:  # cannot be a winner before 6 rounds
            return False
        return self.board.check_winner(player)

    def start(self):
        while not self.stopped:
            self.board.print_board()
            round_player = self.players[self.round % TicTacToe.MAX_PLAYERS];

            is_valid_position = False
            while not is_valid_position:
                row, col = round_player.get_move()
                is_valid_position = self.board.is_position_valid(row, col)
                if not is_valid_position:
                    print(f'\nInvalid move. Maybe this position already have a value. Please, try again!')

            self.board.make_move(row, col, round_player)
            self.round += 1

            has_winner = self.__is_winner(round_player)
            self.stopped = has_winner or self.board.is_board_full()

        self.board.print_board()

        if not has_winner and self.board.is_board_full():
            print('\nDraw! There is no winner in this match :(')
        else:
            print(f'\nCongratulations, {round_player.name} is the winner!')


def get_player():
    name = input('\nWhat\'s your name?\n')
    symbol = ''
    while symbol not in ('X', 'x', 'O', 'o'):
        symbol = input('Which symbol do you want to play, X or O?\n')
    return Player(name, symbol)


def main():
    player_one = get_player()
    player_two = get_player()

    while player_one == player_two:
        print('You cannot choose the same symbol!')
        player_two = get_player()

    game = TicTacToe(player_one, player_two)
    game.start()


if __name__ == '__main__':
    main()
