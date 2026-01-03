from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/new-game/', views.new_game, name='new_game'),
    path('api/game-state/', views.get_game_state, name='game_state'),
    path('api/draw-card/', views.draw_card, name='draw_card'),
    path('api/move-card/', views.move_card, name='move_card'),
    path('api/auto-move/', views.auto_move, name='auto_move'),
]