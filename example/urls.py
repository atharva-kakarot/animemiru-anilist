from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("anime/id=<int:anime_id>", views.anime_view, name="anime-view"),
    path("api-proxy/<str:search_query>", views.search_view, name="api-proxy")
]