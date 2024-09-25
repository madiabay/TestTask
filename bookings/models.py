import uuid
from django.db import models

from . import choices


class Resource(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    description = models.TextField()
    max_duration = models.DurationField()  # max booking duration
    max_slots = models.PositiveIntegerField()  # max slots booked at once

    def __str__(self):
        return self.name


class Booking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name="bookings")
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name="bookings")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=choices.StatusChoices, default=choices.StatusChoices.NEW)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} booking {self.resource.name} from {self.start_time} to {self.end_time}"

    class Meta:
        unique_together = ('resource', 'start_time', 'end_time')