from django.urls import path

from . import views

app_name = 'ratesmash'
urlpatterns = [
    path('', views.index, name='index'),
    path('create_room/', views.create_room, name='create_room'),
    path('room_detail/<int:room_id>/', views.room_detail, name='room_detail'),
    path('join_room/<int:room_id>/', views.join_room, name='join_room'),
    path('delete_room/<int:room_id>/', views.delete_room, name='delete_room'),
    path('send_result/<int:room_id>/', views.send_result, name='send_result'),
    path('all_players/', views.all_players, name='all_players'),
    path('player_detail/<int:player_id>/', views.player_detail, name='player_detail'),
    path('howtoplay/', views.howtoplay, name='howtoplay'),
    path('error_message/', views.error_message, name='error_message'),
]