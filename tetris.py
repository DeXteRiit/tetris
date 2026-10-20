import random
import tkinter

rows = 20
cols = 10
size = 50
canvas = tkinter.Canvas(width=cols * size, height=rows * size, bg="black")
canvas.pack()


class Block:
    def __init__(self, col_pos, row_pos, color):
        self.col_pos = col_pos
        self.row_pos = row_pos
        self.color = color
        self.id = canvas.create_rectangle(
            col_pos * size,
            row_pos * size,
            col_pos * size + size,
            row_pos * size + size,
            fill=color,
        )

    def move(self, offset_col, offset_row):
        self.col_pos += offset_col
        self.row_pos += offset_row
        canvas.move(self.id, offset_col * size, offset_row * size)

    def moveto(self, col_pos, row_pos):
        self.col_pos = col_pos
        self.row_pos = row_pos
        canvas.moveto(self.id, self.col_pos * size, self.row_pos * size)


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
            self.blocks.append(Block(col_pos, i, color))
            self.blocks.append(Block(col_pos + 1, i, color))


class Long_piece(Piece):
    def __init__(self, col_pos, row_pos, color):
        super().__init__(col_pos, row_pos, color)
        for i in range(4):
            self.blocks.append(Block(col_pos - 2 + i, row_pos, color))


class L_block(Piece):
    def __init__(self, col_pos, row_pos, color):
        super().__init__(col_pos, row_pos, color)
        for i in range(3):
            self.blocks.append(Block(col_pos - 1 + i, row_pos + 1, color))
        self.blocks.append(Block(col_pos + 1, row_pos, color))


class J_block(Piece):
    def __init__(self, col_pos, row_pos, color):
        super().__init__(col_pos, row_pos, color)
        for i in range(3):
            self.blocks.append(Block(col_pos - 1 + i, row_pos, color))
        self.blocks.append(Block(col_pos + 1, row_pos + 1, color))


class S_block(Piece):
    def __init__(self, col_pos, row_pos, color):
        super().__init__(col_pos, row_pos, color)
        for i in range(2):
            self.blocks.append(Block(col_pos - i, row_pos + i, color))
            self.blocks.append(Block(col_pos + 1 - i, row_pos + i, color))


class Z_block(Piece):
    def __init__(self, col_pos, row_pos, color):
        super().__init__(col_pos, row_pos, color)
        for i in range(2):
            self.blocks.append(Block(col_pos + i, row_pos + i, color))
            self.blocks.append(Block(col_pos + 1 + i, row_pos + i, color))


colors = ("blue", "red", "yellow", "green", "purple")
block_types = (Square_piece, Long_piece, L_block, J_block, S_block, Z_block)
active_piece = random.choice(block_types)(cols // 2, 0, random.choice(colors))
block_grid = [
    [0 for _ in range(cols)] for _ in range(rows)
]  # creates 2d list with [row][col] [[0 for _ in range(2)] for _ in range(3)] == [[0,0], [0,0], [0,0]]


def sync_with_grid():
    for row_index in range(rows):
        for col_index in range(cols):
            id = block_grid[row_index][col_index]
            if id != 0:
                canvas.moveto(id, col_index * size, row_index * size)


def clear_grid():
    global block_grid
    for row in block_grid:
        for id in row:
            if id != 0:
                canvas.delete(id)
    block_grid = [[0 for _ in range(cols)] for _ in range(rows)]


def clear_lines():
    global block_grid
    lines_cleared = 0
    new_grid = []
    for row in block_grid:
        count = 0
        for id in row:
            if id != 0:
                count += 1
        if count >= len(row):
            lines_cleared += 1
            for id in row:
                canvas.delete(id)
        else:
            new_grid.append(row)

    if lines_cleared > 0:
        for _ in range(lines_cleared):
            empty = [0 for _ in range(cols)]
            new_grid.insert(0, empty)
        block_grid = new_grid
        sync_with_grid()


def can_move_in_dir(offset_col, offset_row):
    for block in active_piece.blocks:
        next_col = block.col_pos + offset_col
        next_row = block.row_pos + offset_row
        if next_col < 0 or next_col >= cols or next_row < 0 or next_row >= rows:
            return False
        if block_grid[next_row][next_col] != 0:
            return False

    return True


def can_fall():

    for block in active_piece.blocks:
        if block.row_pos + 1 >= rows or not can_move_in_dir(0, 1):
            return False
    return True


def is_game_over():

    for block in active_piece.blocks:
        if not can_move_in_dir(0, 0):
            return True
    return False


def fall():
    global active_piece
    if can_fall():
        active_piece.move(0, 1)
    else:
        for block in active_piece.blocks:
            block_grid[block.row_pos][block.col_pos] = block.id
        clear_lines()
        active_piece = random.choice(block_types)(cols // 2, 0, random.choice(colors))


def game_loop():

    if is_game_over():
        clear_grid()
    else:
        fall()

    canvas.after(500, game_loop)


def move_left(event):
    if can_move_in_dir(-1, 0):
        active_piece.move(-1, 0)


def move_right(event):
    if can_move_in_dir(1, 0):
        active_piece.move(1, 0)


def drop(event):
    if not is_game_over():
        last_piece = active_piece
        while last_piece == active_piece:
            fall()


def can_rotate():
    for block in active_piece.blocks:
        offsetX = block.col_pos - active_piece.col_pos
        offsetY = block.row_pos - active_piece.row_pos
        new_col_pos = active_piece.col_pos + offsetY
        new_row_pos = active_piece.row_pos - offsetX
        if (
            new_col_pos < 0
            or new_col_pos >= cols
            or new_row_pos < 0
            or new_row_pos >= rows
        ):
            return False
        if block_grid[new_row_pos][new_col_pos] != 0:
            return False
    return True


def rotate(even):
    if can_rotate():
        for block in active_piece.blocks:
            offsetX = block.col_pos - active_piece.col_pos
            offsetY = block.row_pos - active_piece.row_pos
            new_col_pos = active_piece.col_pos + offsetY
            new_row_pos = active_piece.row_pos - offsetX
            block.moveto(new_col_pos, new_row_pos)


canvas.bind_all("<Left>", move_left)
canvas.bind_all("<Right>", move_right)
canvas.bind_all("<Down>", drop)
canvas.bind_all("<Up>", rotate)

if __name__ == "__main__":
    game_loop()
    canvas.mainloop()
