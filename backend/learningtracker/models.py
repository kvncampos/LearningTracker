from django.contrib.auth.models import User
from django.db import models


class DailyLearning(models.Model):
    class Topics(models.TextChoices):
        PYTHON = "Python", "Python"
        DJANGO = "Django", "Django"
        FLASK = "Flask", "Flask"
        KUBERNETES = "Kubernetes", "Kubernetes"
        DOCKER = "Docker", "Docker"
        GRAFANA = "Grafana", "Grafana"
        SQL = "SQL", "SQL"
        NOSQL = "NoSQL", "NoSQL"
        REACT = "React", "React"
        ANGULAR = "Angular", "Angular"
        VUE = "Vue", "Vue"
        TESTING = "Testing", "Testing"
        CI_CD = "CI/CD", "CI/CD"
        DEVOPS = "DevOps", "DevOps"
        CLOUD = "Cloud", "Cloud"
        MACHINE_LEARNING = "Machine Learning", "Machine Learning"
        DATA_ANALYSIS = "Data Analysis", "Data Analysis"
        SECURITY = "Security", "Security"
        OTHER = "Other", "Other"

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="daily_learnings",
        verbose_name="User",
        help_text="The user who owns this learning entry.",
    )
    date = models.DateField(
        null=False,
        verbose_name="Learning Date",
        help_text="The date of the learning entry.",
    )
    learning_type = models.CharField(
        null=False,
        max_length=50,
        choices=Topics.choices,
        default=Topics.OTHER,
        verbose_name="Learning Topic",
        help_text="The topic of the learning entry.",
    )
    description = models.TextField(
        null=False,
        max_length=500,
        verbose_name="Description",
        help_text="A detailed description of what you learned.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At",
        help_text="When the entry was created.",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Updated At",
        help_text="When the entry was last updated.",
    )

    class Meta:
        verbose_name = "Daily Learning Entry"
        verbose_name_plural = "Daily Learning Entries"
        unique_together = ("user", "date")
        indexes = [
            models.Index(fields=["user", "date"]),
        ]

    def __str__(self):
        return f"{self.user.username}'s Learning on {self.date}"
