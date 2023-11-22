from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView




urlpatterns = [
    path("dashboard/", views.Home.as_view(), name="search" ),
    path("", view=views.Landingpage.as_view(), name="landing"),
    path("login/", view=views.LoginView.as_view(), name="login"),
    path("signup/", view=views.SignUpView.as_view(), name="signup"),
    path("logout/", views.APILogoutView.as_view(), name="logout"),
    path("save/", view=views.HandleVideo.as_view(), name="save_video" ),
    path("users/", views.userview.as_view(), name="userview")
    
]
