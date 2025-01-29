import pytest

from minesweeper.gameboard import create, Point, reveal, Cell, status, is_on_gameboard


def test_create_gameboard_with_invalid_bomb_count():
    rows = 2
    cols = 2
    bomb_count = rows * cols

    with pytest.raises(ValueError):
        create(rows, cols, bomb_count)


def test_create_gameboard_with_maximum_bomb_count():
    rows = 10
    cols = 10
    bomb_count = rows * cols - 1

    gameboard = create(rows, cols, bomb_count)

    assert sum(cell.is_bomb() for row in gameboard for cell in row) == bomb_count


def test_create_gameboard_with_minimum_bomb_count():
    rows = 10
    cols = 10
    bomb_count = 1

    gameboard = create(rows, cols, bomb_count)

    assert sum(cell.is_bomb() for row in gameboard for cell in row) == bomb_count


def test_revealing_a_bomb_bounded_cell():
    point = Point(0, 0)
    board = [
        [Cell(Point(0, 0)), Cell(Point(0, 1)), Cell(Point(0, 2))],
        [Cell(Point(1, 0)), Cell(Point(1, 1)), Cell(Point(1, 2))],
        [Cell(Point(2, 0)), Cell(Point(2, 1)), Cell(Point(2, 2))],
    ]

    board[0][1].plant_bomb()
    board[1][0].plant_bomb()
    board[1][1].plant_bomb()

    reveal(board, point)

    assert board[0][0].revealed == True
    assert board[0][1].revealed == False
    assert board[0][2].revealed == False
    assert board[1][0].revealed == False
    assert board[1][1].revealed == False
    assert board[1][2].revealed == False
    assert board[2][0].revealed == False
    assert board[2][1].revealed == False
    assert board[2][2].revealed == False


def test_revealing_a_bomb():
    point = Point(0, 1)
    board = [
        [Cell(Point(0, 0)), Cell(Point(0, 1)), Cell(Point(0, 2))],
        [Cell(Point(1, 0)), Cell(Point(1, 1)), Cell(Point(1, 2))],
        [Cell(Point(2, 0)), Cell(Point(2, 1)), Cell(Point(2, 2))],
    ]

    board[0][1].plant_bomb()
    board[1][0].plant_bomb()
    board[1][1].plant_bomb()

    reveal(board, point)

    assert board[0][0].revealed == False
    assert board[0][1].revealed == True
    assert board[0][2].revealed == False
    assert board[1][0].revealed == False
    assert board[1][1].revealed == False
    assert board[1][2].revealed == False
    assert board[2][0].revealed == False
    assert board[2][1].revealed == False
    assert board[2][2].revealed == False


def test_revealing_an_unbounded_cell():
    point = Point(2, 2)
    board = [
        [Cell(Point(0, 0)), Cell(Point(0, 1)), Cell(Point(0, 2))],
        [Cell(Point(1, 0)), Cell(Point(1, 1)), Cell(Point(1, 2))],
        [Cell(Point(2, 0)), Cell(Point(2, 1)), Cell(Point(2, 2))],
    ]

    board[0][1].plant_bomb()
    board[1][0].plant_bomb()
    board[1][1].plant_bomb()

    reveal(board, point)

    assert board[0][0].revealed == False
    assert board[0][1].revealed == False
    assert board[0][2].revealed == True
    assert board[1][0].revealed == False
    assert board[1][1].revealed == False
    assert board[1][2].revealed == True
    assert board[2][0].revealed == True
    assert board[2][1].revealed == True
    assert board[2][2].revealed == True


def test_status_win():
    board = [
        [Cell(Point(0, 0)), Cell(Point(0, 1)), Cell(Point(0, 2))],
        [Cell(Point(1, 0)), Cell(Point(1, 1)), Cell(Point(1, 2))],
        [Cell(Point(2, 0)), Cell(Point(2, 1)), Cell(Point(2, 2))],
    ]
    board[0][1].plant_bomb()

    for row in board:
        for cell in row:
            if not cell.is_bomb():
                cell.revealed = True

    assert status(board) == "W"


def test_status_loss():
    board = [
        [Cell(Point(0, 0)), Cell(Point(0, 1)), Cell(Point(0, 2))],
        [Cell(Point(1, 0)), Cell(Point(1, 1)), Cell(Point(1, 2))],
        [Cell(Point(2, 0)), Cell(Point(2, 1)), Cell(Point(2, 2))],
    ]
    board[0][1].plant_bomb()
    board[0][1].revealed = True

    assert status(board) == "L"


def test_status_in_progress():
    board = [
        [Cell(Point(0, 0)), Cell(Point(0, 1)), Cell(Point(0, 2))],
        [Cell(Point(1, 0)), Cell(Point(1, 1)), Cell(Point(1, 2))],
        [Cell(Point(2, 0)), Cell(Point(2, 1)), Cell(Point(2, 2))],
    ]
    board[0][1].plant_bomb()
    board[1][0].plant_bomb()
    board[1][1].plant_bomb()
    board[0][0].revealed = True

    assert status(board) == "I"


def test_is_on_gameboard():
    board = [
        [Cell(Point(0, 0)), Cell(Point(0, 1)), Cell(Point(0, 2))],
        [Cell(Point(1, 0)), Cell(Point(1, 1)), Cell(Point(1, 2))],
    ]

    valid_points = [
        Point(0, 0),
        Point(0, 1),
        Point(0, 2),
        Point(1, 0),
        Point(1, 1),
        Point(1, 2),
    ]

    for point in valid_points:
        is_on_gameboard(point, board) == True


def test_is_not_on_gameboard():
    board = [
        [Cell(Point(0, 0)), Cell(Point(0, 1)), Cell(Point(0, 2))],
        [Cell(Point(1, 0)), Cell(Point(1, 1)), Cell(Point(1, 2))],
    ]

    invalid_points = [
        Point(-1, -1),
        Point(-1, 0),
        Point(-1, 1),
        Point(-1, 2),
        Point(-1, 3),
        Point(0, 3),
        Point(1, 3),
        Point(2, 3),
        Point(2, 2),
        Point(2, 1),
        Point(2, 0),
        Point(2, -1),
        Point(1, -1),
        Point(0, -1),
    ]

    for point in invalid_points:
        is_on_gameboard(point, board) == False
