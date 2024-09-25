from django.db import models


class StatusChoices(models.TextChoices):
    NEW = 'NEW'
    ACTIVE = 'ACTIVE'
    QUEUED = 'QUEUED'
    COMPLETED = 'COMPLETED'
    CANCELLED = 'CANCELLED'
