from django.urls import path
from Reception.views import (worker_home, add_client, room_reservation, add_room, check_in_1, fetch_rooms,
                             search_reservation, reservation_details, delete_reservation)


urlpatterns = [
    path("", worker_home, name="worker_home"),
    path('add_client/', add_client, name='add_client'),
    path('room_reservation/', room_reservation, name='room_reservation'),
    path('add_room/', add_room, name='add_room'),
    path('check-in/', check_in_1, name='check_in'),
    path('fetch_rooms/', fetch_rooms, name='fetch_rooms'),
    path('search_reservation/', search_reservation, name='search_reservation'),
    path('reservation_details/<int:pk>/', reservation_details, name='reservation_details'),
    path('reservation/delete/<int:pk>/', delete_reservation, name='delete_reservation'),
]
