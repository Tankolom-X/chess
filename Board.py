from pieces.Pawn import Pawn
from pieces.King import King
from pieces.Rook import Rook
from pieces.Knight import Knight
from pieces.Bishop import Bishop
from pieces.Queen import Queen

from Helper import WHITE, BLACK, correct_coords, opponent


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
            return False
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
        self.field[row][col] = None
        self.field[row1][col1] = piece
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
