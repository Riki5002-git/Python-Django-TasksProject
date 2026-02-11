from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Role(models.TextChoices):
        MANAGER = 'מנהל', 'מנהל'
        WORKER = 'עובד', 'עובד'

    id = models.AutoField(primary_key=True)
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.WORKER
    )
    team = models.ForeignKey(
        'Team',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="team_users"
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Team(models.Model):
    id = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=100)

    def __str__(self):
        return self.team_name


class Task(models.Model):
    class Status(models.TextChoices):
        NEW = 'חדש', 'חדש'
        IN_PROGRESS = 'בתהליך', 'בתהליך'
        DONE = 'הושלם', 'הושלם'

    id = models.AutoField(primary_key=True)
    task_name = models.CharField(max_length=100)
    task_description = models.TextField()
    end_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW
    )
    user = models.ForeignKey(
        'User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="user_tasks"
    )
    team_name = models.ForeignKey(
        'Team',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="team_tasks"
    )

    def __str__(self):
        worker_name = f"{self.user.first_name} {self.user.last_name}" if self.user else "ללא משתמש"
        return f"{self.task_name} - {worker_name} (צוות: {self.team_name})"