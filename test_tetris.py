import pytest

import tetris


@pytest.fixture(autouse=True)
def reset_tetris_env():
    tetris.canvas.delete("all")
    tetris.block_grid = [[0 for _ in range(tetris.cols)] for _ in range(tetris.rows)]

    yield


def test_block_grid_aliasing():
    row_refrences = [id(row) for row in tetris.block_grid]
    assert len(row_refrences) == len(set(row_refrences)), (
        "Bug detected: Multiple rows share the exact same memory reference (aliasing)!"
    )
    assert len(tetris.block_grid) >= 2
    assert len(tetris.block_grid[0]) >= 1
    tetris.block_grid[0][0] = 999
    assert tetris.block_grid[1][0] == 0, (
        "Bug detected, Modifying row 0, changed row 1; Cells are aliased"
    )


def test_game_over():
    tetris.active_piece = tetris.Square_piece(0, 0, "yellow")
    tetris.block_grid[1][0] = tetris.Block(2, 0, "white").id
    assert tetris.is_game_over()


def test_clear_grid():
    last_count = len(tetris.canvas.find_all())
    tetris.block_grid[2][0] = tetris.Block(2, 0, "white").id
    tetris.clear_grid()
    assert last_count == len(tetris.canvas.find_all())


def test_can_fall():
    tetris.active_piece = tetris.Square_piece(0, 1, "yellow")
    tetris.block_grid[1][1] = tetris.Block(1, 1, "white").id
    assert not tetris.can_fall()

    tetris.active_piece = tetris.Square_piece(tetris.rows - 1, 1, "yellow")
    assert not tetris.can_fall()


def test_clear_lines():
    last_count = len(tetris.canvas.find_all())
    for i in range(tetris.cols):
        tetris.block_grid[0][i] = tetris.Block(0, i, "white").id
    tetris.clear_lines()
    assert last_count == len(tetris.canvas.find_all())


def test_snc_with_grid():
    block = tetris.Block(2, 0, "white")

    tetris.block_grid[0][0] = block.id
    tetris.sync_with_grid()
    assert block.row_pos == 0


def test_can_move_in_dir():
    tetris.active_piece = tetris.Piece(0, 0, "yellow")
    tetris.active_piece.blocks = [tetris.Block(0, 0, "yellow")]
    assert not tetris.can_move_in_dir(0, -1)
    assert not tetris.can_move_in_dir(-1, 0)

    tetris.block_grid[0][1] = tetris.Block(1, 0, "white").id
    assert not tetris.can_move_in_dir(1, 0)

    tetris.block_grid[1][0] = tetris.Block(0, 1, "white").id
    assert not tetris.can_move_in_dir(0, 1)

    tetris.active_piece.blocks[0].moveto(tetris.cols - 1, tetris.rows - 1)
    assert not tetris.can_move_in_dir(0, 1)
    assert not tetris.can_move_in_dir(1, 0)

    tetris.block_grid[tetris.rows - 2][tetris.cols - 1] = tetris.Block(0, 1, "white").id
    assert not tetris.can_move_in_dir(0, -1)

    tetris.block_grid[tetris.rows - 1][tetris.cols - 2] = tetris.Block(0, 1, "white").id
    assert not tetris.can_move_in_dir(-1, 0)
