from .gameboard import Move, Point, create, is_on_gameboard, reveal, status
from .models import Game
from .serializers import GameSerializer, GameDeserializer

from django.utils import timezone
from rest_framework import status as rest_status
from rest_framework.response import Response
from rest_framework.views import APIView

import jsonpickle


class GameApiView(APIView):
    def get(self, request, *args, **kwargs):
        game = Game.objects.filter(pk=kwargs["pk"]).first()

        if not game:
            return Response(
                {"error": "Game not found"}, status=rest_status.HTTP_404_NOT_FOUND
            )

        serializer = GameDeserializer(game)
        return Response(serializer.data, status=rest_status.HTTP_200_OK)


class GameListApiView(APIView):
    def get(self, request, *args, **kwargs):
        games = Game.objects.all()
        serializer = GameDeserializer(games, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        data = {
            "player_name": request.data.get("player_name"),
            "rows": int(request.data.get("rows")),
            "columns": int(request.data.get("columns")),
            "bomb_count": int(request.data.get("bomb_count")),
        }

        if len(data["player_name"]) < 1 or len(data["player_name"]) > 20:
            return Response(
                {"error": "Player name must be between 1 and 20 characters"},
                status=rest_status.HTTP_400_BAD_REQUEST,
            )
        if (
            data["rows"] < 2
            or data["rows"] > 80
            or data["columns"] < 2
            or data["columns"] > 80
        ):
            return Response(
                {"error": "The number of rows and columns must be between 2 and 80"},
                status=rest_status.HTTP_400_BAD_REQUEST,
            )

        if data["bomb_count"] > data["rows"] * data["columns"] - 1:
            return Response(
                {
                    "error": f"Bomb count must be < rows * columns ({ data["rows"] * data["columns"] })"
                },
                status=rest_status.HTTP_400_BAD_REQUEST,
            )

        board = create(data["rows"], data["columns"], data["bomb_count"])

        data["board"] = jsonpickle.encode(board)
        data["moves"] = jsonpickle.encode([])
        data["status"] = status(board)
        data["last_moved_at"] = timezone.now().utcnow()

        serializer = GameSerializer(data=data)

        if serializer.is_valid():
            game = serializer.save()
            deserializer = GameDeserializer(game, many=False)
            return Response(deserializer.data)

        return Response(serializer.errors, status=rest_status.HTTP_400_BAD_REQUEST)


class ClickApiView(APIView):
    def post(self, request, *args, **kwargs):
        game = Game.objects.filter(pk=kwargs["pk"]).first()

        if not game:
            return Response(
                {"error": "Game not found"}, status=rest_status.HTTP_404_NOT_FOUND
            )

        if not game.in_progress():
            serializer = GameDeserializer(game)
            return Response(serializer.data, status=rest_status.HTTP_200_OK)

        point = Point(request.data.get("row"), request.data.get("column"))
        board = jsonpickle.decode(game.board)

        if not is_on_gameboard(point, board):
            return Response(
                {"error": "Invalid point"}, status=rest_status.HTTP_400_BAD_REQUEST
            )

        game.last_moved_at = timezone.now()
        moves = jsonpickle.decode(game.moves)

        moves.append(Move(point, "click", game.last_moved_at))
        board = reveal(board, point)

        game.moves = jsonpickle.encode(moves)
        game.status = status(board)
        game.board = jsonpickle.encode(board)

        game.save()

        serializer = GameDeserializer(game)
        return Response(serializer.data, status=rest_status.HTTP_200_OK)


class ToggleFlagApiView(APIView):
    def post(self, request, *args, **kwargs):
        game = Game.objects.filter(pk=kwargs["pk"]).first()

        if not game:
            return Response(
                {"error": "Game not found"}, status=rest_status.HTTP_404_NOT_FOUND
            )

        if not game.in_progress():
            serializer = GameDeserializer(game)
            return Response(serializer.data, status=rest_status.HTTP_200_OK)

        point = Point(request.data.get("row"), request.data.get("column"))
        board = jsonpickle.decode(game.board)

        if not is_on_gameboard(point, board):
            return Response(
                {"error": "Invalid point"}, status=rest_status.HTTP_400_BAD_REQUEST
            )

        game.last_moved_at = timezone.now().utcnow()
        moves = jsonpickle.decode(game.moves)

        moves.append(Move(point, "flag", game.last_moved_at))
        board[point.row][point.column].toggle_flag()

        game.moves = jsonpickle.encode(moves)
        game.status = status(board)
        game.board = jsonpickle.encode(board)

        game.save()

        serializer = GameDeserializer(game)
        return Response(serializer.data, status=rest_status.HTTP_200_OK)
