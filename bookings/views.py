from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from . import serializers, services, models


class BookingViewSetV1(ViewSet):
    booking_service = services.BookingServiceV1()

    def get_permissions(self):
        if self.action in ('create_booking', 'cancel_booking'):
            return (IsAuthenticated(), )
        elif self.action == 'list_bookings':
            return (AllowAny(), )

        return super().get_permissions()

    def create_booking(self, request, *args, **kwargs):
        serializer = serializers.BookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        message = self.booking_service.create_booking(data=serializer.validated_data, user=request.user)
        return Response(message, status=status.HTTP_201_CREATED)

    def list_bookings(self, request):
        bookings = self.booking_service.get_bookings()
        serializer = serializers.BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def cancel_booking(self, request, pk):
        message, status = self.booking_service.cancel_booking(user=request.user, pk=pk)
        return Response(message, status=status)

