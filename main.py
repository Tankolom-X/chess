from Board import Board
from Helper import print_board, BLACK, WHITE


def main():
    board = Board()
    while True:
        print_board(board)
        print('Команды:')
        print('    exit                               -- выход')
        print('    move <row> <col> <row1> <row1>     -- ход из клетки (row, col)')
        print('                                          в клетку (row1, col1)')
        print('    castling0                          -- рокировка в длинную сторону')
        print('    castling7                          -- рокировка в короткую сторону')
        print('    promote pawn <row> <col>           -- ход пешки из клетки (row, col) ')
        print('    <row1> <col1> <new_char>              в клетку (row1, col1)')
        print('                                          с превращением в фигуру символом <new_char>')

        if board.current_player_color() == WHITE:
            print('Ход белых:')
        else:
            print('Ход чёрных:')
        command = input()

        if command == 'exit':
            break
        elif command.split()[0] == 'castling0':
            if board.check(board.current_player_color()):
                print('Вам шах. Сделайте другой ход')
            else:
                if board.castling0():
                    print('Ход успешен')
                else:
                    print('Рокировка невозможна! Попробуйте другой ход!')

        elif command.split()[0] == 'castling7':
            if board.check(board.current_player_color()):
                print('Вам шах. Сделайте другой ход')
            else:
                if board.castling7():
                    print('Ход успешен')
                else:
                    print('Рокировка невозможна! Попробуйте другой ход!')

        elif command.split()[0] + ' ' + command.split()[1] == 'promote pawn':
            move_type1, move_type2, row, col, row1, col1, new_char = command.split()
            row, col, row1, col1 = int(row), int(col), int(row1), int(col1)
            piece1 = board.field[row][col]
            piece2 = board.field[row1][col1]
            if board.move_and_promote_pawn(row, col, row1, col1, new_char):
                if not board.check(1 if board.current_player_color() == 2 else 2):
                    print('Ход успешен')
                else:
                    print('Вам шах. Сделайте другой ход')
                    board.field[row][col] = piece1
                    board.field[row1][col1] = piece2
                    board.color = 1 if board.current_player_color() == 2 else 2
            else:
                print('Координаты некорректны! Попробуйте другой ход!')
        elif command.split()[0] == 'move':

            move_type, row, col, row1, col1 = command.split()
            row, col, row1, col1 = int(row), int(col), int(row1), int(col1)
            piece1 = board.get_piece(row, col)
            piece2 = board.get_piece(row1, col1)

            if board.move_piece(row, col, row1, col1):
                if not board.check(1 if board.current_player_color() == 2 else 2):
                    print('Ход успешен')
                else:
                    print('Вам шах. Сделайте другой ход')
                    board.field[row][col] = piece1
                    board.field[row1][col1] = piece2
                    board.color = 1 if board.current_player_color() == 2 else 2
            else:
                print('Координаты некорректны! Попробуйте другой ход!')

        else:
            print('Команда некорректна')


if __name__ == '__main__':
    main()
