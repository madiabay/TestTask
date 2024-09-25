from rest_framework import serializers
from . import choices


class BookingSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    user_id = serializers.IntegerField(read_only=True)
    resource_id = serializers.UUIDField(required=True)
    start_time = serializers.DateTimeField(required=True)
    end_time = serializers.DateTimeField(required=True)
    status = serializers.ChoiceField(choices=choices.StatusChoices, read_only=True)

    def validate(self, data):
        start_time = data['start_time']
        end_time = data['end_time']

        if start_time >= end_time:
            raise serializers.ValidationError("End time must be after start time")

        return data
