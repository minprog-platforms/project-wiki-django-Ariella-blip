from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("random/", views.random_entry, name="random"),
    path("new/", views.new_page, name="new"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search", views.search, name="search"),
]
