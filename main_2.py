WHITE = 1
BLACK = 2


# Удобная функция для вычисления цвета противника
def opponent(color):
    if color == WHITE:
        return BLACK
    else:
        return WHITE


def print_board(board):  # Распечатать доску в текстовом виде (см. скриншот)
    print('     +----+----+----+----+----+----+----+----+')
    for row in range(7, -1, -1):
        print(' ', row, end='  ')
        for col in range(8):
            print('|', board.cell(row, col), end=' ')
        print('|')
        print('     +----+----+----+----+----+----+----+----+')
    print(end='        ')
    for col in range(8):
        print(col, end='    ')
    print()


def main():
    # Создаём шахматную доску
    board = Board()
    # Цикл ввода команд игроков
    while True:
        # Выводим положение фигур на доске
        print_board(board)
        # Подсказка по командам
        print('Команды:')
        print('    exit                               -- выход')
        print('    move <row> <col> <row1> <row1>     -- ход из клетки (row, col)')
        print('                                          в клетку (row1, col1)')
        print('    castling0                          -- рокировка в длинную сторону')
        print('    castling7                          -- рокировка в короткую сторону')
        print('    move_and_promote_pawn <row> <col>  -- ход пешки из клетки (row, col) ')
        print('    <row1> <col1> <new_char>              в клетку (row1, col1)')
        print('                                          с превращением в фигуру символом <new_char>')
        # Выводим приглашение игроку нужного цвета
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
        elif command.split()[0] == 'move_and_promote_pawn':
            move_type, row, col, row1, col1, new_char = command.split()
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


def correct_coords(row, col):
    return 0 <= row < 8 and 0 <= col < 8


class Board:
    def __init__(self):
        self.color = WHITE
        self.field = []
        for row in range(8):
            self.field.append([None] * 8)
        self.field[0] = [
            Rook(WHITE), Knight(WHITE), Bishop(WHITE), Queen(WHITE),
            King(WHITE), Bishop(WHITE), Knight(WHITE), Rook(WHITE)
        ]
        self.field[1] = [
            Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE),
            Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE)
        ]
        self.field[6] = [
            Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK),
            Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK)
        ]
        self.field[7] = [
            Rook(BLACK), Knight(BLACK), Bishop(BLACK), Queen(BLACK),
            King(BLACK), Bishop(BLACK), Knight(BLACK), Rook(BLACK)
        ]

    def current_player_color(self):
        return self.color

    def cell(self, row, col):
        '''Возвращает строку из двух символов. Если в клетке (row, col)
        находится фигура, символы цвета и фигуры. Если клетка пуста,
        то два пробела.'''
        piece = self.field[row][col]
        if piece is None:
            return '  '
        color = piece.get_color()
        c = 'w' if color == WHITE else 'b'
        return c + piece.char()

    def get_piece(self, row, col):
        if correct_coords(row, col):
            return self.field[row][col]
        else:
            return None

    def move_piece(self, row, col, row1, col1):
        if not correct_coords(row, col) or not correct_coords(row1, col1):
            return False
        if row == row1 and col == col1:
            return False  # нельзя пойти в ту же клетку
        piece = self.field[row][col]
        if piece is None:
            return False
        if piece.get_color() != self.color:
            return False
        if self.field[row1][col1] is None:
            if not piece.can_move(self, row, col, row1, col1):
                return False
        elif self.field[row1][col1].get_color() == opponent(piece.get_color()):
            if not piece.can_attack(self, row, col, row1, col1):
                return False
        else:
            return False
        self.field[row][col] = None  # Снять фигуру.
        self.field[row1][col1] = piece  # Поставить на новое место.
        if type(self.field[row1][col1]) == King or type(self.field[row1][col1]) == Rook:
            self.field[row1][col1].was_moved()
        self.color = opponent(self.color)
        return True

    def move_and_promote_pawn(self, row, col, row1, col1, new_char):
        if new_char not in ('Q', 'R', 'N', 'B'):
            return False
        piece = self.field[row][col]
        if (piece is None) or (piece.char() != 'P'):
            return False
        if piece.get_color() == WHITE and row1 != 7:
            return False
        if piece.get_color() == BLACK and row1 != 0:
            return False
        if self.move_piece(row, col, row1, col1):
            if new_char == 'Q':
                self.field[row1][col1] = Queen(piece.get_color())
            elif new_char == 'R':
                self.field[row1][col1] = Rook(piece.get_color())
            elif new_char == 'N':
                self.field[row1][col1] = Knight(piece.get_color())
            elif new_char == 'B':
                self.field[row1][col1] = Bishop(piece.get_color())
            return True
        return False

    def cell_is_under_attack(self, row1, col1, color):
        for row in range(8):
            for col in range(8):
                piece = self.field[row][col]
                if (piece is not None) and piece.get_color() != color:
                    if type(piece) is King:
                        continue
                    if piece.can_attack(self, row, col, row1, col1):
                        return True
        else:
            return False

    def castling0(self):
        if self.current_player_color() == 1:
            if type(self.field[0][0]) == Rook and self.field[0][0].starting_position:
                if type(self.field[0][4]) == King and self.field[0][4].starting_position:
                    if self.field[0][1] == self.field[0][2] == self.field[0][3] is None \
                            and self.cell_is_under_attack(0, 1, self.current_player_color()) == \
                            self.cell_is_under_attack(0, 2, self.current_player_color()) \
                            == self.cell_is_under_attack(0, 3, self.current_player_color()) \
                            == self.cell_is_under_attack(0, 4, self.current_player_color()) is False:
                        k1 = self.field[0][4]
                        r1 = self.field[0][0]
                        self.field[0][4] = None
                        self.field[0][0] = None
                        self.field[0][2] = k1
                        self.field[0][3] = r1
                        self.color = opponent(self.color)
                        return True

        if self.current_player_color() == 2:
            if type(self.field[7][0]) == Rook and self.field[7][0].starting_position:
                if type(self.field[7][4]) == King and self.field[7][4].starting_position:
                    if self.field[7][1] == self.field[7][2] == self.field[7][3] is None \
                            and self.cell_is_under_attack(7, 1, self.current_player_color()) \
                            == self.cell_is_under_attack(7, 2, self.current_player_color()) \
                            == self.cell_is_under_attack(7, 3, self.current_player_color()) \
                            == self.cell_is_under_attack(7, 4, self.current_player_color()) is False:
                        k1 = self.field[7][4]
                        r1 = self.field[7][0]
                        self.field[7][4] = None
                        self.field[7][0] = None
                        self.field[7][2] = k1
                        self.field[7][3] = r1
                        self.color = opponent(self.color)
                        return True
        return False

    def castling7(self):
        if self.current_player_color() == 1:
            if type(self.field[0][7]) == Rook and self.field[0][7].starting_position:
                if type(self.field[0][4]) == King and self.field[0][4].starting_position:
                    if self.field[0][6] == self.field[0][5] is None \
                            and self.cell_is_under_attack(0, 6, self.current_player_color()) \
                            == self.cell_is_under_attack(0, 5, self.current_player_color()) == \
                            self.cell_is_under_attack(0, 4, self.current_player_color()) is False:
                        k1 = self.field[0][4]
                        r1 = self.field[0][7]
                        self.field[0][4] = None
                        self.field[0][7] = None
                        self.field[0][6] = k1
                        self.field[0][5] = r1
                        self.color = opponent(self.color)
                        return True

        if self.current_player_color() == 2:
            if type(self.field[7][7]) == Rook and self.field[7][7].starting_position:
                if type(self.field[7][4]) == King and self.field[7][4].starting_position:
                    if self.field[7][6] == self.field[7][5] is None \
                            and self.cell_is_under_attack(7, 6, self.current_player_color()) \
                            == self.cell_is_under_attack(7, 5, self.current_player_color()) == \
                            self.cell_is_under_attack(7, 4, self.current_player_color()) is False:
                        k1 = self.field[7][4]
                        r1 = self.field[7][7]
                        self.field[7][4] = None
                        self.field[7][4] = None
                        self.field[7][7] = None
                        self.field[7][6] = k1
                        self.field[7][5] = r1
                        self.color = opponent(self.color)
                        return True
        return False

    def check(self, color):
        for row in range(8):
            for col in range(8):
                piece = self.field[row][col]
                if type(piece) is King and piece.get_color() == color:
                    if self.cell_is_under_attack(row, col, color):
                        return True
                    else:
                        return False
        return False


class Rook:

    def __init__(self, color):
        self.color = color
        self.starting_position = True

    def was_moved(self):
        self.starting_position = False

    def get_color(self):
        return self.color

    def char(self):
        return 'R'

    def can_move(self, board, row, col, row1, col1):
        # Невозможно сделать ход в клетку, которая не лежит в том же ряду
        # или столбце клеток.
        if row != row1 and col != col1:
            return False

        step = 1 if (row1 >= row) else -1
        for r in range(row + step, row1, step):
            # Если на пути по горизонтали есть фигура
            if not (board.get_piece(r, col) is None):
                return False

        step = 1 if (col1 >= col) else -1
        for c in range(col + step, col1, step):
            # Если на пути по вертикали есть фигура
            if not (board.get_piece(row, c) is None):
                return False

        return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Pawn:

    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'P'

    def can_move(self, board, row, col, row1, col1):
        # Пешка может ходить только по вертикали
        # "взятие на проходе" не реализовано
        if col != col1:
            return False
        # Пешка может сделать из начального положения ход на 2 клетки
        # вперёд, поэтому поместим индекс начального ряда в start_row.
        if self.color == WHITE:
            direction = 1
            start_row = 1
        else:
            direction = -1
            start_row = 6

        # ход на 1 клетку
        if row + direction == row1:
            return True

        # ход на 2 клетки из начального положения
        if (row == start_row
                and row + 2 * direction == row1
                and board.field[row + direction][col] is None):
            return True

        return False

    def can_attack(self, board, row, col, row1, col1):
        direction = 1 if (self.color == WHITE) else -1
        return (row + direction == row1
                and (col + 1 == col1 or col - 1 == col1))


class Knight:

    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'N'  # kNight, буква 'K' уже занята королём

    def can_move(self, board, row, col, row1, col1):
        if not correct_coords(row1, col1):
            return False

        delta_row = abs(row - row1)
        delta_col = abs(col - col1)
        if max(delta_col, delta_row) == 2 and min(delta_col, delta_row) == 1:
            return True
        return False

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class King:
    def __init__(self, color):
        self.color = color
        self.starting_position = True

    def was_moved(self):
        self.starting_position = False

    def get_color(self):
        return self.color

    def char(self):
        return 'K'

    def can_move(self, board, row, col, row1, col1):
        if not correct_coords(row, col):
            return False
        color = self.get_color()
        if color == 1:
            if row == 0 and col == 4 and row1 == 0 and col1 == 6:
                if board.castling7():
                    return True
            if row == 0 and row1 == 0 and col == 4 and col1 == 2:
                if board.castling0():
                    return True

        cells = list()
        cells.append((row1 + 1, col1) if correct_coords(row1 + 1, col1) else None)
        cells.append((row1 + 1, col1 + 1) if correct_coords(row1 + 1, col1 + 1) else None)
        cells.append((row1 + 1, col1 - 1) if correct_coords(row1 + 1, col1 - 1) else None)
        cells.append((row1, col1 + 1) if correct_coords(row1, col1 + 1) else None)
        cells.append((row1, col1 - 1) if correct_coords(row1, col1 - 1) else None)
        cells.append((row1 - 1, col1 + 1) if correct_coords(row1, col1 + 1) else None)
        cells.append((row1 - 1, col1 - 1) if correct_coords(row1, col1 - 1) else None)
        cells.append((row1 - 1, col1) if correct_coords(row1, col1) else None)

        for i in cells:
            if type(board.field[i[0]][i[1]]) == King and board.field[i[0]][i[1]].get_color() != board.color:
                return False

        if board.cell_is_under_attack(row1, col1, board.current_player_color()):
            return False
        return ((row + 1 == row1 or row - 1 == row1) and col == col1) or (
                (col + 1 == col1 or col - 1 == col1) and row == row1) or (
                       row + 1 == row1 and (col + 1 == col1 or col - 1 == col1)) or (
                       row - 1 == row1 and (col + 1 == col1 or col - 1 == col1))

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Queen:

    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'Q'

    def can_move(self, board, row, col, row1, col1):

        piece1 = board.get_piece(row1, col1)
        if not (piece1 is None) and piece1.get_color() == self.color:
            return False
        if row == row1 or col == col1:
            step = 1 if (row1 >= row) else -1
            for r in range(row + step, row1, step):
                if not (board.get_piece(r, col) is None):
                    return False
            step = 1 if (col1 >= col) else -1
            for c in range(col + step, col1, step):
                if not (board.get_piece(row, c) is None):
                    return False
            return True

        if row - col == row1 - col1:
            step = 1 if (row1 >= row) else -1
            for r in range(row + step, row1, step):
                c = col - row + r
                if not (board.get_piece(r, c) is None):
                    return False
            return True

        if row + col == row1 + col1:
            step = 1 if (row1 >= row) else -1
            for r in range(row + step, row1, step):
                c = row + col - r
                if not (board.get_piece(r, c) is None):
                    return False
            return True
        return False

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Bishop:

    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'B'

    def can_move(self, board, row, col, row1, col1):

        if not correct_coords(row1, col1):
            return False

        k_row = 1
        if row1 > row:
            if col1 < col:
                k_row = -1

        if row1 < row:
            if col1 > col:
                k_row = - 1

        if (row - col != row1 - col1) and (row + col != row1 + col1):
            return False

        if row1 > row:
            it_row = range(1, row1 - row)
        elif row1 < row:
            it_row = range(row1 - row + 1, 0)

        if row == row1 or col == col1:
            return False
        for i in it_row:
            if board.cell(row + i, col + i * k_row) != '  ':
                return False
        return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)
