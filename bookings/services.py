import uuid
from django.contrib.auth.models import User
from rest_framework import serializers, status
from typing import OrderedDict
from . import models, choices


class BookingServiceV1:

    @staticmethod
    def create_booking(data: OrderedDict, user: User):
        try:
            resource = models.Resource.objects.get(id=data['resource_id'])
        except (models.Resource.DoesNotExist, User.DoesNotExist, Exception):
            raise serializers.ValidationError({"detail": "Объект не найден."})

        time_delta = data['end_time'] - data['start_time']
        print(time_delta)
        print(resource.max_duration)
        if time_delta > resource.max_duration:
            raise serializers.ValidationError({"detail": "Превышена максимальная продолжительность бронирования."})


        conflicting_bookings = models.Booking.objects.filter(
            resource=resource,
            status=choices.StatusChoices.ACTIVE,
            end_time__gt=data['start_time'],
            start_time__lt=data['end_time']
        )

        if conflicting_bookings.count() < resource.max_slots:
            models.Booking.objects.create(
                user=user,
                resource=resource,
                start_time=data['start_time'],
                end_time=data['end_time'],
                status=choices.StatusChoices.ACTIVE,
            )
            return {"message": "Бронирование успешно зарегистрировано."}
        else:
            models.Booking.objects.create(
                user=user,
                resource=resource,
                start_time=data['start_time'],
                end_time=data['end_time'],
                status=choices.StatusChoices.QUEUED,
            )
            print(f'Пользователь {user} добавлен в очередь на {resource.name}')
            return {"message": "Ресурс занят. Вы добавлены в очередь."}

    @staticmethod
    def get_bookings():
        return models.Booking.objects.all()

    @staticmethod
    def cancel_booking(user: User, pk: uuid.UUID):
        try:
            booking = models.Booking.objects.get(pk=pk)
            if booking.user != user:
                return {"message": "Вы не можете отменить бронирование, так как это не ваша."}, status.HTTP_403_FORBIDDEN
            if booking.status == choices.StatusChoices.ACTIVE:
                resource = booking.resource
                booking.delete()
                next_booking = models.Booking.objects.filter(
                    resource=resource, status=choices.StatusChoices.QUEUED
                ).order_by('created_at').first()

                if next_booking:
                    next_booking.status = choices.StatusChoices.ACTIVE
                    next_booking.save()
                    print(f"Пользователь {next_booking.user} получил слот.")
                return {"message": "Вы успешно отменили бронирование."}, status.HTTP_204_NO_CONTENT
            return {"message": "Только активные бронирования можно отменить."}, status.HTTP_400_BAD_REQUEST
        except models.Booking.DoesNotExist:
            return {"message": "Бронирование не найдено."}, status.HTTP_404_NOT_FOUND