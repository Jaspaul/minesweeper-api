from rest_framework import serializers
from .models import Game
import jsonpickle


def get_cell_image(game, cell):
    if game.status == "I":
        if cell.is_bomb() and cell.revealed:
            return "bomb-result-error.png"
        if cell.flagged:
            return "square-flagged.png"
        if cell.revealed:
            if cell.neighbour_count == 0:
                return "square-clicked.png"
            return f"square-{cell.neighbour_count}.png"
        return "square-unclicked.png"

    if cell.is_bomb() and cell.revealed:
        return "bomb-result-error.png"

    if cell.flagged and not cell.is_bomb():
        return "bomb-result-incorrect.png"

    if cell.flagged and cell.is_bomb():
        return "square-flagged.png"

    if cell.revealed and cell.neighbour_count == 0:
        return "square-clicked.png"

    if cell.revealed:
        return f"square-{cell.neighbour_count}.png"

    if cell.is_bomb():
        return "bomb-result-location.png"

    return "square-unclicked.png"


class GameDeserializer(serializers.ModelSerializer):
    board = serializers.SerializerMethodField()
    moves = serializers.SerializerMethodField()

    def get_board(self, obj):
        board = jsonpickle.decode(obj.board)

        for row in board:
            for i in range(len(row)):
                row[i] = get_cell_image(obj, row[i])

        return board

    def get_moves(self, obj):
        return len(jsonpickle.decode(obj.moves))

    class Meta:
        model = Game
        fields = [
            "id",
            "player_name",
            "status",
            "bomb_count",
            "rows",
            "columns",
            "board",
            "moves",
            "last_moved_at",
        ]


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = [
            "player_name",
            "status",
            "bomb_count",
            "rows",
            "columns",
            "board",
            "moves",
            "last_moved_at",
        ]
