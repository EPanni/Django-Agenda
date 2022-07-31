from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.search, name="search"),
    path("<int:contact_id>", views.display_contact, name="display_contact"),
]
