import pytest

import tetris


@pytest.fixture(autouse=True)
def reset_tetris_env():
    tetris.canvas.delete("all")
    tetris.block_grid = [[0 for _ in range(tetris.rows)] for _ in range(tetris.cols)]

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


# def test_game_over_clearing():
#     tetris.active_piece = tetris.Square_piece(0, 0, "yellow")
#     tetris.block_grid[1][0] = tetris.Block(2, 0, "white").id
#     assert tetris.is_game_over()


def test_clear_grid():
    tetris.block_grid[2][0] = tetris.Block(2, 0, "white").id
    last_count = len(tetris.canvas.find_all())
    tetris.clear_grid()
    assert last_count - 1 == len(tetris.canvas.find_all())


def test_canvas_del():
    last_count = len(tetris.canvas.find_all())
    id = tetris.canvas.create_rectangle(0, 0, 10, 10)
    current_count = len(tetris.canvas.find_all())
    assert current_count == last_count + 1
    tetris.canvas.delete(id)
    assert last_count == len(tetris.canvas.find_all())
