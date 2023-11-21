from django.urls import path
from . import views


urlpatterns = [
    path("dashboard/", views.Home.as_view(), name="search" ),
    path("", view=views.Landingpage.as_view(), name="landing")
]
