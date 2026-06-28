from django.db import models
from django.conf import settings


class Category(models.Model):
    name   = models.CharField(max_length=100)
    color  = models.CharField(max_length=7, default='#6366f1')  # hex color
    user   = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='categories')

    class Meta:
        verbose_name_plural = 'categories'
        unique_together = ('name', 'user')

    def __str__(self):
        return self.name


class Task(models.Model):
    class Status(models.TextChoices):
        TODO        = 'todo',        'To Do'
        IN_PROGRESS = 'in_progress', 'In Progress'
        DONE        = 'done',        'Done'

    class Priority(models.IntegerChoices):
        LOW    = 1, 'Low'
        MEDIUM = 2, 'Medium'
        HIGH   = 3, 'High'

    title       = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status      = models.CharField(max_length=20, choices=Status.choices, default=Status.TODO)
    priority    = models.IntegerField(choices=Priority.choices, default=Priority.MEDIUM)
    due_date    = models.DateField(null=True, blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks')
    category    = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    completed_count = models.IntegerField(default=0)
    last_completed  = models.DateTimeField(null=True, blank=True)
    class Meta:
        ordering = ['-priority', 'due_date']

    def __str__(self):
        return self.title
# Create your models here.
