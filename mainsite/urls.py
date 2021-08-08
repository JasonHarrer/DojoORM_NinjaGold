from django.urls import path
from . import views


urlpatterns = [
                path('', views.index),
                path('process-game', views.process_game),
                path('process-money', views.process_money),
                path('reset', views.reset),
                path('start', views.start),
                path('game-over', views.game_over)
              ]
