class Bishop:

    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'B'

    def can_move(self, board, row, col, row1, col1):
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
