from django.db import models


# Create your models here.
class DailyLearning(models.Model):
    date = models.DateField(unique=True)
    description = models.TextField()

    def __str__(self):
        return f"Learning on {self.date}"
