from tetris import block_grid, width, height, size


def test_block_grid_cell_independency():
    row_refrences = [id(row) for row in block_grid]
    assert len(row_refrences) == len(set(row_refrences)), (
        "Bug detected: Multiple rows share the exact same memory reference (aliasing)!"
    )
    assert len(block_grid) >= 2
    assert len(block_grid[0]) >= 1
    block_grid[0][0] = 999
    assert block_grid[1][0] == 0, (
        "Bug detected, Modifying row 0, changed row 1; Cells are aliased"
    )
