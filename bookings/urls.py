from django.urls import path
from . import views


urlpatterns = [
    path('bookings/', views.BookingViewSetV1.as_view({
        'post': 'create_booking',
        'get': 'list_bookings',
    })),
    path('bookings/<uuid:pk>/cancel/', views.BookingViewSetV1.as_view({'delete': 'cancel_booking'})),
]