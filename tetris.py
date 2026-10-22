import random
import tkinter

import pieces
from constants import *

canvas = tkinter.Canvas(width=COLS * SIZE, height=ROWS * SIZE, bg="black")

canvas.pack()
pieces.init_canvas(canvas)

block_types = tuple(pieces.Piece.__subclasses__())
active_piece = random.choice(block_types)(COLS // 2, 1, random.choice(COLORS))
block_grid = [
    [0 for _ in range(COLS)] for _ in range(ROWS)
]  # creates 2d list with [row][col] [[0 for _ in range(2)] for _ in range(3)] == [[0,0], [0,0], [0,0]]


def sync_with_grid():
    for row_index in range(ROWS):
        for col_index in range(COLS):
            id = block_grid[row_index][col_index]
            if id != 0:
                canvas.moveto(id, col_index * SIZE, row_index * SIZE)


def clear_grid():
    global block_grid
    for row in block_grid:
        for id in row:
            if id != 0:
                canvas.delete(id)
    block_grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]


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
            empty = [0 for _ in range(COLS)]
            new_grid.insert(0, empty)
        block_grid = new_grid
        sync_with_grid()


def can_move_in_dir(offset_col, offset_row):
    for block in active_piece.blocks:
        next_col = block.col_pos + offset_col
        next_row = block.row_pos + offset_row
        if next_col < 0 or next_col >= COLS or next_row < 0 or next_row >= ROWS:
            return False
        if block_grid[next_row][next_col] != 0:
            return False

    return True


def can_fall():

    for block in active_piece.blocks:
        if block.row_pos + 1 >= ROWS or not can_move_in_dir(0, 1):
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
        active_piece = random.choice(block_types)(COLS // 2, 1, random.choice(COLORS))
        # active_piece = Long_piece(cols // 2, 0, random.choice(COLORS))


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
        new_col_pos = int(active_piece.col_pos + offsetY)
        new_row_pos = int(active_piece.row_pos - offsetX)
        if (
            new_col_pos < 0
            or new_col_pos >= COLS
            or new_row_pos < 0
            or new_row_pos >= ROWS
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
            new_col_pos = int(active_piece.col_pos + offsetY)
            new_row_pos = int(active_piece.row_pos - offsetX)
            block.moveto(new_col_pos, new_row_pos)


canvas.bind_all("<Left>", move_left)
canvas.bind_all("<Right>", move_right)
canvas.bind_all("<Down>", drop)
canvas.bind_all("<Up>", rotate)

if __name__ == "__main__":
    game_loop()
    canvas.mainloop()
