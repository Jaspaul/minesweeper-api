import random

from datetime import datetime
from typing import List, Literal


class Point:
    def __init__(self, row, column):
        self.row = row
        self.column = column


class Move:
    def __init__(
        self, point: Point, action: Literal["click", "flag"], timestamp: datetime
    ):
        self.point = point
        self.action = action
        self.timestamp = timestamp


class Cell:
    def __init__(self, position: Point):
        self.flagged = False
        self.neighbour_count = 0
        self.position = position
        self.revealed = False

    def toggle_flag(self):
        self.flagged = not self.flagged

    def plant_bomb(self):
        self.neighbour_count = -1

    def is_bomb(self):
        return self.neighbour_count == -1

    def has_neighbours(self):
        return self.neighbour_count > 0


def surrounding_cells(gameboard: List[List[Cell]], point: Point) -> List[Cell]:
    rows = len(gameboard)
    columns = len(gameboard[0])

    return [
        gameboard[row][col]
        for row in [point.row - 1, point.row, point.row + 1]
        for col in [point.column - 1, point.column, point.column + 1]
        if row >= 0 and row < rows and col >= 0 and col < columns
    ]


def create(rows: int, columns: int, bomb_count: int) -> List[List[Cell]]:
    if bomb_count > rows * columns - 1:
        max_plus_one = rows * columns
        raise ValueError(f"Bomb count must be < rows * columns ({max_plus_one})")

    gameboard = [
        [Cell(Point(row, column)) for column in range(columns)] for row in range(rows)
    ]

    available_positions = [
        [row, column] for column in range(columns) for row in range(rows)
    ]
    random.shuffle(available_positions)

    bombs = []
    for bomb in range(bomb_count):
        [row, column] = available_positions.pop()
        bombs.append([row, column])
        gameboard[row][column].plant_bomb()

    for [row, column] in bombs:
        for cell in surrounding_cells(gameboard, Point(row, column)):
            if not cell.is_bomb():
                cell.neighbour_count += 1

    return gameboard


def reveal(gameboard: List[List[Cell]], selected: Point) -> List[List[Cell]]:
    remaining = [gameboard[selected.row][selected.column]]

    if gameboard[selected.row][selected.column].flagged:
        return gameboard

    while len(remaining) > 0:
        current = remaining.pop()
        current.revealed = True

        if not current.is_bomb() and not current.has_neighbours():
            for cell in surrounding_cells(gameboard, current.position):
                if not cell.is_bomb() and not cell.revealed:
                    remaining.append(cell)

    return gameboard


def status(gameboard: List[List[Cell]]) -> Literal["W", "L", "I"]:
    total_cells = 0
    revealed_cells = 0
    bomb_count = 0

    for row in gameboard:
        for cell in row:
            if cell.is_bomb() and cell.revealed:
                return "L"
            if cell.is_bomb():
                bomb_count += 1
            if cell.revealed:
                revealed_cells += 1
            total_cells += 1

    if total_cells - revealed_cells == bomb_count:
        return "W"

    return "I"


def is_on_gameboard(point: Point, gameboard: List[List[Cell]]) -> bool:
    return (
        point.row >= 0
        and point.row < len(gameboard)
        and point.column >= 0
        and point.column < len(gameboard[0])
    )
