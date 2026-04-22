from django.urls import path

from .views import ask, index

urlpatterns = [
    path("", index, name="index"),
    path("api/ask/", ask, name="ask"),
]
