from Helper import correct_coords


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
