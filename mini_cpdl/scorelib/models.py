from django.db import models


class Score(models.Model):
    title = models.CharField(max_length=100)
    composer = models.CharField(max_length=100)
    voicing = models.CharField(max_length=100)

    def __str__(self):
        return self.composer + ": " + self.title + " (" + self.voicing + ")"
