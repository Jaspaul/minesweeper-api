from django.db import models


# Create your models here.
class Game(models.Model):
    STATUSES = {
        "W": "Win",
        "L": "Lose",
        "I": "InProgress",
    }

    board = models.TextField(null=False)
    bomb_count = models.IntegerField()
    columns = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_moved_at = models.DateTimeField(auto_now_add=True)
    moves = models.TextField(null=False)
    player_name = models.CharField(max_length=20)
    rows = models.IntegerField()
    status = models.CharField(max_length=1, choices=STATUSES)

    def in_progress(self):
        return self.status == "I"
