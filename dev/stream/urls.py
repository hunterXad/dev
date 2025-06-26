from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_room, name='create_stream_room'),
    path('room/<str:room_name>/', views.room, name='stream_room'),
    path('lobby/<str:room_name>/', views.lobby, name='stream_lobby'),
    path('room/<str:room_name>/handle/', views.handle_join_request, name='handle_join_request'),
    path('room/<str:room_name>/waiting/<str:user_name>/', views.waiting_page, name='waiting_page'),
    path('room/<str:room_name>/check/<str:user_name>/', views.check_join_status, name='check_join_status'),

]
