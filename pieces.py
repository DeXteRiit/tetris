from constants import *


def init_canvas(canvas):
    global _canvas
    _canvas = canvas


class Block:
    def __init__(self, col_pos, row_pos, color):
        self.col_pos = col_pos
        self.row_pos = row_pos
        self.color = color
        self.id = _canvas.create_rectangle(
            col_pos * SIZE,
            row_pos * SIZE,
            col_pos * SIZE + SIZE,
            row_pos * SIZE + SIZE,
            fill=color,
        )

    def move(self, offset_col, offset_row):
        self.col_pos += offset_col
        self.row_pos += offset_row
        _canvas.move(self.id, offset_col * SIZE, offset_row * SIZE)

    def moveto(self, col_pos, row_pos):
        self.col_pos = col_pos
        self.row_pos = row_pos
        _canvas.moveto(self.id, self.col_pos * SIZE, self.row_pos * SIZE)


class Piece:
    def __init__(self, col_pos, row_pos, color):
        self.col_pos = col_pos
        self.row_pos = row_pos
        self.color = color
        self.blocks = []

    def move(self, offset_col, offset_row):
        self.col_pos += offset_col
        self.row_pos += offset_row
        for block in self.blocks:
            block.move(offset_col, offset_row)


class Square_piece(Piece):
    def __init__(self, col_pos, row_pos, color):
        super().__init__(col_pos, row_pos, color)
        for i in range(2):
            self.blocks.append(Block(col_pos - 1, row_pos - i, color))
            self.blocks.append(Block(col_pos, row_pos - i, color))
        self.col_pos -= 0.5
        self.row_pos -= 0.5


class Long_piece(Piece):
    def __init__(self, col_pos, row_pos, color):
        super().__init__(col_pos, row_pos, color)
        for i in range(4):
            self.blocks.append(Block(col_pos - 2 + i, row_pos, color))


class L_piece(Piece):
    def __init__(self, col_pos, row_pos, color):
        super().__init__(col_pos, row_pos, color)
        for i in range(3):
            self.blocks.append(Block(col_pos - 1 + i, row_pos + 1, color))
        self.blocks.append(Block(col_pos + 1, row_pos, color))


class J_piece(Piece):
    def __init__(self, col_pos, row_pos, color):
        super().__init__(col_pos, row_pos, color)
        for i in range(3):
            self.blocks.append(Block(col_pos - 1 + i, row_pos, color))
        self.blocks.append(Block(col_pos + 1, row_pos + 1, color))


class S_piece(Piece):
    def __init__(self, col_pos, row_pos, color):
        super().__init__(col_pos, row_pos, color)
        for i in range(2):
            self.blocks.append(Block(col_pos - i, row_pos - i, color))
            self.blocks.append(Block(col_pos + 1 - i, row_pos - i, color))


class Z_piece(Piece):
    def __init__(self, col_pos, row_pos, color):
        super().__init__(col_pos, row_pos, color)
        for i in range(2):
            self.blocks.append(Block(col_pos + i, row_pos - i, color))
            self.blocks.append(Block(col_pos + 1 + i, row_pos - i, color))


class T_piece(Piece):
    def __init__(self, col_pos, row_pos, color):
        super().__init__(col_pos, row_pos, color)
        for i in range(3):
            self.blocks.append(Block(col_pos - 1 + i, row_pos, color))
        self.blocks.append(Block(col_pos, row_pos - 1, color))
