from django.urls import path

from . import views

urlpatterns = [
    path("who-made-me/", views.index, name="index"),
    path("get-word/<str:word>/", views.get_word, name="get-word"),
    path("number-to-word/", views.number_to_word, name="number-to-word"),
]
