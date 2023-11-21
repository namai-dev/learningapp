from django.urls import path
from . import views


urlpatterns = [
    path("dashboard/", views.Home.as_view(), name="search" ),
    path("", view=views.Landingpage.as_view(), name="landing"),
    path("login/", view=views.LoginView.as_view(), name="login"),
    path("signup/", view=views.SignUpView.as_view(), name="login")
]
