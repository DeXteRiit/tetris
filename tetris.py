import tkinter

width = 200
height = 400
canvas = tkinter.Canvas(width=width, height=height, bg="black")
canvas.pack()
size = 50


def create_block(x, y, color):
    return canvas.create_rectangle(x, y, x + size, y + size, fill=color)


def create_square_block():
    ids = []
    for i in range(2):
        ids.append(create_block(width // 2, i * size, "yellow"))
        ids.append(create_block(width // 2 + size, i * size, "yellow"))
    return ids


ids = create_square_block()
block_grid = [
    [0 for _ in range(width // size)] for _ in range(height // size)
]  # creates 2d list with [row][col] [[0 for _ in range(2)] for _ in range(3)] == [[0,0], [0,0], [0,0]]

# for row_index in range(height // size):
#     for col_index in range(width // size):
#         id = block_grid[row_index][col_index]
#         print(id)


def sync_with_grid():
    for row_index in range(height // size):
        for col_index in range(width // size):
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
            empty = [0 for _ in range(width // size)]
            new_grid.insert(0, empty)
        block_grid = new_grid
        sync_with_grid()
    block_grid = new_grid


def fall():
    global ids
    fallable = True

    for id in ids:
        coords = canvas.coords(id)
        row = int(coords[1] // size)
        col = int(coords[0] // size)
        if row + 1 >= len(block_grid) or block_grid[row + 1][col] != 0:
            fallable = False

    if fallable:
        for id in ids:
            canvas.move(id, 0, size)
    else:
        for id in ids:
            coords = canvas.coords(id)
            row = int(coords[1] // size)
            col = int(coords[0] // size)
            block_grid[row][col] = id
        clear_lines()
        ids = create_square_block()


def game_loop():
    fall()

    canvas.after(500, game_loop)


def move_left(event):
    moveble = True
    for id in ids:
        coords = canvas.coords(id)
        row = int(coords[1] // size)
        col = int(coords[0] // size)
        if canvas.coords(id)[0] <= 0 or block_grid[row][col - 1] != 0:
            moveble = False
    if moveble:
        for id in ids:
            canvas.move(id, -size, 0)


def move_right(event):
    moveble = True
    for id in ids:
        coords = canvas.coords(id)
        row = int(coords[1] // size)
        col = int(coords[0] // size)

        if canvas.coords(id)[2] >= 800 or block_grid[row][col + 1] != 0:
            moveble = False
    if moveble:
        for id in ids:
            canvas.move(id, size, 0)


canvas.bind_all("<Left>", move_left)
canvas.bind_all("<Right>", move_right)

if __name__ == "__main__":
    game_loop()
    canvas.mainloop()
