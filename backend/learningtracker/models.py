from datetime import date

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

from .utils.error_const import DAILY_LEARNING_ERRORS, TAG_ERRORS


class Tag(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="tags",
        verbose_name="User",
        help_text="The user who owns this tag.",
    )
    name = models.CharField(
        max_length=30,
        verbose_name="Tag Name",
        help_text="The name of the tag.",
    )

    class Meta:
        unique_together = ("user", "name")
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def clean(self):
        errors = {}
        # Check for uniqueness of the tag for the user
        if Tag.objects.filter(user=self.user, name=self.name).exists():
            errors["duplicate_name"] = TAG_ERRORS["duplicate_name"]
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        # Ensure validation is performed before saving
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.user.username})"


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
    tags = models.ManyToManyField(
        Tag,
        related_name="daily_learnings",
        blank=True,
        verbose_name="Tags",
        help_text="Tags associated with this learning entry.",
    )

    class Meta:
        verbose_name = "Daily Learning Entry"
        verbose_name_plural = "Daily Learning Entries"
        constraints = [
            models.UniqueConstraint(fields=["user", "date"], name="unique_user_date")
        ]
        indexes = [
            models.Index(fields=["user", "date"]),
        ]

    def __str__(self):
        return (
            f"{self.user.username}'s {self.learning_type} "
            f"Learning on {self.date.strftime('%b %d, %Y')}"
        )

    def clean(self):
        """
        Add custom validation logic for the model.
        """
        errors = {}
        # Validate Date is not in the Future
        if self.date > date.today():
            errors["date"] = [DAILY_LEARNING_ERRORS["invalid_date"]]

        # Validate Description has Minimum Length
        if len(self.description) < 5:
            errors["description"] = [DAILY_LEARNING_ERRORS["invalid_description"]]

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        """
        Override save to enforce validation by calling full_clean.
        """
        self.full_clean()
        super().save(*args, **kwargs)

    @classmethod
    def entries_vs_days(cls, user):
        """
        Returns the ratio of learning entries to the number of days in the current year.
        """
        total_days = (date.today() - date(date.today().year, 1, 1)).days + 1
        entries = cls.objects.filter(user=user, date__year=date.today().year).count()
        return entries, total_days
