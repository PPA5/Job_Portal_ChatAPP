from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_view, name='chat-index'),
    path('room/<str:room_name>/', views.room_view, name='chat-room'),
    path('<str:user_name>/', views.user_view, name='user-chat'),
]