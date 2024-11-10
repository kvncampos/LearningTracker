from django.db import models


# Create your models here.
class DailyLearning(models.Model):
    date = models.DateField(unique=True, null=False)
    description = models.TextField(null=False)

    def __str__(self):
        return f"Learning on {self.date}"
