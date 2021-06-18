from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.title, name="title"),
    path("search", views.search, name="search"),
    path("create", views.create, name="create"),
    path("wiki/edit/<str:title>", views.edit, name="edit"),
    path("random", views.random_entry, name="random")
]