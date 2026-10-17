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

    def update_pos(self):
        canvas.moveto(self.id, self.col_pos * size, self.row_pos * size)


class Piece:
    def __init__(self, col_pos, row_pos, color):
        self.col_pos = col_pos
        self.row_pos = row_pos
        self.color = color
        self.blocks = []


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


colors = ("blue", "red", "yellow", "green", "purple")
block_types = (Square_piece, Long_piece)
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


def fall():
    global active_piece
    fallable = True

    for block in active_piece.blocks:
        if (
            block.row_pos + 1 >= len(block_grid)
            or block_grid[block.row_pos + 1][block.col_pos] != 0
        ):
            fallable = False
            break

    if fallable:
        for block in active_piece.blocks:
            block.move(0, 1)
        active_piece.row_pos += 1
    else:
        for block in active_piece.blocks:
            block_grid[block.row_pos][block.col_pos] = block.id
        clear_lines()
        active_piece = random.choice(block_types)(cols // 2, 0, random.choice(colors))


def game_loop():
    fall()

    canvas.after(500, game_loop)


def move_left(event):
    moveble = True
    for block in active_piece.blocks:
        if block.col_pos <= 0 or block_grid[block.row_pos][block.col_pos - 1] != 0:
            moveble = False
            break
    if moveble:
        for block in active_piece.blocks:
            block.move(-1, 0)
        active_piece.col_pos -= 1


def move_right(event):
    moveble = True
    for block in active_piece.blocks:
        if (
            block.col_pos >= cols - 1
            or block_grid[block.row_pos][block.col_pos - 1] != 0
        ):
            moveble = False
            break
    if moveble:
        for block in active_piece.blocks:
            block.move(1, 0)
        active_piece.col_pos += 1


def drop(event):
    last_piece = active_piece
    while last_piece == active_piece:
        fall()


def rotate(even):
    for block in active_piece.blocks:
        offsetX = block.col_pos - active_piece.col_pos
        offsetY = block.row_pos - active_piece.row_pos
        block.col_pos = active_piece.col_pos + offsetY
        block.row_pos = active_piece.row_pos - offsetX
        block.update_pos()


canvas.bind_all("<Left>", move_left)
canvas.bind_all("<Right>", move_right)
canvas.bind_all("<Down>", drop)
canvas.bind_all("<Up>", rotate)

if __name__ == "__main__":
    game_loop()
    canvas.mainloop()
